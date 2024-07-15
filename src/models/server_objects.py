from websockets.legacy.protocol import WebSocketCommonProtocol as websocket

from constants import DEFAULT_CHIPS
from constants import DEFAULT_TABLE_SEATS

from utils.sockets_util import gen_gameid
from .game_objects import Card
from .game_objects import Board
from .game_objects import Deck
# from game_objects import Board
# from game_objects import Deck




# class Spectator:
#     pass

class Player:
    chips: int
    hand: list[Card]

    is_folded: bool
    is_hand_shown: bool

    def __init__(self, chips: int, user = None):
        self.chips = chips
        self.is_hand_shown = False
        self.is_folded = True
        self.user = user
        self.hand = [None, None]


    def chip_bet(self, amount: int) -> int:
        if self.chips - amount < 0:
            # TODO: raise not enough chips
            pass

        self.chips -= amount

        return amount

    def recieve_hand(self, hand: list[Card]):
        self.hand = hand

    def recieve_chips(self, chips: int):
        self.chips += chips

    def as_dict(self, requesting_user=None):
        player_dict = dict()


        try:
            player_dict["chips"] = self.chips
            player_dict["is_folded"] = self.is_folded 

            player_dict["user"] = self.user.username if self.user is not None else None
            
            if (self.user is None
                or self.user.username == requesting_user
                or self.is_hand_shown):
                player_dict["hand"] = self.hand
            else:
                player_dict["hand"] = ["x", "x"]
        except Exception as e:
            print(f"Error in player->as_dict: {e}")
            
        return player_dict




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
        self.player = None

    def eject_player(self):
        self.player = None
    
    def seat_player(self, player: Player):
        self.player = player

    def as_dict(self, requesting_user = None):
        seat_dict = dict()

        try:
            seat_dict["player"] = self.player.as_dict(requesting_user) if self.player is not None else None
        except Exception as e:
            print(f"Error in seat->as_dict: {e}")
        return seat_dict
    
    
    def __str__(self):
        return f"Seated user: {self.player.user.username if self.player is not None else None}"
    
    def __repr__(self):
        return f"Seated user: {self.player.user.username if self.player is not None else None}"


class Table:
    max_seats: int
    board: Board


    __deck: Deck
    __seats: list[Seat]
    __current_turn: int

    def __init__(self, max_seats: int):
        self.max_seats = max_seats
        self.__seats = []

        for _ in range(max_seats):
            self.__seats.append(Seat())

    def seat_user(self, seat_index: int, user: User):
        if self.get_user_seat(user.username) is not None:
            return

        if self.__seats[seat_index].player is not None:
            # player object is seated at the table

            if self.__seats[seat_index].player.user is None:
                pass
            pass

        else:
            # player object
            player = Player(DEFAULT_CHIPS, user)
            user.player = player
            player.user = user

            self.__seats[seat_index].seat_player(player)

    
    def deal_hands():
        pass

    def progress_phase():
        pass

    def as_dict():
        pass

    def find_empty_seat(self):
        for i, seat in enumerate(self.__seats):
            if seat.player is None:
                return i, seat

    def get_user_seat(self, username: str):
        for seat in self.__seats:
            if seat.player is None or seat.player.user is None:
                continue
            try:
                if seat.player.user.username == username:
                    return seat
            except Exception as e:
                print(f"Issue with getting user seat: {e}")

    def game_update(self, username: str):
        # gets game data based on the given user_id's permissions
        pass

    def as_dict(self, user = None):
        table_dict = dict()
        user_seat = None
        try:
            if user is not None:
                user_seat =  self.get_user_seat(user)

            if user_seat is not None:
                table_dict["player_seat"] = user_seat.as_dict(user)
            else:
                table_dict["player_seat"] = None

            table_dict["seats"] = [seat.as_dict() for seat in self.__seats]
        except Exception as e:
            print(f"Error in table->as_dict: {e}")
        return table_dict

    def __str__(self):
        return f"Seats: {[seat for seat in self.__seats]}"



class Room:

    __users: dict[str: User]

    __table: Table

    room_id: int

    max_capacity: int



    def __init__(self):
        self.room_id = gen_gameid()

        self.__users = dict()

        self.__table = Table(DEFAULT_TABLE_SEATS)
        self.max_capacity = 10

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

    def request_seat(self, username: str) -> bool:
        user = self.__users.get(username)
        if user is not None:
            i, seat = self.__table.find_empty_seat()
            return self.__table.seat_user(i, user)
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
    
    @property
    def capacity(self):
        return f"{len(self.get_users())}/{self.max_capacity}"

    def table_dict(self, user):
        return self.__table.as_dict(user)

    def __str__(self) -> str:
        return f"Room: {self.room_id}, Users: {self.__users}, Table: {self.__table}"

    def print_room(self, room_id):
        print(self.rooms[room_id])