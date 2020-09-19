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
	raise UnsuccessfulTest
except Check:
	print("Test Success")

board.movePiece((3,3), (1,2))

try:
    board.movePiece((4,7), (6,5))
    raise UnsuccessfulTest
except Check:
    print("Test Success")

try:

    board.movePiece((1,1), (2,1))
    raise UnsuccessfulTest
except Check:
    print("Test Success")

board.movePiece((0,4), (0,3))

board.movePiece((1,2), (0,0))

board.movePiece((0,5), (3,2))

board.movePiece((0,0), (2,1))

try:
    board.movePiece((1,1), (2,1))
    raise UnsuccessfulTest
except IllegalMove:
    print("Test Success")

board.movePiece((1,0), (2,1))

board.movePiece((4,7), (6,5))

try:
    board.movePiece((7,4), (6,5))
    raise UnsuccessfulTest
except CheckMate:
    print("Test Success")

# Just some black moves to Castle

board.movePiece((6,3), (4,3), ignoreCheck=True, ignoreMate=True)


board.movePiece((7,3), (5,3), ignoreCheck=True)

board.movePiece((7,2), (5,4), ignoreCheck=True)

board.movePiece((7,4), (7,0), ignoreCheck=True)

print(board)
