# formatPGN.py

from ChessBoard import initClassic
from ChessVector import ChessVector


def toPGN(historyList, **kwargs):
    pass


def toChessBoard(PGNString):
    board = initClassic()


def readable(historyList, players=2):
    finalString = ""
    i = 0
    while i * players < len(historyList):
        i += 1
        finalString += str(i) + ". " + " - ".join(historyList[(i - 1) * players:i * players:1]) + "\n"
    return finalString
