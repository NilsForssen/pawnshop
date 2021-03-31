# Utils.py

from typing import List, Generator
from string import ascii_lowercase
from .ChessVector import ChessVector
from .ChessBoard import Board
from .Piece import Piece


def _catchOutofBounce(func):
    """Decorator for catching out of bounce ´´IndexError´´"""
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except IndexError:
            return False
    return wrapper



def _positivePos(func):
    """Decorator for ensuring a position is not negative"""
    def wrapper(pInstance, vector, bInstance, *args, **kwargs):
        if not vector.row < 0 and not vector.col < 0:
            return func(pInstance, vector, bInstance, *args, **kwargs)
        else:
            return False
    return wrapper


def removeDupes(vectorList: List[ChessVector]) -> List[ChessVector]:
    """Remove duplicate positions

    :param vectorList: List to remove duplicates from
    :returns: List without duplicates
    :rtype: ``list``
    """
    for i, superVec in enumerate(vectorList):
        if superVec.matches(vectorList[i + 1::]):
            vectorList.remove(superVec)
            return removeDupes(vectorList)
    else:
        return vectorList


def createNotation(board: Board, startPiece: Piece, targetVec: ChessVector, isPawn=False, capture=False) -> str:
    """Create a notation for a move

    Creates notation of move according to standard chess notation.

    :param startPiece: Piece to be moved
    :param targetVec: Destination of move
    :param **Flags: Flags to create notation
    :returns: Notation of move
    :rtype: ``str``

    :**Flags:
        :isPawn (True):
        :capture (True):
    """
    notation = ""
    targetNot = targetVec.getStr(board)

    if not isPawn:
        notation = startPiece.symbol
        for piece in board.iterPieces(startPiece.color):
            if piece is not startPiece and isinstance(piece, type(startPiece)):
                if targetVec.matches(piece.getMoves(board, ignoreCheck=True)):
                    if piece.vector.col == startPiece.vector.col:
                        notation += inverseIdx(startPiece.vector.row, board)
                    else:
                        notation += toAlpha(startPiece.vector.col)
                    break
    elif capture:
        notation = toAlpha(startPiece.vector.col)

    if capture:
        notation += "x"

    notation += targetNot
    return notation


def countAlpha() -> Generator[str]:
    """Generator to count in alphabetical order

    Counts in alphabetical order.
    a->b->c->...->aa->ab->...->ba->...

    :yields: Character
    :ytype: ``generator``
    """
    stringList = [0]
    num = 0
    while True:
        yield (num, "".join([ascii_lowercase[num] for num in stringList]))
        i = 1
        num += 1

        while True:
            if i > len(stringList):
                stringList.insert(0, 0)
                break
            else:
                changeTo = stringList[-i] + 1
            if changeTo >= len(ascii_lowercase):
                stringList[-i::] = [0] * (i)
                i += 1
                continue
            else:
                stringList[-i] = changeTo
                break


def inverseIdx(idx: int, board: Board) -> str:
    """Inverse index

    Inverses idx given board rows and returns string

    :param idx: Index to reverse
    :param board: Board to reverse according to rows
    :returns: Reversed index
    :rtype: ``str``
    """
    return str(board.getRows() - idx)


def toAlpha(num: int) -> str:
    """Convert number to alphabetical

    Counts through all alpha until reaching number.
    (I tried to make it not have to count through all alphas,
    however, since my alpha system doesn't match any regular
    base number system I was not able to.)

    :param num: Number to convert
    :returns: Alphabetical string from num
    :rtype: str
    """
    for n, notation in countAlpha():
        if num == n:
            return notation

if __name__ == "__main__":
    # Do some testing

    pass
