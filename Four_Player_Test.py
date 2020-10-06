from StandardSetups import fourPlayer
from Utils import toChessPosition
from Exceptions import *

board = fourPlayer()

def move(start, target, **kwargs):
    print(board.movePiece(toChessPosition(start, board), toChessPosition(target, board), **kwargs))

move("f2", "f3")

move("g2", "g3")

move("g1", "g2")

move("b6", "c6")

move("m7", "l7")

move("n7", "m7")

move("h2", "h3")

move("g2", "g1")

move("b5", "c5")

print(board)