# GmaNotations.py
from copy import copy, deepcopy
from ChessBoard import initClassic, Board
from configurations import ClassicConfig
from ChessVector import ChessVector

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
    while i * 2 < len(historyList):
        i += 1
        PGNString += str(i) + ". " + " ".join(board.history[(i - 1) * 2:i * 2:1]) + "\n"

    return PGNString


def PGN2Board(PGNString):
    board = initClassic()


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
    return finalString


if __name__ == "__main__":

    # Do some testing
    pass
