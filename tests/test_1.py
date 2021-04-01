# test_1.py

from pawnshop.ChessVector import ChessVector
from pawnshop.ChessBoard import initClassic
from pawnshop.Exceptions import IllegalMove, CheckMate
from pawnshop.GameNotations import board2FEN
from pawnshop.Pieces import Queen


board = initClassic()


class UnsuccessfulTest(Exception):
    pass


def move(start, target, **kwargs):
    board.movePiece(ChessVector(start, board), ChessVector(target, board), printout=False, **kwargs)


def test_moves():
    movelist = [
        ("a2", "a3"),
        ("e7", "e5"),
        ("b1", "c3"),
        ("d7", "d5"),
        ("c3", "d5"),
        ("d8", "h4")
    ]
    for m in movelist:
        move(*m)

    try:
        move("f2", "f4")
        raise UnsuccessfulTest
    except IllegalMove:
        pass

    move("d5", "c7")

    try:
        move("h4", "f2")
        raise UnsuccessfulTest
    except IllegalMove:
        pass

    try:
        move("b7", "b6")
        raise UnsuccessfulTest
    except IllegalMove:
        pass

    movelist = [
        ("e8", "d8"),
        ("c7", "a8"),
        ("f8", "c5"),
        ("a8", "b6")
    ]

    for m in movelist:
        move(*m)

    try:
        move("b7", "b6")
        raise UnsuccessfulTest
    except IllegalMove:
        pass

    move("a7", "b6")

    move("h4", "f2", ignoreOrder=True)

    try:
        move("e1", "f2", ignoreOrder=True)
        raise UnsuccessfulTest
    except CheckMate:
        pass

    move("d2", "d4", ignoreCheck=True, ignoreOrder=True, ignoreMate=True)
    move("d1", "d3", ignoreCheck=True)
    move("c1", "e3", ignoreCheck=True, ignoreOrder=True)

    try:
        move("e1", "a1")
        raise UnsuccessfulTest
    except IllegalMove:
        pass

    move("f2", "f5", ignoreOrder=True)
    move("f5", "d3", ignoreOrder=True)

    try:
        move("e1", "a1")
        raise UnsuccessfulTest
    except IllegalMove:
        pass

    move("d3", "f5", ignoreOrder=True)
    move("e1", "c1", ignoreOrder=True)
    move("d4", "e5")
    move("g8", "h6", ignoreCheck=True)

    try:
        move("d8", "h8", ignoreCheck=True, ignoreOrder=True)
        raise UnsuccessfulTest
    except IllegalMove:
        pass

    try:
        move("d8", "d7", ignoreOrder=True)
        raise UnsuccessfulTest
    except IllegalMove:
        pass

    move("d8", "e7", ignoreOrder=True)
    move("f5", "h5")
    move("f7", "f5", ignoreOrder=True)
    move("e5", "f6", ignoreOrder=True)
    move("e7", "e8", ignoreOrder=True)
    move("f6", "f7", ignoreOrder=True)
    move("f7", "f8", promote=Queen)
    move("e8", "f8")

    print(board)


def test_FEN():
    assert board2FEN(board) == "1nb2k1r/1p4pp/1p5n/2b4q/8/P3B3/1PP1P1PP/2KR1BNR"
