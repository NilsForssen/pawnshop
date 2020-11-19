# Utils.py

import sys
import os
from string import ascii_lowercase
from PIL import Image


def getResourcePath(filePath, relativePath):
    """Get resource

    More reliable when script is compiled with pyinstaller.
    """
    resourcePath = os.path.join(os.path.dirname(os.path.abspath(filePath)), relativePath)
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, resourcePath)

    return os.path.join(os.path.abspath("."), resourcePath)


def fetchImage(color, imgpath):
    """Fetch image from disk"""
    img = Image.open(imgpath)
    pixels = img.load()
    fullGreen = 255
    r, g, b = color
    for x in range(img.height):
        for y in range(img.width):
            _, greenVal, _, alpha = pixels[x, y]
            if greenVal:
                ratio = greenVal / fullGreen
                pixels[x, y] = (round(r * ratio), round(g * ratio), round(b * ratio), alpha)
    return img


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


def unpackIndexSlices(idx):
    try:
        r, c = idx
    except (TypeError, ValueError):
        raise ValueError("Index position must be 2-dimensional.") from None

    if type(r) is not slice:
        r = slice(r, r + 1)
    if type(c) is not slice:
        c = slice(c, c + 1)

    return r, c


def createNotation(board, startPiece, targetVec, isPawn=False, capture=False):
    notation = ""
    targetNot = targetVec.getStr(board)

    if not isPawn:
        notation = startPiece.symbol
        for piece in board.pieces[startPiece.color]:
            if not piece is startPiece and isinstance(piece, type(startPiece)):
                if targetVec.matches(piece.getMoves(board)):
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
    return str(board.rows - num)


def toAlpha(num):
    for n, notation in countAlpha():
        if num == n:
            return notation


if __name__ == "__main__":

    # Do some testing
    pass
