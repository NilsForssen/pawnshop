from .Pieces import *
from .Moves import *
from .ChessVector import ChessVector

_colors = ("yellow", "green", "red", "blue")
_yellow, _green, _red, _blue = _colors

_fourPlayerPieces = {
    Rook(_yellow): ChessVector((0, 3)),
    Knight(_yellow): ChessVector((0, 4)),
    Bishop(_yellow): ChessVector((0, 5)),
    Queen(_yellow): ChessVector((0, 6)),
    King(_yellow): ChessVector((0, 7)),
    Bishop(_yellow): ChessVector((0, 8)),
    Knight(_yellow): ChessVector((0, 9)),
    Rook(_yellow): ChessVector((0, 10)),
    Pawn(_yellow, "down"): ChessVector((1, 3)),
    Pawn(_yellow, "down"): ChessVector((1, 4)),
    Pawn(_yellow, "down"): ChessVector((1, 5)),
    Pawn(_yellow, "down"): ChessVector((1, 6)),
    Pawn(_yellow, "down"): ChessVector((1, 7)),
    Pawn(_yellow, "down"): ChessVector((1, 8)),
    Pawn(_yellow, "down"): ChessVector((1, 9)),
    Pawn(_yellow, "down"): ChessVector((1, 10)),

    Rook(_green): ChessVector((3, 13)),
    Knight(_green): ChessVector((4, 13)),
    Bishop(_green): ChessVector((5, 13)),
    Queen(_green): ChessVector((6, 13)),
    King(_green): ChessVector((7, 13)),
    Bishop(_green): ChessVector((8, 13)),
    Knight(_green): ChessVector((9, 13)),
    Rook(_green): ChessVector((10, 13)),
    Pawn(_green, "left"): ChessVector((3, 12)),
    Pawn(_green, "left"): ChessVector((4, 12)),
    Pawn(_green, "left"): ChessVector((5, 12)),
    Pawn(_green, "left"): ChessVector((6, 12)),
    Pawn(_green, "left"): ChessVector((7, 12)),
    Pawn(_green, "left"): ChessVector((8, 12)),
    Pawn(_green, "left"): ChessVector((9, 12)),
    Pawn(_green, "left"): ChessVector((10, 12)),

    Rook(_red): ChessVector((13, 3)),
    Knight(_red): ChessVector((13, 4)),
    Bishop(_red): ChessVector((13, 5)),
    Queen(_red): ChessVector((13, 6)),
    King(_red): ChessVector((13, 7)),
    Bishop(_red): ChessVector((13, 8)),
    Knight(_red): ChessVector((13, 9)),
    Rook(_red): ChessVector((13, 10)),
    Pawn(_red, "up"): ChessVector((12, 3)),
    Pawn(_red, "up"): ChessVector((12, 4)),
    Pawn(_red, "up"): ChessVector((12, 5)),
    Pawn(_red, "up"): ChessVector((12, 6)),
    Pawn(_red, "up"): ChessVector((12, 7)),
    Pawn(_red, "up"): ChessVector((12, 8)),
    Pawn(_red, "up"): ChessVector((12, 9)),
    Pawn(_red, "up"): ChessVector((12, 10)),

    Rook(_blue): ChessVector((3, 0)),
    Knight(_blue): ChessVector((4, 0)),
    Bishop(_blue): ChessVector((5, 0)),
    Queen(_blue): ChessVector((6, 0)),
    King(_blue): ChessVector((7, 0)),
    Bishop(_blue): ChessVector((8, 0)),
    Knight(_blue): ChessVector((9, 0)),
    Rook(_blue): ChessVector((10, 0)),
    Pawn(_blue, "right"): ChessVector((3, 1)),
    Pawn(_blue, "right"): ChessVector((4, 1)),
    Pawn(_blue, "right"): ChessVector((5, 1)),
    Pawn(_blue, "right"): ChessVector((6, 1)),
    Pawn(_blue, "right"): ChessVector((7, 1)),
    Pawn(_blue, "right"): ChessVector((8, 1)),
    Pawn(_blue, "right"): ChessVector((9, 1)),
    Pawn(_blue, "right"): ChessVector((10, 1))
}
_disabled = [
    ChessVector((0, 0)),
    ChessVector((0, 1)),
    ChessVector((0, 2)),
    ChessVector((1, 0)),
    ChessVector((1, 1)),
    ChessVector((1, 2)),
    ChessVector((2, 0)),
    ChessVector((2, 1)),
    ChessVector((2, 2)),
    ChessVector((0, 11)),
    ChessVector((0, 12)),
    ChessVector((0, 13)),
    ChessVector((1, 11)),
    ChessVector((1, 12)),
    ChessVector((1, 13)),
    ChessVector((2, 11)),
    ChessVector((2, 12)),
    ChessVector((2, 13)),
    ChessVector((11, 0)),
    ChessVector((11, 1)),
    ChessVector((11, 2)),
    ChessVector((12, 0)),
    ChessVector((12, 1)),
    ChessVector((12, 2)),
    ChessVector((13, 0)),
    ChessVector((13, 1)),
    ChessVector((13, 2)),
    ChessVector((11, 11)),
    ChessVector((11, 12)),
    ChessVector((11, 13)),
    ChessVector((12, 11)),
    ChessVector((12, 12)),
    ChessVector((12, 13)),
    ChessVector((13, 11)),
    ChessVector((13, 12)),
    ChessVector((13, 13))
]
for piece, vector in _fourPlayerPieces.items():
    piece.vector = vector

_pieceDict = {color: [piece for piece in _fourPlayerPieces.keys() if piece.color == color] for color in _colors}
_moveDict = {color: [Standard, CastleK, CastleQ] for color in _colors}
_promoteToDict = {color: [Queen, Rook, Knight, Bishop] for color in _colors}
_promoteFromDict = {color: [Pawn] for color in _colors}
_promoteAtDict = {color: 8 for color in _colors}

CONFIG = {
    "rows": 14,
    "cols": 14,
    "pieces": _pieceDict,
    "moves": _moveDict,
    "promoteTo": _promoteToDict,
    "promoteFrom": _promoteFromDict,
    "promoteAt": _promoteAtDict,
    "disabled": _disabled,
    "turnorder": ["red", "blue", "yellow", "green"]
}

if __name__ == "__main__":
    print(CONFIG)
