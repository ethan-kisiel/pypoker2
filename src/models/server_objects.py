from websockets.legacy.protocol import WebSocketCommonProtocol as websocket

from constants import DEFAULT_CHIPS
from constants import BIG_BLIND
from constants import SMALL_BLIND
from constants import DEFAULT_TABLE_SEATS

from constants import PhaseOfPlay
from constants import Button
from constants import PlayOption

from utils.sockets_util import gen_gameid
from .game_objects import Card
from .game_objects import Board
from .game_objects import Deck
# from game_objects import Board
# from game_objects import Deck

# class Spectator:
#     pass

class PlayAction:
    username: str
    play_option: PlayOption
    chips: int

    def __init__(self, username: str,  play_option: PlayOption, chips: int):
        self.username = username
        self.play_option = play_option
        self.chips = chips

    def as_dict(self) -> dict:
        pass

    def from_dict(source: dict):
        username = source.get("username")
        play_option = PlayOption(source.get("play_option"))
        chips = source.get(source.get("chips"))
        return PlayAction(username, play_option, chips)


class Player:
    chips: int
    hand: list[Card]

    is_folded: bool
    is_all_in: bool

    is_hand_shown: bool

    current_bet: int = 0

    def __init__(self, chips: int, user = None):
        self.chips = chips
        self.is_hand_shown = False
        self.is_folded = True
        self.user = user
        self.hand = [None, None]

        self.seat = None


    def chip_bet(self, amount: int) -> int:
        if self.chips - amount < 0:
            # TODO: raise not enough chips
            pass
            amount = self.chips
            self.chips = 0
        else:
            self.chips -= amount

        self.current_bet += amount


        return amount

    def recieve_hand(self, hand: list[Card]):
        self.hand = hand
        print(hand)

    def recieve_chips(self, chips: int):
        self.chips += chips

    def as_dict(self, requesting_user=None):
        player_dict = dict()


        try:
            player_dict["chips"] = self.chips
            player_dict["is_folded"] = self.is_folded 
            player_dict["current_bet"] = self.current_bet

            player_dict["user"] = self.user.username if self.user is not None else None
            
            if self.hand[0] is None or self.hand[1] is None:
                player_dict["hand"] = None

            elif (self.user is None
                or self.user.username == requesting_user
                or self.is_hand_shown):
    
                player_dict["hand"] = [card.as_dict for card in self.hand]
            else:
                player_dict["hand"] = [{"face": "X", "value": "X"}, {"face": "X", "value": "X"}]
        except Exception as e:
            print(f"Error in player->as_dict: {e}")
            
        return player_dict
    
    @property
    def is_playing(self):
        if None in self.hand or self.is_folded:
            return False
        return True



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
    
    previous = None
    next = None

    player: Player
    button: Button

    is_current_turn: bool

    def __init__(self):
        self.player = None
        self.is_current_turn = False
        self.button = None


    def eject_player(self):
        self.player = None
    
    def seat_player(self, player: Player):
        self.player = player
        self.player.seat = self

    def get_active_next(self, include_folded_players = True):
        if self.next is not None and self.next.player is not None:
            if not include_folded_players:
                if self.get_active_next().player.is_folded:
                    return self.get_active_next().get_active_next(False)
            return self.next
        elif self.next is not None:
            return self.next.get_active_next()
        return None

    def as_dict(self, requesting_user = None):
        seat_dict = dict()

        seat_dict["button"] = self.button.value if self.button is not None else None
        seat_dict["is_current_turn"] = self.is_current_turn

        try:
            seat_dict["player"] = self.player.as_dict(requesting_user) if self.player is not None else None
        except Exception as e:
            print(f"Error in seat->as_dict: {e}")
        return seat_dict
    
    @property
    def is_empty(self):
        return self.player is None
    
    def __str__(self):
        return f"Seated user: {self.player.user.username if self.player is not None else None}"
    
    def __repr__(self):
        return f"Seated user: {self.player.user.username if self.player is not None else None}"


