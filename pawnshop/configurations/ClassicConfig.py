# ClassicConfig.py

from pawnshop.Pieces import *
from pawnshop.ChessVector import ChessVector
from pawnshop.Moves import *

_colors = ("black", "white")
_black, _white = _colors
_classicPieces = {
    Rook(_black): ChessVector((0, 0)),
    Knight(_black): ChessVector((0, 1)),
    Bishop(_black): ChessVector((0, 2)),
    Queen(_black): ChessVector((0, 3)),
    King(_black): ChessVector((0, 4)),
    Bishop(_black): ChessVector((0, 5)),
    Knight(_black): ChessVector((0, 6)),
    Rook(_black): ChessVector((0, 7)),
    Pawn(_black, "down"): ChessVector((1, 0)),
    Pawn(_black, "down"): ChessVector((1, 1)),
    Pawn(_black, "down"): ChessVector((1, 2)),
    Pawn(_black, "down"): ChessVector((1, 3)),
    Pawn(_black, "down"): ChessVector((1, 4)),
    Pawn(_black, "down"): ChessVector((1, 5)),
    Pawn(_black, "down"): ChessVector((1, 6)),
    Pawn(_black, "down"): ChessVector((1, 7)),

    Rook(_white): ChessVector((7, 0)),
    Knight(_white): ChessVector((7, 1)),
    Bishop(_white): ChessVector((7, 2)),
    Queen(_white): ChessVector((7, 3)),
    King(_white): ChessVector((7, 4)),
    Bishop(_white): ChessVector((7, 5)),
    Knight(_white): ChessVector((7, 6)),
    Rook(_white): ChessVector((7, 7)),
    Pawn(_white, "up"): ChessVector((6, 0)),
    Pawn(_white, "up"): ChessVector((6, 1)),
    Pawn(_white, "up"): ChessVector((6, 2)),
    Pawn(_white, "up"): ChessVector((6, 3)),
    Pawn(_white, "up"): ChessVector((6, 4)),
    Pawn(_white, "up"): ChessVector((6, 5)),
    Pawn(_white, "up"): ChessVector((6, 6)),
    Pawn(_white, "up"): ChessVector((6, 7))
}

for piece, vector in _classicPieces.items():
    piece.vector = vector

_pieceDict = {color: [piece for piece in _classicPieces.keys() if piece.color == color] for color in _colors}
_moveDict = {color: [Standard, CastleK, CastleQ, EnPassant] for color in _colors}
_promoteToDict = {color: [Queen, Rook, Knight, Bishop] for color in _colors}
_promoteFromDict = {color: [Pawn] for color in _colors}
_promoteAtDict = {color: 8 for color in _colors}

CONFIG = {
    "rows": 8,
    "cols": 8,
    "pieces": _pieceDict,
    "moves": _moveDict,
    "promoteTo": _promoteToDict,
    "promoteFrom": _promoteFromDict,
    "promoteAt": _promoteAtDict,
    "turnorder": ["white", "black"]
}

if __name__ == "__main__":
    print(CONFIG)
