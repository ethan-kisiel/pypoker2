import json
from models.server_objects import Room
from models.server_objects import User




from websockets.legacy.protocol import WebSocketCommonProtocol as websocket


#from models.server_objects import 

# Create and shut down rooms
# list available rooms and their player counts

# join users to rooms
# kick users from room


class RoomManager:
    rooms: dict[int: Room]

    def __init__(self):
        self.rooms = dict()

    def create_room(self,) -> int:
        """
        create room and add to rooms
        returns room id
        """
        room = Room()
        self.rooms[room.room_id] = room

        return room.room_id

    def close_room(self, room_id: int):
        #TODO: kick users
        room = self.rooms.get(room_id)

        del self.rooms[room_id]
        pass

    def join_user(self, room_id: int, username: str, websocket):
        room = self.rooms.get(room_id)
        if room is not None:
            return room.add_user(username, websocket)
    

    # def kick_user(self, username: str):
    #     pass
    
    async def kick_user(self, websocket):
        for room in self.rooms.values():
            for user in room.get_users():
                if user.get_socket() == websocket:
                    print("REMOVING USER")
                    room.remove_user_connection(user.username)
                    message = {"type": "user_disconnect", "username": user.username}
                    await self.broadcast_message(room.room_id, message)

    def get_rooms(self):
        return self.rooms.keys()

    async def broadcast_message(self, room_id: int, message: dict):
        try:
            s_message = json.dumps(message)
            print(f"Sending Message: {s_message}")

        except Exception as e:
            print(f"ERROR IN BROADCAST: {e}")
            return

        room = self.rooms.get(room_id)
        if room is not None:
            for user in room.get_users():
                try:
                    await user.get_socket().send(s_message)
                except Exception as e:
                    print(f"Failed to broadcast messasge: {e}")