class Table:
    max_seats: int
    board: Board
    pot: int

    phase_of_play: PhaseOfPlay = PhaseOfPlay.WAITING
    highest_bet: int = 0

    __deck: Deck = Deck()
    __seats: list[Seat] = []

    def __init__(self, max_seats: int):
        self.max_seats = max_seats

        for _ in range(max_seats): # create seats
            self.__seats.append(Seat())

        for i, seat in enumerate(self.__seats):
            ''' initialize linked list of seats '''
            if i == 0:
                seat.previous = self.__seats[-1]
                seat.next = self.__seats[i+1]
        
            elif i == len(self.__seats) -1:
                seat.next = self.__seats[0]
                seat.previous = self.__seats[i-1]
            else:
                seat.next = self.__seats[i+1]
                seat.previous = self.__seats[i-1]

        self.pot = 0

    def seat_user(self, seat_index: int, user: User):
        if self.get_user_seat(user.username) is not None:
            return

        if self.__seats[seat_index].player is not None:
            # player object is seated at the table

            if self.__seats[seat_index].player.user is None:
                # player is at seat, but user is disconnected from player
                pass
            pass

        else:
            # player object
            player = Player(DEFAULT_CHIPS, user)
            user.player = player
            player.user = user

            self.__seats[seat_index].seat_player(player)

            if self.phase_of_play == PhaseOfPlay.WAITING and len(self.active_seats) >= 3:
                # if we are in the waiting phase and there are now 3 users seated, begin play
                self.progress_phase()

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
    
    
    def find_button_seat(self, button: Button):
        for seat in self.__seats:
            if seat.button == button:
                return seat
    @property  
    def active_unfolded_seats(self):
        return [seat for seat in self.active_seats if not seat.player.is_folded]

    def process_action(self, play_action: PlayAction):
        player_seat = self.get_user_seat(play_action.username)
        match play_action.play_option:
            case PlayOption.ALL_IN:
                #self.handle_bet()
                pass
            case PlayOption.BET:
                pass
            case PlayOption.CHECK:
                pass
            case PlayOption.FOLD:
                player_seat.player.is_folded = True
            case PlayOption.ALL_IN:
                pass
            case _:
                pass


        player_seat.is_current_turn = False

        if len(self.active_unfolded_seats) <= 1:
            self.phase_of_play = PhaseOfPlay.CLEANUP
            self.progress_phase()
        else:
            player_seat.get_active_next(False).is_current_turn = True
        # if win condition??

    
    def handle_bet(self, amount: int):
        self.pot += amount
        if amount > self.highest_bet:
            self.highest_bet = amount

    @property
    def active_seats(self):
        return [seat for seat in self.__seats if seat.player is not None]

    @property
    def are_bets_equal(self):
        for seat in self.active_seats:
            if seat.player.is_folded or seat.player.is_all_in:
                continue
            if seat.player.current_bet != self.highest_bet:
                return False
        return True


    def game_update(self, username: str):
        # gets game data based on the given user_id's permissions
        pass


    def deal_hands(self):
        for seat in self.active_seats:
            seat.player.recieve_hand(self.__deck.r_draw_cards(2))
            seat.player.is_folded = False
        self.phase_of_play = PhaseOfPlay.PREFLOP


    def deal_buttons(self):
        dealer = self.find_button_seat(Button.DEALER)
        if dealer is None:
            self.active_seats[0].button = Button.DEALER

            small_blind_seat =  self.active_seats[0].get_active_next()
            small_blind_seat.button = Button.SMALL_BLIND
            
            big_blind_seat = small_blind_seat.get_active_next()
            big_blind_seat.button = Button.BIG_BLIND

           # self.active_seats[0].get_active_next().button = Button.BIG_BLIND

        else:

            sb_seat = self.find_button_seat(Button.SMALL_BLIND)
            bb_seat = self.find_button_seat(Button.BIG_BLIND)

            sb_seat.button = None
            bb_seat.button = None
        
            dealer.button = None
            dealer.get_active_next().button = Button.DEALER
            new_dealer = self.find_button_seat(Button.DEALER)

            small_blind_seat = new_dealer.get_active_next()
            small_blind_seat.button = Button.SMALL_BLIND

            big_blind_seat = small_blind_seat.get_active_next()
            big_blind_seat.button = Button.BIG_BLIND

    def progress_phase(self):
        match self.phase_of_play:
            case PhaseOfPlay.WAITING:
                self.deal_hands()
                self.deal_buttons()

                for seat in self.active_seats:
                    seat.is_current_turn = False



                # Take Bets from buttons
                self.find_button_seat(Button.SMALL_BLIND).is_current_turn = True
                # take blinds
                bb_bet = self.find_button_seat(Button.BIG_BLIND).player.chip_bet(BIG_BLIND)
                sb_bet = self.find_button_seat(Button.SMALL_BLIND).player.chip_bet(SMALL_BLIND)
                #

                self.handle_bet(bb_bet)
                self.handle_bet(sb_bet)

                self.phase_of_play = PhaseOfPlay.PREFLOP

            case PhaseOfPlay.PREFLOP:
                self.phase_of_play = PhaseOfPlay.FLOP
            case PhaseOfPlay.FLOP:
                self.phase_of_play = PhaseOfPlay.TURN
            case PhaseOfPlay.RIVER:
                self.phase_of_play = PhaseOfPlay.CLEANUP
            case PhaseOfPlay.CLEANUP:
                print(f"Reached CLEANUP phase, proceeding to WAITING phase")

                self.__deck = Deck()
                self.phase_of_play = PhaseOfPlay.WAITING
                self.progress_phase()


    def as_dict(self, user = None):
        table_dict = dict()
        user_seat = None
        try:
            if user is not None:
                user_seat =  self.get_user_seat(user)

            if user_seat is not None:
                table_dict["player_seat"] = user_seat.as_dict(user)
                play_options = []

                if None not in user_seat.player.hand:
                    play_options.append(PlayOption.SHOW_HAND.value)
                    play_options.append(PlayOption.FOLD.value)

                if (user_seat.is_current_turn
                    and self.phase_of_play != PhaseOfPlay.WAITING
                    and self.phase_of_play != PhaseOfPlay.CLEANUP):
                   # if user_seat.player.chips
                   #TODO: check what player can do based on their chips
                    pass
                    if user_seat.player.current_bet < self.highest_bet:
                        play_options.append(PlayOption.BET.value)
                    elif user_seat.player.current_bet == self.highest_bet:
                        play_options.append(PlayOption.CHECK.value)

                table_dict["player_seat"]["play_options"] = play_options
            else:
                table_dict["player_seat"] = None

            table_dict["seats"] = [seat.as_dict() for seat in self.__seats if seat.is_empty or seat.player.user.username != user]
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
    
    def handle_player_action(self, username: str, play_option: str, chips = None):
        play_action_dict = {"username": username, "play_option": play_option, "chips": chips}
        play_action = PlayAction.from_dict(play_action_dict)

        self.__table.process_action(play_action)


    @property
    def capacity(self):
        return f"{len(self.get_users())}/{self.max_capacity}"

    def table_dict(self, user):
        return self.__table.as_dict(user)

    def __str__(self) -> str:
        return f"Room: {self.room_id}, Users: {self.__users}, Table: {self.__table}"

    def print_room(self, room_id):
        print(self.rooms[room_id])