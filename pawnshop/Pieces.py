# Pieces.py

from copy import deepcopy
from abc import ABC, abstractmethod
from typing import List
from .Utils import (
    _catchOutofBounce,
    _positivePos,
    removeDupes
)
from .ChessVector import ChessVector
from .ChessBoard import Board


_directions = {
    "up": ((-1, 0), (-1, -1), (-1, 1)),
    "down": ((1, 0), (1, 1), (1, -1)),
    "right": ((0, 1), (-1, 1), (1, 1)),
    "left": ((0, -1), (1, -1), (-1, -1))
}

_directions = {key: [ChessVector(offset) for offset in _directions[key]] for key in _directions}


class Piece(ABC):
    """Abstract base class for pieces

    :param color: Color of piece
    :param value: Numerical value of piece
    :param symbol: Char symbol of piece
    """

    def __init__(self, color: str, value: int, symbol: str, *args, **kwargs):
        self.vector = None
        self.color = color
        self.value = value
        self.symbol = symbol
        self.firstMove = True

    def __str__(self):
        return self.color[0] + self.symbol

    @abstractmethod
    def getStandardMoves(self, board: Board):
        """Returns standard destinations of piece in board
        """
        raise NotImplementedError

    def getMoves(self, board: Board, ignoreCheck=False, ignoreMate=False) -> List[ChessVector]:
        """Returns all moves of piece in board

        Uses board.getMoves() method to check what moves piece is allowed to.

        :param board: Board to move in
        :param **Flags: Flags to pass into move
        :returns: List of possible moves
        :rtype: ``list``

        :**Flags:
            :ignoreCheck (False): Ignore checks when getting moves
            :ignoreMate (False): Ignore checkmate when getting moves
        """
        destList = []
        for move in board.getMoves(self.color):
            if move.pieceCondition(self):
                destList.extend(move.getDestinations(self, board))

        if not ignoreCheck:
            remove = []

            for dest in destList:
                testBoard = deepcopy(board)
                testBoard.movePiece(self.vector, dest, ignoreMate=ignoreMate, checkForMate=False, printout=False, checkMove=False, promote=Queen, ignoreOrder=True)
                if testBoard.getChecks(self.color):
                    remove.append(dest)

            for dest in remove:
                destList.remove(dest)

        return destList

    def move(self, destVector: ChessVector) -> None:
        """Move piece to destination

        :param destVector: Destination
        """
        self.vector = destVector
        self.firstMove = False

    def postAction(self, board: Board) -> None:
        """Do action after piece is moved in board

        Call this after a piece is moved in board
        """
        pass

    @_positivePos
    @_catchOutofBounce
    def canWalk(self, vector: ChessVector, board: Board) -> bool:
        """Check if piece can walk to destination in board

        :param vector: Destination
        :param board: Board to check in
        :returns: If piece can move
        :rtype: ``bool``
        """
        return board.isEmpty(vector)

    @_positivePos
    @_catchOutofBounce
    def canCapture(self, vector: ChessVector, board: Board) -> bool:
        """Check if piece can capture to destination in board

        :param vector: Destination
        :param board: Board to check in
        :returns: If piece can capture
        :rtype: ``bool``
        """
        destPiece = board[vector]
        try:
            return destPiece.color != self.color
        except AttributeError:
            return False

    @_positivePos
    @_catchOutofBounce
    def canMove(self, vector: ChessVector, board: Board) -> bool:
        """Check if piece can capture to destination in board

        :param vector: Destination
        :param board: Board to check in
        :returns: If piece can move (capture or walk)
        :rtype: ``bool``
        """
        destPiece = board[vector]
        try:
            return destPiece.color != self.color
        except AttributeError:
            return board.isEmpty(vector)

    def _getMovesInLine(self, iterVector: ChessVector, board: Board) -> List[ChessVector]:
        """Get moves in one line

        Return all positions piece is can move to iterating with iterVector.
        Stops if piece can capture as piece cannot continue moving after capturing.

        :param iterVector: Vector to iterate moves with
        :param board: Board to check in
        :returns: List of possible destinations
        :rtype: ``list``
        """
        moveList = []
        newV = self.vector
        while True:
            newV += iterVector
            if self.canWalk(newV, st):
                moveList.append(newV)
            elif self.canCapture(newV, board):
                moveList.append(newV)
                break
            else:
                break
        return moveList


