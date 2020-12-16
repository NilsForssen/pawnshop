# GmaNotations.py
import re
from copy import deepcopy
from ChessBoard import initClassic, Board
from configurations import ClassicConfig
from ChessVector import ChessVector
from Pieces import *
from Utils import toAlpha
from Moves import CastleK, CastleQ


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


def board2PGN(board, **tags):
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


def PGN2Board(PGNString):
    notations = re.finditer(r"\s*(?P<castleQ>O-O-O)|(?P<castleK>O-O)|(?P<piece>[A-Z]*)(?P<pcol>[a-h]?)(?P<capture>[x]?)(?P<col>[a-h]+)(?P<rank>\d+)=?(?P<promote>[A-Z]?)\+*\#?", PGNString)
    pTypes = dict(zip(map(lambda pt: pt.notation, [Pawn, Rook, Knight, Bishop, King, Queen]), [Pawn, Rook, Knight, Bishop, King, Queen]))

    board = initClassic()
    for i, notation in enumerate(notations):
        color = ["white", "black"][i % 2 == 1]
        if (not notation.group("castleK") is None) or (not notation.group("castleQ") is None):
            for king in board.kings[color]:
                for move in board.moves[color]:
                    if ((not notation.group("castleK") is None) and move is CastleK) or ((not notation.group("castleQ") is None) and move is CastleQ):
                        board.movePiece(king.vector, move.getDestinations(king, board).pop(), checkMove=False, ignoreMate=True, checkForCheck=False, printOut=False)
                        break
                else:
                    continue
                break
        else:
            for piece in board.pieces[color]:
                vector = ChessVector(notation.group("col") + notation.group("rank"), board)
                if vector.matches(piece.getMoves(board)):
                    pType = pTypes[notation.group("piece")]
                    if isinstance(piece, pType):
                        if notation.group("pcol") == "" or notation.group("pcol") == toAlpha(piece.vector.col):
                            board.movePiece(piece.vector, vector, checkMove=False, promote=pTypes[notation.group("promote")], ignoreMate=True, checkForCheck=False, printOut=False)
                            break
                        else:
                            continue
                    else:
                        continue

    board.checkForCheck()
    return board


def FEN2Board(FENString):
    board = Board()
    config = deepcopy(ClassicConfig.CONFIG)
    board.setup(config)


def board2FEN(board):
    pass


def readable(historyList, players=2):
    finalString = ""
    i = 0
    while i * players < len(historyList):
        i += 1
        finalString += str(i) + ". " + " - ".join(historyList[(i - 1) * players:i * players:1]) + "\n"
    return finalString.strip()


if __name__ == "__main__":

    # Do some testing
    pass
