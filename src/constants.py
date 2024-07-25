from enum import Enum

TEST = "Test"

FACES = ('c', 'd', 'h', 's')
VALUES = ( '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A')

DEFAULT_CHIPS = 10000
BIG_BLIND = 100
SMALL_BLIND = 50

DEFAULT_TABLE_SEATS = 7


class PhaseOfPlay(Enum):
    WAITING = "waiting"
    PREFLOP = "preflop"
    FLOP = "flop"
    TURN = "turn"
    RIVER = "river"
    CLEANUP = "cleanup"

class Button(Enum):
    NONE = "none"
    DEALER = "dealer"
    BIG_BLIND = "big_blind"
    SMALL_BLIND = "small_blind"

class PlayOption(Enum):
    BET = "bet"
    CALL = "call"
    RAISE = "raise"
    ALL_IN = "all_in"
    CHECK = "check"
    FOLD = "fold"
    SHOW_HAND = "show_hand"

class WebsocketMessageType(Enum):
    JOIN = "join"
    CHAT_MESSAGE = "chat_message"
    REQUEST_SEAT = "request_seat"
    PLAYER_ACTION = "player_action"


class CardFaces(Enum):
    CLUBS = "c"
    DIAMONDS = "d"
    HEARTS = "h"
    SPADES = "s"

    def get_unicode(face):
        if face == CardFaces.CLUBS:
            return "♣"
        if face == CardFaces.DIAMONDS:
            return "♦"
        if face == CardFaces.HEARTS:
            return "♥"
        if face == CardFaces.SPADES:
            return "♠"