# Pieces.py

from copy import deepcopy
from abc import ABC, abstractmethod
from .Utils import (
    _catchOutofBounce,
    _positivePos,
    removeDupes
)
from .ChessVector import ChessVector


_directions = {
    "up": ((-1, 0), (-1, -1), (-1, 1)),
    "down": ((1, 0), (1, 1), (1, -1)),
    "right": ((0, 1), (-1, 1), (1, 1)),
    "left": ((0, -1), (1, -1), (-1, -1))
}

_directions = {key: [ChessVector(offset) for offset in _directions[key]] for key in _directions}


class Piece(ABC):
    def __init__(self, color, value, symbol, *args, **kwargs):
        self.vector = None
        self.color = color
        self.value = value
        self.symbol = symbol
        self.firstMove = True

    def __str__(self):
        return self.color[0] + self.symbol

    @abstractmethod
    def getStandardMoves(self, board):
        """Returns standard destinations of piece in board"""
        raise NotImplementedError

    def getMoves(self, board, ignoreCheck=False, ignoreMate=False):
        """Returns board-specific moves of piece in board"""
        destList = []
        for move in board.moves[self.color]:
            if move.pieceCondition(self):
                destList.extend(move.getDestinations(self, board))

        if not ignoreCheck:
            remove = []

            for dest in destList:
                testBoard = deepcopy(board)
                testBoard.movePiece(self.vector, dest, ignoreMate=ignoreMate, checkForMate=False, printOut=False, checkMove=False, promote=Queen, ignoreOrder=True)
                if testBoard.checks[self.color]:
                    remove.append(dest)

            for dest in remove:
                destList.remove(dest)

        return destList

    def move(self, destVector):
        """Move piece"""
        self.vector = destVector
        self.firstMove = False

    def postAction(self, board):
        """Do something after a piece is moved"""
        pass

    @_positivePos
    @_catchOutofBounce
    def canWalk(self, vector, board):
        return board.isEmpty(vector)

    @_positivePos
    @_catchOutofBounce
    def canCapture(self, vector, board):
        destPiece = board[vector]
        try:
            return destPiece.color != self.color
        except AttributeError:
            return False

    @_positivePos
    @_catchOutofBounce
    def canMove(self, vector, board):
        destPiece = board[vector]
        try:
            return destPiece.color != self.color
        except AttributeError:
            return board.isEmpty(vector)

    def _getMovesInLine(self, iterVector, board):
        moveList = []
        newV = self.vector
        while True:
            newV += iterVector
            if self.canWalk(newV, board):
                moveList.append(newV)
            elif self.canCapture(newV, board):
                moveList.append(newV)
                break
            else:
                break
        return moveList


class Pawn(Piece):
    def __init__(self, color, direction="up", rank=2, *args, **kwargs):
        super().__init__(color, 1, "P")

        self.passed = False
        self.direction = direction.lower()
        self.rank = rank

        if direction in _directions.keys():
            self.forwardVec, self.lDiagVec, self.rDiagVec = _directions[direction]
        else:
            raise ValueError(f"Direction is not any of {_directions.keys()}")

    def getStandardMoves(self, board):
        """
        Returns list of possible destinations
        """

        destList = []
        destVec = self.vector + self.forwardVec

        if self.canWalk(destVec, board):
            destList.append(destVec)
            if self.firstMove:
                destVec += self.forwardVec
                if self.canWalk(destVec, board):
                    destList.append(destVec)

        for destVec in self.getAttacking(board):
            if self.canCapture(destVec, board):
                destList.append(destVec)

        return destList

    def move(self, newV):
        if self.firstMove:
            if abs(self.vector.row - newV.row) == 2 or abs(self.vector.col - newV.col) == 2:
                self.passed = True
                self.rank += 1
        self.rank += 1
        super().move(newV)

    def postAction(self, board):
        self.passed = False

    def getAttacking(self, board):
        return (self.vector + self.lDiagVec, self.vector + self.rDiagVec)


class Rook(Piece):
    def __init__(self, color, *args, **kwargs):
        super().__init__(color, 5, "R")

    def getStandardMoves(self, board):
        destList = []
        for vecTuple in _directions.values():
            forwardVec = vecTuple[0]
            destList.extend(self._getMovesInLine(forwardVec, board))
        return destList


class Knight(Piece):
    def __init__(self, color, *args, **kwargs):
        super().__init__(color, 3, "N")

    def getStandardMoves(self, board):
        destList = []
        offsetList = [
            (1, 2),
            (1, -2),
            (-1, 2),
            (-1, -2),
            (2, 1),
            (2, -1),
            (-2, 1),
            (-2, -1)
        ]
        vecList = [ChessVector(offset) for offset in offsetList]

        for offsetVec in vecList:
            destVec = self.vector + offsetVec
            if self.canMove(destVec, board):
                destList.append(destVec)
        return destList


class Bishop(Piece):
    def __init__(self, color, *args, **kwargs):
        super().__init__(color, 3, "B")

    def getStandardMoves(self, board):
        destList = []
        for vecTuple in _directions.values():
            destList.extend(self._getMovesInLine(vecTuple[1], board))
        return destList


class King(Piece):
    def __init__(self, color, *args, **kwargs):
        super().__init__(color, int(1e10), "K")

    def getStandardMoves(self, board):
        destList = []
        for offsetVec in removeDupes([vec for vecList in _directions.values() for vec in vecList]):
            destVec = self.vector + offsetVec
            if self.canMove(destVec, board):
                destList.append(destVec)
        return destList


class Queen(Piece):
    def __init__(self, color, *args, **kwargs):
        super().__init__(color, 9, "Q")

    def getStandardMoves(self, board):
        destList = []
        for vecTuple in _directions.values():
            destList.extend(self._getMovesInLine(vecTuple[0], board))
            destList.extend(self._getMovesInLine(vecTuple[1], board))
        return destList


class Disabled():
    def __init__(self, vector, *args, **kwargs):
        self.vector = vector

    def __str__(self):
        return "  "

    def move(self, vec):
        self.vector = vec


class Empty():
    def __init__(self, vector, *args, **kwargs):
        self.vector = vector

    def __str__(self):
        return "__"

    def move(self, vec):
        self.vector = vec


pieceNotations = {
    "P": Pawn,
    "N": Knight,
    "B": Bishop,
    "R": Rook,
    "Q": Queen,
    "K": King
}

if __name__ == "__main__":

    # Do some testing
    pass
