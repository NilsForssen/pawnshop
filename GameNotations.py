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
                        board.movePiece(king.vector, move.getDestinations(king, board).pop(), checkMove=False, ignoreMate=True, checkForCheck=False)
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
                            board.movePiece(piece.vector, vector, checkMove=False, promote=pTypes[notation.group("promote")], ignoreMate=True, checkForCheck=False)
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
    print(
        PGN2Board(
            """[Event "India-China Summit Match"]
[Site "Hyderabad IND"]
[Date "2015.03.04"]
[EventDate "2015.03.02"]
[Round "3.1"]
[Result "1-0"]
[White "Baskaran Adhiban"]
[Black "Wei Yi"]
[ECO "B97"]
[WhiteElo "2646"]
[BlackElo "2706"]
[PlyCount "49"]

1. e4 c5 2. Nf3 d6 3. d4 cxd4 4. Nxd4 Nf6 5. Nc3 a6 6. Bg5 e6
7. f4 Qb6 8. Qd3 Qxb2 9. Rb1 Qa3 10. Be2 Nbd7 11. O-O Be7
12. Kh1 h6 13. Qh3 Qc5 14. Rbd1 Qc7 15. Bh4 Nc5 16. Bxf6 Bxf6
17. e5 dxe5 18. Ndb5 axb5 19. Nxb5 Qb6 20. Nd6+ Ke7 21. fxe5
Nd7 22. exf6+ Nxf6 23. Qg3 Kf8 24. Nxf7 Kxf7 25. Bh5+"""
        ))
    # Do some testing
    pass
