# test_2.py

from pawnshop.ChessBoard import init4P
from pawnshop.ChessVector import ChessVector

board = init4P()

def move(start, target, **kwargs):
    board.movePiece(ChessVector(start, board), ChessVector(target, board), **kwargs)

def test_moves():
    move("f2", "f3")

    move("g2", "g3", ignoreOrder=True)

    move("g1", "g2", ignoreOrder=True)

    move("b6", "c6", ignoreOrder=True)

    move("m7", "l7", ignoreOrder=True)

    move("n7", "m7", ignoreOrder=True)

    move("h2", "h3", ignoreOrder=True)

    move("g2", "g1", ignoreOrder=True)

    move("b5", "c5", ignoreOrder=True)

