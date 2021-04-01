# GameNotations.py

import re
from copy import deepcopy

from .ChessBoard import (
    initClassic,
    Board
)
from .configurations import ClassicConfig
from .ChessVector import ChessVector
from .Pieces import *
from .Utils import toAlpha
from .Moves import (
    CastleK,
    CastleQ
)


STANDARDTAGS = [
    "Event",
    "Site",
    "Date",
    "Round",
    "White",
    "Black",
    "Result"
]
OPTIONALTAGS = [
    "Annotator",
    "PlyCount",
    "TimeControl",
    "Time",
    "Termination",
    "Mode",
    "FEN"
]
ALLTAGS = [*STANDARDTAGS, *OPTIONALTAGS]


def board2PGN(board: Board, **tags) -> str:
    """Get Portable Game Notation from board

    :param board: Board to get notation from
    :param **tags: Tags added to the notation
    :returns: PGN string
    :rtype: ``str``

    :**tags: Tags found in STANDARDTAGS and OPTIONALTAGS
    """
    PGNString = ""
    tags = {t.lower(): v for t, v in tags.items()}

    for TAG in ALLTAGS:
        if TAG.lower() in tags:
            PGNString += f"[{TAG} \"{str(tags[TAG.lower()])}\"]\n"
    i = 0
    while i * 2 < len(board.history):
        i += 1
        PGNString += str(i) + ". " + " ".join(board.history[(i - 1) * 2:i * 2:1]) + "\n"

    return PGNString


def PGN2Board(PGNString: str) -> Board:
    """Get Board object from Portable Game Notation

    :param PGNString: PGN string
    :returns: Board object from PGN
    :rtype: ``Board``
    """
    notations = re.finditer(r"\s*(?P<castleQ>O-O-O)|(?P<castleK>O-O)|(?P<piece>[A-Z]*)(?P<pcol>[a-h]?)(?P<capture>[x]?)(?P<col>[a-h]+)(?P<rank>\d+)=?(?P<promote>[A-Z]?)\+*\#?", PGNString)

    board = initClassic()
    for i, notation in enumerate(notations):
        color = ["white", "black"][i % 2 == 1]
        if (not notation.group("castleK") is None) or (not notation.group("castleQ") is None):
            for king in board.kings[color]:
                for move in board.moves[color]:
                    if ((not notation.group("castleK") is None) and move is CastleK) or ((not notation.group("castleQ") is None) and move is CastleQ):
                        board.movePiece(king.vector, move.getDestinations(king, board).pop(), checkMove=False, ignoreMate=True, checkForCheck=False, printOut=False, ignoreOrder=True)
                        break
                else:
                    continue
                break
        else:
            for piece in board.pieces[color]:
                vector = ChessVector(notation.group("col") + notation.group("rank"), board)
                if vector.matches(piece.getMoves(board)):
                    pType = pieceNotations[notation.group("piece")]
                    if isinstance(piece, pType):
                        if notation.group("pcol") == "" or notation.group("pcol") == toAlpha(piece.vector.col):
                            board.movePiece(piece.vector, vector, checkMove=False, promote=pieceNotations[notation.group("promote")], ignoreMate=True, checkForCheck=False, printOut=False, ignoreOrder=True)
                            break
                        else:
                            continue
                    else:
                        continue

    board.checkForCheck()
    return board


def FEN2Board(FENString: str) -> Board:
    """Get Board object from Forsyth-Edwards-Notation

    :param FENString: Forsyth-Edwards-Notation
    :returns: Board object from FEN
    :rtype: ``Board``
    """
    board = Board()
    config = deepcopy(ClassicConfig.CONFIG)
    del config["pieces"]
    board.setup(config)

    fieldFinder = re.finditer(r"[^ ]+", FENString)
    rowFinder = re.finditer(r"([^/]+)", next(fieldFinder).group())

    for rowi, row in enumerate(rowFinder):
        coli = 0
        for chari, char in enumerate(row.group(0)):
            if char.isnumeric():
                for coli in range(coli, coli + int(char)):
                    vector = ChessVector((rowi, coli), board)
                    board[vector] = Empty(vector)
                    coli += 1
            else:
                vector = ChessVector((rowi, coli), board)

                if char.isupper():
                    board[vector] = pieceNotations[char]("white", direction="up")
                elif char.islower():
                    board[vector] = pieceNotations[char.upper()]("black", direction="down")
                coli += 1

    # No other fields are critical, might implement more later
    return board


def board2FEN(board: Board) -> str:
    """Get Forsyth-Edward-Notation from board

    The notation does not account for:
    current turn, castling potential, en-passant or move count
    - only the position is notated (I am lazy)

    :param board: Board to get FEN from
    :returns: FEN string
    :rtype: ``str``
    """
    FENString = ""
    for rowi, row in enumerate(board._board):
        empty = 0
        for coli, piece in enumerate(row):
            if isinstance(piece, Empty) or isinstance(piece, Disabled):
                empty += 1
            else:
                if empty:
                    FENString += str(empty)
                if piece.color == "white":
                    ps = piece.symbol.upper()
                elif piece.color == "black":
                    ps = piece.symbol.lower()
                FENString += ps
                empty = 0

        if empty:
            FENString += str(empty)
        if not rowi == board.getRows() - 1:
            FENString += "/"

    return FENString


def readable(historyList: List[str], players=2) -> str:
    """Get printable format of history

    :param historyList: History to be read
    :param players: How many players the history includes
    :returns: Readable string of history
    :rtype: ``str``
    """
    finalString = ""
    i = 0
    while i * players < len(historyList):
        i += 1
        finalString += str(i) + ". " + " - ".join(historyList[(i - 1) * players:i * players:1]) + "\n"
    return finalString.strip()


if __name__ == "__main__":

    # Do some testing
    pass
