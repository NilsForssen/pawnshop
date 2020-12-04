# ChessBoard.py

import json
from copy import deepcopy, copy
from Utils import getResourcePath, countAlpha
from Exceptions import *
from configurations import ClassicConfig, FourPlayerConfig
from Pieces import *


class Board():
    def __init__(self):
        self._board = []

    def __iter__(self):
        """
        Returns iterator of board

        Starting from top left, iterates through evey piece of the board
        """
        for p in [p for row in self._board for p in row]:
            yield p

    def __str__(self):
        string = "\n"
        ending = "\t|\n\n\t\t__" + ("\t__" * self.cols) + "\n\n\t\t"
        alpha = countAlpha()

        for row in self._board:

            num, char = next(alpha)

            string += str(self.rows - num) + "\t|\t\t"

            for piece in row:
                string += str(piece) + "\t"

            string += "\n\n"

            ending += "\t" + char.upper()

        return string + ending + "\n\n"

    def __setitem__(self, index, item):

        try:
            iter(item)
        except TypeError:
            item = [item]

        try:
            iter(index)
        except TypeError:
            index = [index]

        if len(index) != len(item):
            raise ValueError("List index expected {0} values to unpack but {1} were given".format(
                len(item), len(index)))

        for i, vec in enumerate(index):

            if isinstance(self._board[vec.row][vec.col], Disabled):
                raise DisabledError(vec.getStr(self))

            item1 = self._board[vec.row][vec.col]
            item2 = item[i]

            if not isinstance(item2, Disabled):

                if not isinstance(item1, Empty):
                    self._removePiece(item1)

                if not isinstance(item2, Empty):

                    if item2 in [p for pList in self.pieces.values() for p in pList]:
                        pass
                    else:
                        self._addPiece(item2, vec)

            self._board[vec.row][vec.col] = item2

    def __getitem__(self, index):
        res = []

        try:
            iter(index)
        except TypeError:
            index = [index]

        for vec in index:
            if isinstance(self._board[vec.row][vec.col], Disabled):
                raise DisabledError(vec.getStr(self))
            res.append(self._board[vec.row][vec.col])

        if len(res) == 1:
            return res.pop()
        else:
            return res

    def removeColor(self, color):
        vectors = list(map(lambda p: p.vector, self.pieces[color]))
        self[vectors] = [Empty(vector) for vector in vectors]
        self.checkForCheck()

    def setup(self, config={}):
        with open(getResourcePath(__file__, "configurations/DefaultConfig.JSON"), "r") as default:
            dConfig = json.load(default)

            self.rows = config.get("rows") or dConfig.get("rows ")
            self.cols = config.get("cols") or dConfig.get("cols")
            self.pieces = config.get("pieces") or dConfig.get("pieces")
            self.moves = config.get("moves") or dConfig.get("moves")
            self.promoteTo = config.get("promoteTo") or dConfig.get("promoteTo")
            self.promoteFrom = config.get("promoteFrom") or dConfig.get("promoteFrom")
            self.promoteAt = config.get("promoteAt") or dConfig.get("promteAt")
            self.turnorder = config.get("turnorder") or dConfig.get("turnorder")

            self._board = [[Empty(ChessVector((row, col))) for col in range(self.cols)] for row in range(self.rows)]

            for color, pieceList in self.pieces.items():
                for piece in pieceList:
                    self[piece.vector] = piece

            for vec in config.get("disabled") or dConfig.get("disabled"):
                self[vec] = Disabled(vec)

        self.checks = {key: False for key in self.pieces.keys()}
        self.checkmates = copy(self.checks)
        self.kings = {key: [piece for piece in self.pieces[key] if isinstance(piece, King)] for key in self.pieces.keys()}
        self.history = []

        self.checkForCheck()

    def swapPositions(self, vec1, vec2):
        self._board[vec1.row][vec1.col].move(vec2)
        self._board[vec2.row][vec2.col].move(vec1)
        self._board[vec1.row][vec1.col], self._board[vec2.row][vec2.col] = self._board[vec2.row][vec2.col], self._board[vec1.row][vec1.col]

    def isEmpty(self, vector):
        return isinstance(self[vector], Empty)

    def isThreatened(self, vector, alliedColor):
        hostilePieces = [piece for col, pList in self.pieces.items() if col != alliedColor for piece in pList]

        for hp in hostilePieces:
            hostile = hp.getMoves(self, ignoreCheck=True)
            if vector in hostile:
                return True
        else:
            return False

    def checkForCheck(self, checkForMate=True):
        for color in self.pieces.keys():

            for alliedKing in self.kings[color]:

                if self.isThreatened(alliedKing.vector, color):
                    self.checks[color] = True
                    break
            else:
                self.checks[color] = False

            if self.checks[color] and checkForMate:

                alliedPiecesPos = map(lambda p: p.vector, self.pieces[color])

                for alliedPos in list(alliedPiecesPos):
                    for move in self[alliedPos].getMoves(self, ignoreCheck=True):
                        testBoard = deepcopy(self)
                        for pieceType in [None, *self.promoteTo[color]]:
                            try:
                                testBoard.movePiece(alliedPos, move, ignoreMate=True,
                                                    checkForMate=False, promote=pieceType,
                                                    printOut=False)
                            except PromotionError:
                                continue
                            else:
                                break

                        if testBoard.checks[color]:
                            continue
                        else:
                            self.checkmates[color] = False
                            break
                    else:
                        continue
                    break
                else:
                    self.checkmates[color] = True

    def movePiece(self, startVec, targetVec,
                  ignoreMate=False, checkForCheck=True,
                  checkForMate=True, printOut=True, *args, **kwargs):

        if self.isEmpty(startVec):
            raise EmptyError(startVec.getStr(self))

        startPiece = self[startVec]

        if self.checkmates[startPiece.color] and not ignoreMate:
            raise CheckMate

        for move in self.moves[startPiece.color]:
            if move.pieceCondition(startPiece):
                if targetVec in move.getDestinations(startPiece, self):
                    notation = move.action(startPiece, targetVec, self, *args, **kwargs)
                    if checkForCheck:
                        self.checkForCheck(checkForMate=checkForMate)
                    break

        else:
            raise IllegalMove(startVec.getStr(self), targetVec.getStr(self))

        for color in self.checks.keys():
            if self.checkmates[color]:
                if printOut:
                    print(f"{color} in Checkmate!")
                if not "#" in notation:
                    notation += "#"

            elif self.checks[color]:
                if printOut:
                    print(f"{color} in Check!")
                if not "+" in notation:
                    notation += "+"

        for piece in [p for pList in self.pieces.values() for p in pList]:

            if not piece is startPiece:
                piece.postAction(self)

        self.history.append(notation)
        if printOut:
            print(notation)
        return notation

    def _addPiece(self, piece, vector):

        if not piece.color in self.pieces:
            self.pieces[piece.color] = []
            self.kings[piece.color] = []
            self.checks[piece.color] = False
            self.checkmates[piece.color] = False

        self.pieces[piece.color].append(piece)

        if isinstance(piece, King):
            self.kings[piece.color].append(piece)

        piece.vector = vector

    def _removePiece(self, piece):

        self.pieces[piece.color].remove(piece)

        if isinstance(piece, King) and piece in self.kings[piece.color]:
            self.kings[piece.color].remove(piece)

        if not self.pieces[piece.color]:
            del self.pieces[piece.color]
            del self.promoteTo[piece.color]
            del self.promoteFrom[piece.color]
            del self.promoteAt[piece.color]
            del self.kings[piece.color]
            del self.checks[piece.color]
            del self.checkmates[piece.color]

            self.turnorder.remove(piece.color)

        piece.vector = None


def initClassic():

    board = Board()
    board.setup(deepcopy(ClassicConfig.CONFIG))
    return board


def init4P():
    board = Board()
    board.setup(deepcopy(FourPlayerConfig.CONFIG))
    return board


if __name__ == "__main__":

    # Do some testing
    pass
