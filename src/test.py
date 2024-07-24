from models.game_objects import Board, Deck, HandScorer, Card

d = Deck()
b = Board()


hand = ["c_A","c_2"]

board = ["c_3", "c_4", "c_5", "c_J", "c_10"]


board = [Card(0, 0, card) for card in board]
hand = [Card(0, 0, card) for card in hand]
hs = HandScorer(hand, board)

print(hs.flush)
print(hs.straight)