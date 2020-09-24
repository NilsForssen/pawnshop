from Exceptions import DisabledError
from string import ascii_lowercase

def _catchOutofBounce(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except IndexError:
            return False
    return wrapper


def _positivePos(func):
    def wrapper(pInstance, pos, bInstance):

        if not pos[0] < 0 and not pos[1] < 0:
            return func(pInstance, pos, bInstance)
        else:
            return False
    return wrapper


def infiRange(start, stop=None, step=1):
    i = start
    while True:
        if stop and stop == i:
            break
        yield i
        i += step


def countAlpha():
    stringList = [0]
    num = 0
    
    while True:

        yield (num, "".join([ascii_lowercase[num] for num in stringList]))
        i = 1
        num += 1 

        while True:

            if i > len(stringList):
                stringList.insert(0,0)
                break
            else:
                charToChange2 = stringList[-i] + 1

            if charToChange2 >= len(ascii_lowercase):
                stringList[-i::] = [0]*(i)
                i += 1 
                continue
            else:

                stringList[-i] = charToChange2
                break


def formatNum(num, board):
    return str(board.rows - num)


def toAlpha(num):
    for n, notation in countAlpha():
        if num == n:
            return notation
            

def createNotation(board, startPiece, startPos, targetPos, isPawn=False, capture=False):

    notation = ""
    targetNot = toChessMetric(targetPos, board)

    if not isPawn:

        notation = startPiece.symbol
        for piece in board.pieceDict[startPiece.color]:
            if not piece is startPiece and isinstance(piece, type(startPiece)):
                if targetPos in piece.getMoves(board):
                    if piece.position[1] == startPos[1]:
                        notation += formatNum(startPos[0], board)
                    else: 
                        notation += toAlpha(startPos[1])
                    break
    elif capture:
        notation = toAlpha(startPos[1])

    if capture:
        notation += "x"

    notation += targetNot

    return notation

            
def toChessMetric(chessPosition, board):
    notation = ""

    notation += toAlpha(chessPosition[1])
    notation += formatNum(chessPosition[0], board)

    return notation


def toChessPosition(chessMetric, board):

    for i, char in enumerate(chessMetric):
        if not char in ascii_lowercase:

            if i == 0: raise ValueError("Chess metric does not include column")
            
            alpha = chessMetric[:i]
            num = chessMetric[i::]

            if not len(num): raise ValueError("Chess metric does not include row")

            row = board.rows - int(num)
            for n, a in countAlpha():
                if a == alpha:
                    col = n
                    break

    return (row, col)