from Pieces import *
from StandardSetups import classic_pieces
from Exceptions import *
from ChessBoard import init_classic
from Moves import Castle_K, Castle_Q, _Standard

board = init_classic(_Standard, Castle_K, Castle_Q)
board.pieceSetup(classic_pieces.items())

print(board.movePiece((1,3), (3,3)))

print(board.movePiece((7,1), (5,2)))

print(board.movePiece((1,4), (3,4)))

print(board.movePiece((5,2), (3,3)))

print(board.movePiece((0,3), (4,7)))

try:
	board.movePiece((6,5), (4,5))
	raise UnsuccessfulTest
except Check:
	print("Test Success")

print(board.movePiece((3,3), (1,2)))

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

print(board.movePiece((0,4), (0,3)))

print(board.movePiece((1,2), (0,0)))

print(board.movePiece((0,5), (3,2)))

print(board.movePiece((0,0), (2,1)))

try:
    board.movePiece((1,1), (2,1))
    raise UnsuccessfulTest
except IllegalMove:
    print("Test Success")

print(board.movePiece((1,0), (2,1)))

print(board.movePiece((4,7), (6,5)))

try:
    board.movePiece((7,4), (6,5))
    raise UnsuccessfulTest
except CheckMate:
    print("Test Success")

# Just some black moves to Castle

print(board.movePiece((6,3), (4,3), ignoreCheck=True, ignoreMate=True))

print(board.movePiece((7,3), (5,3), ignoreCheck=True))

print(board.movePiece((7,2), (5,4), ignoreCheck=True))

try:
    print(board.movePiece((7,4), (7,0)))
    raise UnsuccessfulTest
except IllegalMove:
    print("Test Success")

print(board.movePiece((6,5), (3,5)))

print(board.movePiece((3,5), (5,3)))

try:
    print(board.movePiece((7,4), (7,0)))
    raise UnsuccessfulTest
except IllegalMove:
    print("Test Success")

print(board.movePiece((5,3), (3,5)))


print(board.movePiece((7,4), (7,0)))
print(board)
