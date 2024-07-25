import asyncio
import json

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
                    if action["play_option"] == "bet":
                        action_result = room.handle_player_action(username, "bet", chips)
                    if action["play_option"] == "call":
                        action_result = room.handle_player_action(username, "call")

                    await self.room_manager.broadcast_game_update(room_id)

                    if action_result is not None:
                        for seat_score in action_result:
                            message = f"{seat_score[0].player.user.username} won with: {",".join([card.unicode for card in seat_score[1][1]])}"
                            data = {"type": "chat_message", "username": "Server", "message": message}
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