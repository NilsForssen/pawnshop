# Utils.py

from string import ascii_lowercase


def _catchOutofBounce(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except IndexError:
            return False
    return wrapper


def _positivePos(func):
    def wrapper(pInstance, vector, bInstance):
        if not vector.row < 0 and not vector.col < 0:
            return func(pInstance, vector, bInstance)
        else:
            return False
    return wrapper


def removeDupes(vectorList):
    for i, superVec in enumerate(vectorList):
        if superVec.matches(vectorList[i + 1::]):
            vectorList.remove(superVec)
            return removeDupes(vectorList)
    else:
        return vectorList


def createNotation(board, startPiece, targetVec, isPawn=False, capture=False):
    notation = ""
    targetNot = targetVec.getStr(board)

    if not isPawn:
        notation = startPiece.symbol
        for piece in board.iterPieces(startPiece.color):
            if not piece is startPiece and isinstance(piece, type(startPiece)):
                if targetVec.matches(piece.getMoves(board, ignoreCheck=True)):
                    if piece.vector.col == startPiece.vector.col:
                        notation += invertIdx(startPiece.vector.row, board)
                    else:
                        notation += toAlpha(startPiece.vector.col)
                    break
    elif capture:
        notation = toAlpha(startPiece.vector.col)

    if capture:
        notation += "x"

    notation += targetNot
    return notation


def countAlpha():
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


def inverseIdx(num, board):
    return str(board.getRows() - num)


def toAlpha(num):
    for n, notation in countAlpha():
        if num == n:
            return notation


if __name__ == "__main__":

    # Do some testing
    pass
