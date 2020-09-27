from ChessBoard import Board, init_4P, init_classic
from Moves import _Standard, Castle_K, Castle_Q
from Pieces import *

classic_pieces = {
    Rook("black"): (0,0),
    Knight("black"): (0,1),
    Bishop("black"): (0,2),
    Queen("black"): (0,3),
    King("black"): (0,4),
    Bishop("black"): (0,5),
    Knight("black"): (0,6),
    Rook("black"): (0,7),
    Pawn("black", "down"): (1,0),
    Pawn("black", "down"): (1,1),
    Pawn("black", "down"): (1,2),
    Pawn("black", "down"): (1,3),
    Pawn("black", "down"): (1,4),
    Pawn("black", "down"): (1,5),
    Pawn("black", "down"): (1,6),
    Pawn("black", "down"): (1,7),

    Rook("white"): (7,0),
    Knight("white"): (7,1),
    Bishop("white"): (7,2),
    Queen("white"): (7,3),
    King("white"): (7,4),
    Bishop("white"): (7,5),
    Knight("white"): (7,6),
    Rook("white"): (7,7),
    Pawn("white", "up"): (6,0),
    Pawn("white", "up"): (6,1),
    Pawn("white", "up"): (6,2),
    Pawn("white", "up"):(6,3),
    Pawn("white", "up"): (6,4),
    Pawn("white", "up"): (6,5),
    Pawn("white", "up"): (6,6),
    Pawn("white", "up"): (6,7)
    }

four_player_pieces = {
    Rook("yellow"): (0,3),
    Knight("yellow"): (0,4),
    Bishop("yellow"): (0,5),
    Queen("yellow"): (0,6),
    King("yellow"): (0,7),
    Bishop("yellow"): (0,8),
    Knight("yellow"): (0,9),
    Rook("yellow"): (0,10),
    Pawn("yellow", "down"): (1,3),
    Pawn("yellow", "down"): (1,4),
    Pawn("yellow", "down"): (1,5),
    Pawn("yellow", "down"): (1,6),
    Pawn("yellow", "down"): (1,7),
    Pawn("yellow", "down"): (1,8),
    Pawn("yellow", "down"): (1,9),
    Pawn("yellow", "down"): (1,10),

    Rook("red"): (13,3),
    Knight("red"): (13,4),
    Bishop("red"): (13,5),
    Queen("red"): (13,6),
    King("red"): (13,7),
    Bishop("red"): (13,8),
    Knight("red"): (13,9),
    Rook("red"): (13,10),
    Pawn("red", "up"): (12,3),
    Pawn("red", "up"): (12,4),
    Pawn("red", "up"): (12,5),
    Pawn("red", "up"): (12,6),
    Pawn("red", "up"): (12,7),
    Pawn("red", "up"): (12,8),
    Pawn("red", "up"): (12,9),
    Pawn("red", "up"): (12,10),

    Rook("green"): (3,13),
    Knight("green"): (4,13),
    Bishop("green"): (5,13),
    Queen("green"): (6,13),
    King("green"): (7,13),
    Bishop("green"): (8,13),
    Knight("green"): (9,13),
    Rook("green"): (10,13),
    Pawn("green", "left"): (3,12),
    Pawn("green", "left"): (4,12),
    Pawn("green", "left"): (5,12),
    Pawn("green", "left"): (6,12),
    Pawn("green", "left"): (7,12),
    Pawn("green", "left"): (8,12),
    Pawn("green", "left"): (9,12),
    Pawn("green", "left"): (10,12),

    Rook("blue"): (3,0),
    Knight("blue"): (4,0),
    Bishop("blue"): (5,0),
    Queen("blue"): (6,0),
    King("blue"): (7,0),
    Bishop("blue"): (8,0),
    Knight("blue"): (9,0),
    Rook("blue"): (10,0),
    Pawn("blue", "right"): (3,1),
    Pawn("blue", "right"): (4,1),
    Pawn("blue", "right"): (5,1),
    Pawn("blue", "right"): (6,1),
    Pawn("blue", "right"): (7,1),
    Pawn("blue", "right"): (8,1),
    Pawn("blue", "right"): (9,1),
    Pawn("blue", "right"): (10,1)
    }

def classic():

    board = init_classic(_Standard, Castle_K, Castle_Q)

    board.pieceSetup(classic_pieces.items())

    return board


def four_player():

    board = init_4P(_Standard, Castle_K, Castle_Q)

    board.pieceSetup(four_player_pieces)

    return board 

if __name__ == "__main__":

    # Do some testing
    pass