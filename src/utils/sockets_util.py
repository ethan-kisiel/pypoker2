from random import randint
# from managers.room_manager import RoomManager

def gen_gameid() -> int:
    return randint(100000,999999)


# def handle_room_action(message: dict, room_manager: RoomManager):
#     pass