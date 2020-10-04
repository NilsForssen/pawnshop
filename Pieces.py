from abc import ABC, abstractmethod
from Utils import (
    _catchOutofBounce,
    _positivePos,
    infiRange
)


_directions = {
    "up": ((-1,0), (-1,-1), (-1,1)),
    "down": ((1,0), (1,1), (1,-1)),
    "right": ((0,1), (-1,1), (1,1)),
    "left": ((0,-1), (1,-1), (-1,-1))
}

class Piece(ABC):
    def __init__(self, color, value, symbol):
        self.position = None
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

    def getSpecificMoves(self, board):
        """Returns board-specific moves of piece in board"""
        destList = []
        for move in board.moveDict(self.color):
            if move.pieceCondition(self, board):
                destList.extend(move.getDestinations)
        return destList

    @abstractmethod
    def getMoves(self, board):
        """Returns all possible destinations of piece in board"""
        raise NotImplementedError

    def move(self, destPos):
        """Move piece"""
        self.position = destPos
        self.firstMove = False

    def postAction(self, board):
        """Do something after a piece is moved"""
        pass

    def getDest(self, offx, offy):
        return (self.position[0] + offx, self.position[1] + offy)

    @_positivePos
    @_catchOutofBounce
    def canWalk(self, pos, board):
        return board.isEmpty(pos)

    @_positivePos
    @_catchOutofBounce
    def canCapture(self, pos, board):
        destPiece = board[pos]
        try:
            return destPiece.color != self.color
        except AttributeError:
            return False

    @_positivePos
    @_catchOutofBounce
    def canMove(self, pos, board):
        destPiece = board[pos]
        try:
            return destPiece.color != self.color
        except AttributeError:
            return board.isEmpty(pos)

    def _getMovesInLine(
        self, board,
        rowIter=infiRange(0, step=0), colIter=infiRange(0, step=0)
        ):

        moveList = []

        while True:

            try:
                pos = self.getDest(next(rowIter), next(colIter))
            except StopIteration:
                break

            if self.canWalk(pos, board):
                moveList.append(pos)
            elif self.canCapture(pos, board):
                moveList.append(pos)
                break
            else:
                break

        return moveList


class Pawn(Piece):
    def __init__(self, color, direction="up"):
        super().__init__(color, 1, "P")

        self.passed = False
        self.direction = direction.lower()

        if direction in _directions.keys():
            self.forward, self.diagL, self.diagR = _directions[direction]
        else:
            raise ValueError(f"Direction is not any of {_directions.items()}")

    def getStandardMoves(self, board):
        """
        Returns list of possible destinations
        """
        destList = []

        dest = self.getDest(*self.forward)
        if self.canWalk(dest, board):
            destList.append(dest)
            if self.firstMove:
                dest = self.getDest(*(self.forward[0]*2, self.forward[1]*2))
                if self.canWalk(dest, board):
                    destList.append(dest)

        for dest in self.getAttacking(board):
            if self.canCapture(dest, board):
                destList.append(dest)

        return destList

    def getMoves(self, board):
        return [*self.getStandardMoves(board), *self.getSpecialMoves(boar)]

    def move(self, pos):
        if self.firstMove:
            if (abs(pos[0] - self.position[0]) == 2
                and pos[1] == self.position[1])
                or (abs(pos[1] - self.position[1]) == 2
                and pos[0] == self.position[0]):

                self.passed = True

        super().move(pos)

    def postAction(self, board):
        passed = False

    def getAttacking(self, board):
        return [self.getDest(*self.diagL), self.getDest(*self.diagR)]


class Rook(Piece):
    def __init__(self, color):
        super().__init__(color, 5, "R")

    def getStandardMoves(self, board):
        destList = []
        destList.extend(self._getMovesInLine(
            board, rowIter=infiRange(1, step=1)))
        destList.extend(self._getMovesInLine(
            board, rowIter=infiRange(-1, step=-1)))
        destList.extend(self._getMovesInLine(
            board, colIter=infiRange(1, step=1)))
        destList.extend(self._getMovesInLine(
            board, colIter=infiRange(-1, step=-1)))
        return destList

    def getMoves(self board):
        return [*self.getStandardMoves, *self.getSpecificMoves]


class Knight(Piece):
    def __init__(self, color):
        super().__init__(color, 3, "N")

    def getStandardMoves(self, board):
        destList = []
        offsetList = [
            (1,2),
            (1,-2),
            (-1,2),
            (-1,-2),
            (2,1),
            (2,-1),
            (-2,1),
            (-2,-1)
        ]
        for offx, offy in offsetList:
            dest = self.getDest(offx, offy)
            if self.canMove(dest, board):
                destList.append(dest)
        return destList

    def getMoves(self, board):
        return [*self.getStandardMoves, *self.getSpecificMoves]


class Bishop(Piece):
    def __init__(self, color):
        super().__init__(color, 3, "B")


    def getStandardMoves(self, board):
        destList = []
        destList.extend(self._getMovesInLine(board,
            rowIter=infiRange(1, step=1), colIter=infiRange(1, step=1)))
        destList.extend(self._getMovesInLine(board,
            rowIter=infiRange(1, step=1), colIter=infiRange(-1, step=-1)))
        destList.extend(self._getMovesInLine(board,
            rowIter=infiRange(-1, step=-1), colIter=infiRange(1, step=1)))
        destList.extend(self._getMovesInLine(board,
            rowIter=infiRange(-1, step=-1), colIter=infiRange(-1, step=-1)))
        return destList

    def getMoves(self, board):
        return [*self.getStandardMoves, *self.getSpecificMoves]


class King(Piece):
    def __init__(self, color):
        super().__init__(color, int(1e10), "K")

    def getStandardMoves(self, board):
        destList = []
        offsetList = [
            (1,0),
            (1,1),
            (0,1),
            (-1,1),
            (-1,0),
            (-1,-1),
            (0,-1),
            (1,-1)
            ]
        for offx, offy in offsetList:
            dest = self.getDest(offx, offy)
            if self.canMove(dest, board):
                destList.append(dest)
        return destList

    def getMoves(self, board):
        return[*self.getStandardMoves, *self.getSpecificMoves]


class Queen(Piece):
    def __init__(self, color):
        super().__init__(color, 9, "Q")

    def getStandardMoves(self, board):
        destList = []
        destList.extend(self._getMovesInLine(board,
            rowIter=infiRange(1, step=1)))
        destList.extend(self._getMovesInLine(board,
            rowIter=infiRange(-1, step=-1)))
        destList.extend(self._getMovesInLine(board,
            colIter=infiRange(1, step=1)))
        destList.extend(self._getMovesInLine(board,
            colIter=infiRange(-1, step=-1)))
        destList.extend(self._getMovesInLine(board,
            rowIter=infiRange(1, step=1), colIter=infiRange(1, step=1)))
        destList.extend(self._getMovesInLine(board,
            rowIter=infiRange(1, step=1), colIter=infiRange(-1, step=-1)))
        destList.extend(self._getMovesInLine(board,
            rowIter=infiRange(-1, step=-1), colIter=infiRange(1, step=1)))
        destList.extend(self._getMovesInLine(board,
            rowIter=infiRange(-1, step=-1), colIter=infiRange(-1, step=-1)))
        return destList

    def getMoves(self, board):
        return [*self.getStandardMoves, *self.getSpecificMoves]


class _Disabled():
    def __str__(self):
        return " "


class _Empty():
    def __str__(self):
        return "__"

if __name__ == "__main__":

    # Do some testing
    pass
