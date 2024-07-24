from models.game_objects import Board, Deck, HandScorer, Card

d = Deck()
b = Board()


hand = ["c_2","d_3"]

board = ["c_4", "d_5", "h_6", "s_7", "c_8"]


board = [Card(0, 0, card) for card in board]
hand = [Card(0, 0, card) for card in hand]
hs = HandScorer(hand, board)

print(hs.flush)
print(hs.score)
print(hs.straights)