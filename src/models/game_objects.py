from random import randint as ri

from constants import FACES
from constants import VALUES
from constants import CardFaces

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
    
    @property
    def as_dict(self):
        return {'face': self.__face, 'value': self.__value}

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
    __cards: list[Card]
    def __init__(self) -> None:
        self.__cards = []


    def draw_flop(self, deck: Deck) -> None:
        '''
        Burns a card from "deck" and
        sets flop to 3 random cards
        '''
        deck.r_draw_card()
        self.__cards[0:3] = deck.r_draw_cards(3)

    def draw_turn(self, deck: Deck) -> None:
        deck.r_draw_card() # burn card
        self.__cards.append(deck.r_draw_card())

    def draw_river(self, deck: Deck) -> None:
        deck.r_draw_card() # burn card
        self.__cards.append(deck.r_draw_card())

    @property
    def cards(self) -> list[Card]:
        '''
        Returns all Cards, which are currently
        a part of the board
        '''
        return self.__cards
    


# class CardSlot:
#     index: int
#     card: Card

#     next = None
#     prev = None

#     def __init__(self, index: int, card: Card, next=None, prev=None):
#         self.index = index
#         self.card = card
        
#         self.next = next
#         self.prev = prev


class HandScorer:
    cards: list[Card]

    def __init__(self, hand: list[Card], board: list[Card]):
        combined_cards = hand + board
        combined_cards.sort()
        
        self.cards = combined_cards

        self.clubs =  [card for card in self.cards if card.get_face() == CardFaces.CLUBS.value]
        self.diamonds = [card for card in self.cards if card.get_face() == CardFaces.DIAMONDS.value]
        self.hearts = [card for card in self.cards if card.get_face() == CardFaces.HEARTS.value]
        self.spades = [card for card in self.cards if card.get_face() == CardFaces.SPADES.value]
        
        self.sets = {}
        for card in self.cards:
            card_val = card.get_value()
            
            if self.sets.get(card_val) is None:
                self.sets[card_val] = [card]
            else:
                self.sets[card_val].append(card)


    def cards_increase_by_one(self, cards: list[Card]):
        for i, card in enumerate(cards):
            if i == len(cards) - 1:
                return True

            if cards[i+1].get_points_value() - card.get_points_value() == 1:
                pass
            else:
                return False

    @property
    def royal_flush(self):
        pass


    @property
    def flush(self):
        '''
        only returns the highest flush
        '''
        flush_cards = []
        if len(self.clubs) >= 5:
            start = len(self.clubs)-5
            flush_cards = self.clubs[start:]

        if len(self.diamonds) >= 5:
            start = len(self.diamonds)-5
            flush_cards = self.diamonds[start:]

        if len(self.hearts) >= 5:
            start = len(self.hearts)-5
            flush_cards = self.hearts[start:]

        if len(self.spades) >= 5:
            start = len(self.spades)-5
            flush_cards = self.spades[start:]

        return flush_cards

    @property
    def straight(self):
        straight_cards = []
        normalized_cards = list(set(self.cards)) # get a list of only cards with different values
        normalized_cards.sort()

        if len(normalized_cards) < 5:
            # not enough cards for there to be a straight
            return straight_cards

        start = len(normalized_cards) - 5

        while start >= 0:
            stop = start+5

            if stop < len(normalized_cards):
                cards_to_search = normalized_cards[start:stop]
            else:
                cards_to_search = normalized_cards[start:]

            if self.cards_increase_by_one(cards_to_search):
                return cards_to_search

            start -= 1
        else:
            # check for 5 high straight
            if (self.cards_increase_by_one(normalized_cards[0:4]) 
                and normalized_cards[-1].get_points_value() == 13):
                straight_cards.append(normalized_cards[-1])
                straight_cards += normalized_cards[0:4]
        
        return straight_cards