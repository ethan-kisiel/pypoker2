import asyncio
import json
import traceback

from websockets import serve

from websockets.exceptions import ConnectionClosedError
from websockets.exceptions import ConnectionClosedOK

from managers.room_manager import RoomManager




class SocketServer:
    host: str
    port: int
    pending_update: bool

    room_manager: RoomManager

    def __init__(self, host: str, port: int):
        self.host = host
        self.port = port
        self.pending_update = False

        ##self.__rooms: dict[str:Room] = dict()

        ##self.create_room()

    async def handler(self, websocket):
        while True:
            try:
                request = await websocket.recv()
                #print(request)
                data = json.loads(request)

                message_type = data.get("type")
                # print(data)
                if message_type == "join":
                    room_id = data["room_id"]
                    username = data["username"]
                    #print(self.room_manager.rooms)
                    user_joined = self.room_manager.join_user(room_id, username, websocket)

                    if user_joined:
                        message = {"type": "player_joined", "username": username}
                        await self.room_manager.broadcast_message(room_id, message)

                        message = {"type": "room_update", 
                                   "room_data": self.room_manager.rooms[room_id].to_dict()}

                        await self.room_manager.broadcast_message(room_id, message)

                        await self.room_manager.broadcast_game_update(room_id)
                        #rint(f"new user connected: {username}")
                if message_type == "chat_message":
            
                    room_id = data["room_id"]
                    message = data["message"]
                    username = data["username"]

                    data = {"type": "chat_message", "username": username, "message": message}

                    await self.room_manager.broadcast_message(room_id, message=data)
                
                if message_type == "request_seat":
                    print("Player Requested Seat")
                    room_id = data["room_id"]
                    username = data["username"]

                    self.room_manager.rooms[room_id].request_seat(username)
                    room = self.room_manager.rooms[room_id]

                    #data = {"type": "game_update", "table": room.table_dict()}
                    print(self.room_manager.rooms[room_id])

                    await self.room_manager.broadcast_game_update(room_id)

                else:
                    print(data)

                if message_type == "player_action":
                    room_id = data["room_id"]
                    action = data["action"]
                    username = data["username"]

                    chips = action.get("chips")

                    room = self.room_manager.rooms[room_id]
                    

                    action_result = None

                    if action["play_option"] == "fold":
                        action_result = room.handle_player_action(username, "fold")
                    if action["play_option"] == "check":
                        action_result = room.handle_player_action(username, "check")
 
                        sound_message_data = {"type": "play_sound", "sound": "check"}
                        await self.room_manager.broadcast_message(room_id, message=sound_message_data)

                    
                    if action["play_option"] == "raise":
                        action_result = room.handle_player_action(username, "raise", chips)

                        sound_message_data = {"type": "play_sound", "sound": "bet"}
                        await self.room_manager.broadcast_message(room_id, message=sound_message_data)

                    if action["play_option"] == "bet":
                        action_result = room.handle_player_action(username, "bet", chips)
                        
                        sound_message_data = {"type": "play_sound", "sound": "bet"}
                        await self.room_manager.broadcast_message(room_id, message=sound_message_data)
                    if action["play_option"] == "call":
                        action_result = room.handle_player_action(username, "call")
                        
                        sound_message_data = {"type": "play_sound", "sound": "bet"}
                        await self.room_manager.broadcast_message(room_id, message=sound_message_data)

                    await self.room_manager.broadcast_game_update(room_id)

                    for action in action_result:
                        message = ""
                        match action["type"]:
                            case "win":
                                for seat, (score, hand) in action["phase_result"]:

                                    message = f"{seat.player.user.username} won with: {",".join([card.unicode for card in hand])}"


                                    data = {"type": "chat_message", "username": "Server", "message": message, "quiet": False}
                                    await self.room_manager.broadcast_message(room_id, data)

                                    await asyncio.sleep(5)
                                    print("hello world")
                                    room.go_to_cleanup()
                                    await self.room_manager.broadcast_game_update(room_id)

                            case "check":
                                message = f"{action['user']} checked."
                            case "raise":
                                message = f"{action['user']} raised {action['amount']}."
                            case "bet":
                                message = f"{action['user']} bet {action['amount']}."
                            case "call":
                                message = f"{action['user']} called {action['amount']}."
                            case "fold":
                                message = f"{action['user']} folded."
                        
                        if action["type"] != "win":
                            data = {"type": "chat_message", "username": "Server", "message": message, "quiet": True}
                            await self.room_manager.broadcast_message(room_id, data)


            except ConnectionClosedError:
                await self.room_manager.kick_user(websocket)
                # message = {"type": "room_update", 
                #     "room_data": self.room_manager.rooms[room_id].to_dict()}
                # await self.room_manager.broadcast_message(room_id, message)
            except ConnectionClosedOK:
                await self.room_manager.kick_user(websocket)

               
                #await self.room_manager.broadcast_message(room_id, message)
                break

            except Exception as e:
                await self.room_manager.kick_user(websocket)
                print(f"EXCEPTION RAISED: {e}")
                traceback.print_exc()
                pass


    async def start_server(self):
        '''
        Starts Websocket server
        '''
        print(f"STARTING WEBSOCKET SERVER on {self.host}:{self.port}")
        # logging.getLogger("websockets").setLevel(logging.ERROR)
        async with serve(self.handler, self.host, self.port):
            await asyncio.Future()

    def run(self, room_manager: RoomManager):
        '''
        Runs Websocket server in asynchronous event loop
        '''
        print("LAUNCHING SERVER...")
        self.room_manager = room_manager
        asyncio.run(self.start_server())