from pawnshop.ChessBoard import initClassic
from pawnshop.Pieces import *
from pawnshop.Exceptions import *
from pawnshop.ChessVector import ChessVector


board = initClassic()

print(board)


def move(start, target, **kwargs):
    board.movePiece(ChessVector(start, board), ChessVector(target, board), **kwargs)


# print(board.movePiece((6,0), (5,0)))
move("a2", "a3")

# print(board.movePiece((1,3), (3,3)))
move("e7", "e5")

# print(board.movePiece((7,1), (5,2)))
move("b1", "c3")

# print(board.movePiece((1,4), (3,4)))
move("d7", "d5")

# print(board.movePiece((5,2), (3,3)))
move("c3", "d5")

# print(board.movePiece((0,3), (4,7)))
move("d8", "h4")

try:
    # board.movePiece((6,5), (4,5))
    move("f2", "f4")
    raise UnsuccessfulTest
except IllegalMove:
    print("Test Success")

# print(board.movePiece((3,3), (1,2)))
move("d5", "c7")

try:
    # board.movePiece((4,7), (6,5))
    move("h4", "f2")
    raise UnsuccessfulTest
except IllegalMove:
    print("Test Success")

try:
    # board.movePiece((1,1), (2,1))
    move("b7", "b6")
    raise UnsuccessfulTest
except IllegalMove:
    print("Test Success")

# print(board.movePiece((0,4), (0,3)))
move("e8", "d8")

# print(board.movePiece((1,2), (0,0)))
move("c7", "a8")

# print(board.movePiece((0,5), (3,2)))
move("f8", "c5")

# print(board.movePiece((0,0), (2,1)))
move("a8", "b6")

try:
    # board.movePiece((1,1), (2,1))
    move("b7", "b6")
    raise UnsuccessfulTest
except IllegalMove:
    print("Test Success")

# print(board.movePiece((1,0), (2,1)))
move("a7", "b6")

# print(board.movePiece((4,7), (6,5)))
move("h4", "f2", ignoreOrder=True)

try:
    # board.movePiece((7,4), (6,5))
    move("e1", "f2", ignoreOrder=True)
    raise UnsuccessfulTest
except CheckMate:
    print("Test Success")

# Just some white moves to Castle
# print(board.movePiece((6,3), (4,3), ignoreCheck=True, ignoreMate=True))
move("d2", "d4", ignoreOrder=True, ignoreCheck=True, ignoreMate=True)

# print(board.movePiece((7,3), (5,3), ignoreCheck=True))
move("d1", "d3", ignoreCheck=True)

# print(board.movePiece((7,2), (5,4), ignoreCheck=True))
move("c1", "e3", ignoreCheck=True, ignoreOrder=True)

try:
    # print(board.movePiece((7,4), (7,0)))
    move("e1", "a1")
    raise UnsuccessfulTest
except IllegalMove:
    print("Test Success")

# print(board.movePiece((6,5), (3,5)))
move("f2", "f5", ignoreOrder=True)

# print(board.movePiece((3,5), (5,3)))
move("f5", "d3")

try:
    # print(board.movePiece((7,4), (7,0)))
    move("e1", "a1")
    raise UnsuccessfulTest
except IllegalMove:
    print("Test Success")

# print(board.movePiece((5,3), (3,5)))
move("d3", "f5", ignoreOrder=True)

# print(board.movePiece((7,4), (7,0)))
move("e1", "c1", ignoreOrder=True)

move("d4", "e5")

move("g8", "h6", ignoreCheck=True)

try:
    move("d8", "h8", ignoreCheck=True, ignoreOrder=True )
    raise UnsuccessfulTest
except IllegalMove:
    print("Test Success")

try:
    move("d8", "d7", ignoreOrder=True)
    raise UnsuccessfulTest
except IllegalMove:
    print("Test Success")

move("d8", "e7", ignoreOrder=True)

move("f5", "h5")

move("f7", "f5", ignoreOrder=True)

move("e5", "f6", ignoreOrder=True)

move("e7", "e8", ignoreOrder=True)

move("f6", "f7", ignoreOrder=True)

move("f7", "f8", promote=Queen)

move("e8", "f8")

print(board)
