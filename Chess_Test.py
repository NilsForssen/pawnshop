from Pieces import *
from StandardSetups import *
from Exceptions import *


board = classic()

board.movePiece((1,3), (3,3))

board.movePiece((7,1), (5,2))

board.movePiece((1,4), (3,4))

board.movePiece((5,2), (3,3))

board.movePiece((0,3), (4,7))

try:
	board.movePiece((6,5), (4,5))
	raise UnsucessfulTest
except Check:
	print("Test Success")

print(board)
