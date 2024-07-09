from websockets.legacy.protocol import WebSocketCommonProtocol as websocket

from constants import DEFAULT_CHIPS
from constants import DEFAULT_TABLE_SEATS

from utils.sockets_util import gen_gameid
from .game_objects import Card
# from game_objects import Board
# from game_objects import Deck




# class Spectator:
#     pass

class Player:
    chips: int
    __hand: list[Card]

    is_folded: bool
    is_hand_shown: bool

    def __init__(self, chips: int, user = None):
        self.__chips = chips
        self.is_hand_shown = False
        self.is_folded = True
        self.user = user


    def chip_bet(self, amount: int) -> int:
        if self.chips - amount < 0:
            # TODO: raise not enough chips
            pass

        self.chips -= amount

        return amount
    

    def recieve_hand(self, hand: list[Card]):
        self.__hand = hand

    def recieve_chips(self, chips: int):
        self.chips += chips


class User:
    """
    Contains basic information about the User objects,
    which are specific to the Room object, which is 
    specific to the websocket connection
    """
    __socket_connection: websocket

    username: str
    is_spectator: bool

    player: Player | None

    def __init__(self, username, websocket, is_spectator=True):
        self.username = username
        self.__socket_connection = websocket
        self.is_spectator = is_spectator

    def get_socket(self):
        return self.__socket_connection

    def set_socket(self, websocket):
        self.__socket_connection = websocket

    def __repr__(self) -> str:
        return f"Username: {self.username}, Conn: {self.__socket_connection}"


class Seat:
    player: Player
    button: None

    def __init__(self):
        pass

    def eject_player(self):
        self.player = None
    
    def seat_player(self, player: Player):
        self.player = player


class Table:
    max_seats: int
    __seats: list[Seat]

    def __init__(self, max_seats: int):
        self.max_seats = max_seats
        self.__seats = []

        for _ in range(max_seats):
            self.__seats.append(Seat())

    def seat_user(self, seat_index: int, user: User):
        player = Player(DEFAULT_CHIPS, user)
        user.player = player
        player.user = user

        self.__seats[seat_index].seat_player(player)


class Room:

    __users: dict[str: User]

    __table: Table

    room_id: int

    max_capacity: int



    def __init__(self):
        self.room_id = gen_gameid()

        self.__users = dict()

        self.__table = Table(DEFAULT_TABLE_SEATS)

    def add_user(self, username, websocket, is_spectator=True):

        if username in self.__users.keys():

            if self.__users[username].get_socket() is None:
                # if the user is without a socket connection, replace it
                self.__users[username].set_socket(websocket)
                self.__users[username].is_spectator = is_spectator
                return True
            else:
                #self.__users[username].set_socket(websocket)
                return False

        else:
            new_user = User(username, websocket, is_spectator)
            self.__users[username] = new_user
            print(self.__users)
            return True

    def seat_user(self, username: str, seat_index: int) -> bool:
        user = self.__users.get(username)
        if user is not None:
            return self.__table.seat_user(seat_index, user)
        else:
            return False

    def get_users(self):
        return [user for user in self.__users.values() if user.get_socket() is not None]

    def remove_user_connection(self, username):
        user = self.__users.get(username)
        if user is not None:
            user.set_socket(None)

    def close_room(self):
        # shut down room kick users etc
        pass

    def to_dict(self):
        connected_users = [user.username for user in self.get_users()]
        dict_data = {"room_id": self.room_id, "connected_users": connected_users}
        return dict_data

    def __str__(self) -> str:
        return f"Room: {self.room_id}, Users: {self.__users}"