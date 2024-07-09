from random import randint as ri

from constants import FACES
from constants import VALUES

class Card:
    '''
    Playing card represented as "x_Y"
    where x = face, represented as the first letter
    of club, diamond, heart, spade and  Y = Value
    represented as a number value and capital first letter
    of Jack, Queen, King, Ace
    '''
    
    def __init__(self, face: int, value: int, str_rep: str = None) -> None:

        if str_rep is not None:
            self.sync(str_rep)
        else:
            try:
                self.__face = FACES[face]
                self.__value = VALUES[value]
            except:
                print("Could not instantiate Card")

    def sync(self, card_rep: str) -> None:
        '''
        Takes f_V representation of card
        sets self == to representation
        '''
        try:
            rep = card_rep.split('_')
            rep = (FACES.index(rep[0]), VALUES.index(rep[1]))
            self.__init__(rep[0], rep[1])
        except:
            print(type(card_rep))

    def __hash__(self):
        return VALUES.index(self.__value) + 1

    def __lt__(self, other) -> bool:
        if type(other) == Card:
            s_val, o_val = VALUES.index(self.__value), VALUES.index(other.get_value())
            return s_val < o_val
    
    def __le__(self, other) -> bool:
        if type(other) == Card:
            s_val, o_val = VALUES.index(self.__value), VALUES.index(other.get_value())
            return s_val <= o_val
    
    def __eq__(self, other) -> bool:
        if type(other) == Card:
            s_val, o_val = VALUES.index(self.__value), VALUES.index(other.get_value())
            return s_val == o_val
    
    def __gt__(self, other) -> bool:
        if type(other) == Card:
            s_val, o_val = VALUES.index(self.__value), VALUES.index(other.get_value())
            return s_val > o_val
    
    def __ge__(self, other) -> bool:
        if type(other) == Card:
            s_val, o_val = VALUES.index(self.__value), VALUES.index(other.get_value())
            return s_val >= o_val
    
    def __sub__(self, other) -> int:
        if type(other) == Card:
            s_val, o_val = VALUES.index(self.__value), VALUES.index(other.get_value())
            return s_val - o_val
    
    def get_value(self) -> str:
        return self.__value
    
    def get_face(self) -> str:
        return self.__face
    
    def get_points_value(self) -> int:
        '''
        Value specific to the points
        range of 1-13 (for scoring hand)
        '''
        return VALUES.index(self.__value) + 1

    def __str__(self) -> str:
        return f'{self.__face}_{self.__value}'

    def __repr__(self) -> str:
        return f'{self.__face}_{self.__value}'

class Deck:
    def __init__(self) -> None:
        self.__cards = []
        for f in range(len(FACES)):
            for v in range(len(VALUES)):
                self.__cards.append(Card(f, v))

    def get_cards(self) -> list[Card]:
        return self.__cards

    def get_string_cards(self) -> list[str]:
        '''
        Returns array of string representations
        of self.__cards
        '''
        cards = []
        for card in self.__cards:
            cards.append(str(card) + ',')
        return cards
    
    def r_draw_card(self) -> Card:
        '''
        Removes and returns random card
        '''
        stop = len(self.__cards) -1
        return self.__cards.pop(ri(0, stop))
    
    def r_draw_cards(self, amount) -> list[Card]:
        '''
        Draws and removes amount
        number of random cards
        '''

        cards = []
        for _ in range(amount):
            stop = len(self.__cards) -1
            card = self.__cards.pop(ri(0, stop))
            cards.append(card)

        return cards
    
    def draw_card(self, index: int) -> Card:
        '''
        Removes and returns card at designated index;
        if error, returns 0
        (Debugging purposes only)
        '''
        try:
            return self.__cards.pop(index)
        except:
            return 0

    def reset(self) -> None:
        self.__init__()

    def __repr__(self) -> str:
        cards = ''
        cards.join(self.get_string_cards())
        return cards


class Board:
    def __init__(self) -> None:
        self.__board = []
        self.__phase = 0

    def incriment_phase(self) -> None:
        self.__phase += 1

    def draw_flop(self, deck: Deck) -> None:
        '''
        Burns a card from "deck" and
        sets flop to 3 random cards
        '''
        deck.r_draw_card()
        self.__board[0:3] = deck.r_draw_cards(3)

    def draw_turn(self, deck: Deck) -> None:
        deck.r_draw_card() # burn card
        self.__board.append(deck.r_draw_card())

    def draw_river(self, deck: Deck) -> None:
        deck.r_draw_card() # burn card
        self.__board.append(deck.r_draw_card())

    def get_board(self) -> list[Card]:
        '''
        Returns all Cards, which are currently
        a part of the board
        '''
        return self.__board