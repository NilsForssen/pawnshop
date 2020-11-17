# Classic_Test.py

if __name__ == '__main__' and __package__ is None:
    from os import sys, path
    sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))

from ChessBoard import initClassic
from Pieces import *
from Exceptions import *
from ChessVector import ChessVector


board = initClassic()

print(board)


def move(start, target, **kwargs):
    print(board.movePiece(ChessVector(start, board), ChessVector(target, board), **kwargs))


print(board)

move("g2", "g3")
move("f1", "g2")
move("g1", "f3")
move("d2", "d4")
move("d1", "d3")
move("c1", "d2")
move("b1", "c3")

print(board)

print(board[ChessVector("e1", board=board)].getStandardMoves)

move("e1", "g1")