class Pawn(Piece):
    """Pawn object

    :param color: Color of piece
    :param direction: Movement direction of Pawn (default is "up")
    :param rank: Starting rank of pawn, used to calc promote
    """
    def __init__(self, color: str, direction="up", rank=2, *args, **kwargs):
        super().__init__(color, 1, "P")

        self.passed = False
        self.direction = direction.lower()
        self.rank = rank

        if direction in _directions.keys():
            self.forwardVec, self.lDiagVec, self.rDiagVec = _directions[direction]
        else:
            raise ValueError(f"Direction is not any of {_directions.keys()}")

    def getStandardMoves(self, board: Board) -> List[ChessVector]:
        """Returns standard destinations of piece in board

        :param board: Board to check in
        :returns: List of standard posssible destinations
        :rtype: ``list``
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

    def move(self, newV: ChessVector) -> None:
        """Move piece to destination

        If Pawn moves 2 places, it can be captured by en-passant.

        :param newV: Destination
        """
        if self.firstMove:
            if abs(self.vector.row - newV.row) == 2 or abs(self.vector.col - newV.col) == 2:
                self.passed = True
                self.rank += 1
        self.rank += 1
        super().move(newV)

    def postAction(self, *args, **kwargs):
        """Do action after piece is moved in board

        Call this after a piece is moved in board
        """
        self.passed = False

    def getAttacking(self, *args, **kwargs) -> Tuple[ChessVector]:
        """Get the threatened positions of piece

        :returns: Tuple of threatened positions
        :rType: ´´tuple´´
        """
        return [self.vector + self.lDiagVec, self.vector + self.rDiagVec]


class Rook(Piece):
    """Rook object

    :param color: Color of piece
    """
    def __init__(self, color: str, *args, **kwargs):
        super().__init__(color, 5, "R")

    def getStandardMoves(self, board: Board) -> List[ChessVector]:
        """Returns standard destinations of piece in board

        :param board: Board to check in
        :returns: List of standard posssible destinations
        :rtype: ``list``
        """
        destList = []
        for vecTuple in _directions.values():
            forwardVec = vecTuple[0]
            destList.extend(self._getMovesInLine(forwardVec, board))
        return destList


class Knight(Piece):
    """Knight object

    :param color: Color of piece
    """
    def __init__(self, color: str, *args, **kwargs):
        super().__init__(color, 3, "N")

    def getStandardMoves(self, board: Board) -> List[ChessVector]:
        """Returns standard destinations of piece in board

        :param board: Board to check in
        :returns: List of standard posssible destinations
        :rtype: ``list``
        """
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
    """Bishop object

    :param color: Color of piece
    """
    def __init__(self, color: str, *args, **kwargs):
        super().__init__(color, 3, "B")

    def getStandardMoves(self, board: Board) -> List[ChessVector]:
        """Returns standard destinations of piece in board

        :param board: Board to check in
        :returns: List of standard posssible destinations
        :rtype: ``list``
        """
        destList = []
        for vecTuple in _directions.values():
            destList.extend(self._getMovesInLine(vecTuple[1], board))
        return destList


class King(Piece):
    """King object

    :param color: Color of piece
    """
    def __init__(self, color: str, *args, **kwargs):
        super().__init__(color, int(1e10), "K")

    def getStandardMoves(self, board: Board) -> List[ChessVector]:
        """Returns standard destinations of piece in board

        :param board: Board to check in
        :returns: List of standard posssible destinations
        :rtype: ``list``
        """
        destList = []
        for offsetVec in removeDupes([vec for vecList in _directions.values() for vec in vecList]):
            destVec = self.vector + offsetVec
            if self.canMove(destVec, board):
                destList.append(destVec)
        return destList


class Queen(Piece):
    """Queen object

    :param color: Color of piece
    """
    def __init__(self, color: str, *args, **kwargs):
        super().__init__(color, 9, "Q")

    def getStandardMoves(self, board: Board) -> List[ChessVector]:
        """Returns standard destinations of piece in board

        :param board: Board to check in
        :returns: List of standard posssible destinations
        :rtype: ``list``
        """
        destList = []
        for vecTuple in _directions.values():
            destList.extend(self._getMovesInLine(vecTuple[0], board))
            destList.extend(self._getMovesInLine(vecTuple[1], board))
        return destList


class Disabled():
    """Disabled object

    Object for representing disabled positions in chessboard

    :param vector: Position of disabled square
    """
    def __init__(self, vector: ChessVector, *args, **kwargs):
        self.vector = vector

    def __str__(self):
        return "  "

    def move(self, vec: ChessVector):
        """Move disabled object

        Move the disabled square

        :param vec: New position
        """
        self.vector = vec


class Empty():
    """Empty object

    Object for representing empty positions in chessboard

    :param vector: Position of empty square
    """
    def __init__(self, vector: ChessVector, *args, **kwargs):
        self.vector = vector

    def __str__(self):
        return "__"

    def move(self, vec: ChessVector):
        """Move empty object

        Move the empty square

        :param vec: New position
        """
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
