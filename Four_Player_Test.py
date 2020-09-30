from ChessBoard import Board, init_4P
from StandardSetups import four_player_pieces
from Moves import Castle_K, Castle_Q, _Standard, En_Passant
from Utils import toChessPosition
from Exceptions import *

board = init_4P(_Standard, Castle_K, Castle_Q, En_Passant)
board.pieceSetup(four_player_pieces.items())

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

move("b5", "d5")
print(board)