# Four_Player_Test.py

if __name__ == '__main__' and __package__ is None:
    from os import sys, path
    sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))

from ChessBoard import init4P
from ChessVector import ChessVector


board = init4P()


def move(start, target, **kwargs):
    board.movePiece(ChessVector(start, board), ChessVector(target, board), **kwargs)


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
