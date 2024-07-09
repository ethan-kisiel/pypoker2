from models.game_objects import Board, Deck

d = Deck()
b = Board()

b.draw_flop(d)

print(b.get_board())