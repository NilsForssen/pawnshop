# Moves.py

from Typing import List, Union, Tuple
from .Pieces import *
from .ChessBoard import Board
from abc import ABC, abstractclassmethod
from .Utils import createNotation
from .Exceptions import PromotionError


class Move(ABC):
    """Abstract class for moves in chess
    """

    @abstractclassmethod
    def pieceCondition(thisMove, piece: Piece, *args, **kwargs) -> bool:
        """Test if piece satisfies move requirement
        """
        raise NotImplementedError

    @abstractclassmethod
    def getDestinations(thisMove, piece: Piece, board: Board, *args, **kwargs) -> list:
        """Return list of possible destinations
        """
        raise NotImplementedError

    @abstractclassmethod
    def action(thisMove, startPiece, targetPos, board, *args, **kwargs) -> str:
        """Move the piece
        """
        raise NotImplementedError


class Standard(Move):
    """Standard move in chess

    Moves piece according to .getStandardMoves() method
    """

    @classmethod
    def pieceCondition(thisMove, *args, **kwargs) -> bool:
        """Moving piece must satisfy this condition

        Since there is no condition to standard moves, this will always return True.

        :returns: True
        :rtype: ``bool``
        """
        return True

    @classmethod
    def getDestinations(thisMove, piece: Piece, board: Board, *args, **kwargs) -> List[ChessVector]:
        """Get possible destinations of piece

        Calls piece.getStandardMoves() method to get all standard moves of piece.
        Call pieceCondition() classmethod prior.

        :param piece: Piece to get moves from
        :param board: Board which piece is stored in
        :returns: list of possible destinations
        :rtype: list
        """
        return piece.getStandardMoves(board)

    @classmethod
    def action(thisMove, startPiece: Piece, targetVec: ChessVector, board: Board, promote=None, *args, **kwargs) -> str:
        """Performs the action of move

        Moves piece according to standard move rules.
        Call pieceCondition() and getDestinations() classmethods prior.

        :param startPiece: Piece to be moved
        :param targetVec: Destination of piece move
        :param board: Board to perform move in
        :param promote: Promotion type of piece (default is None)
        :returns: Notation of move
        :rtype: ``str``
        """
        promo = False

        for pieceType in board.getPromoteFrom(startPiece.color):
            if isinstance(startPiece, pieceType):

                if startPiece.rank + abs((startPiece.vector - targetVec).tuple()[startPiece.forwardVec.col]) == board.getPromoteAt(startPiece.color):
                    if promote is None:
                        raise PromotionError

                    if promote not in board.getPromoteTo(startPiece.color):
                        raise PromotionError(
                            f"{startPiece.color} cannot promote to {promote}!")

                    promo = True

                break

        targetPiece = board[targetVec]

        notation = createNotation(
            board, startPiece, targetVec,
            isPawn=isinstance(startPiece, Pawn), capture=not isinstance(targetPiece, Empty))

        if not isinstance(targetPiece, Empty):
            board[targetVec] = Empty(targetVec)
            board.swapPositions(startPiece.vector, targetVec)
        else:
            board.swapPositions(startPiece.vector, targetVec)
        if promo:
            newPiece = promote(startPiece.color)
            newPiece.move(startPiece.vector)
            board[startPiece.vector] = newPiece
            notation += "=" + newPiece.symbol

        return notation


class _Castling(Move):
    """Parent class to King-side and Queen-side castling
    """

    @classmethod
    def pieceCondition(thisMove, piece: Piece, *args, **kwargs) -> bool:
        """Moving piece must satisfy this condition

        Must be pieces first move and piece must be instance of ``King``.

        :param piece: Piece to check
        :returns: If piece satisfies requirements
        :rtype: ``bool``
        """
        return piece.firstMove and isinstance(piece, King)

    @classmethod
    def action(thisMove, startPiece: Piece, targetVec: ChessVector, board: Board, *args, **kwargs) -> None:
        """Performs the action of move

        Moves piece according to move rules.
        Returns None as Queen-side and King-side castling are noted differently.
        Call pieceCondition() and getDestinations() classmethods prior.

        :param startPiece: Piece to be moved
        :param targetVec: Destination of piece move
        :param board: Board to perform move in
        """
        for rook in thisMove.findRooks(startPiece, board):
            between = thisMove.findBetween(startPiece.vector, rook.vector)
            if targetVec in between:
                kingTarget, rookTarget = thisMove.getTargets(between)
                board.swapPositions(startPiece.vector, kingTarget)
                board.swapPositions(rook.vector, rookTarget)
                break
        else:
            raise ValueError(f"Piece cannot move to {targetVec}")

    def findBetween(vec1: ChessVector, vec2: ChessVector) -> List[ChessVector]:
        """Helper function to find all positions between two positions

        Helper function.
        If there are not positions between or given positions
        are not in a row, the returned list is empty.

        :param vec1: First position
        :param vec2: Second position
        :returns: List of possitions betweeen
        :rtype: ``list``
        """
        rowStep = vec1.row - vec2.row and (1, -1)[vec1.row - vec2.row < 0]
        colStep = vec1.col - vec2.col and (1, -1)[vec1.col - vec2.col < 0]

        if not rowStep:
            colRange = range(vec2.col + colStep, vec1.col, colStep)
            rowRange = [vec1.row] * len(colRange)
        elif not colStep:
            rowRange = range(vec2.row + rowStep, vec1.row, rowStep)
            colRange = [vec1.col] * len(rowRange)
        else:
            rowRange = range(0,0)
            colRange = range(0,0)

        return [ChessVector(idx) for idx in zip(rowRange, colRange)]

    def emptyBetween(board: Board, between: List[ChessVector]) -> bool:
        """Check if all positions are emtpy

        Helper funciton.
        Check if all positions between two pieces are empty

        :param board: Board to check positions in
        :param between: List of positions to check
        :returns: If all positions are empty or not
        :rtype: ``bool``
        """
        for vector in between:
            if not isinstance(board[vector], Empty):
                return False
        else:
            return True

    def findRooks(piece: Piece, board: Board) -> List[Piece]:
        """Find all rooks in board that are on same lane as piece

        Helper function.
        Iterates through all pieces on board looking for
        rooks on same lane as piece.

        :param piece: Piece to check for same lane
        :param board: Board to check for rooks in
        :returns: List of rooks on same lane as piece
        :rtype: ``list``
        """
        def vecCondition(vec1, vec2):
            return bool(vec2.row - vec1.row) != bool(vec2.col - vec1.col) and (not vec2.row - vec1.row or not vec2.col - vec2.col)

        rookList = []
        for p in board.iterPieces(piece.color):
            if isinstance(p, Rook) and p.firstMove and vecCondition(piece.vector, p.vector):
                rookList.append(p)
        return rookList

    def getTargets(between: list) -> Union[Tuple[ChessVector], None]:
        """Get castling targets

        Helper function
        Get the two middle squares of list of positions between.
        If list is of length 1, this returns None.
        Biased towards the start of list.


        :param between: List of positions between
        :returns: Tuple of target positions
        :rtype: ``tuple`` or None
        """
        if not len(between) > 1:
            return None
        if not len(between) % 2:
            target1 = between[int((len(between) / 2) - 1)]
            target2 = between[int((len(between) / 2))]
        else:
            target1 = between[int((len(between) / 2) - 0.5)]
            target2 = between[int((len(between) / 2) + 0.5)]
        return (target1, target2)


class CastleK(_Castling):
    """Castle King-side move
    """

    @classmethod
    def getDestinations(thisMove, piece: Piece, board: Board, *args, **kwargs) -> List[ChessVector]:
        """Get possible destinations of piece

        Returns all possible castling moves of piece.
        Call pieceCondition() classmethod prior.

        :param piece: Piece to get moves from
        :param board: Board which piece is stored in
        :returns: list of possible destinations
        :rtype: list
        """
        destList = []
        if not board.getChecks(piece.color):
            for rook in thisMove.findRooks(piece, board):
                between = thisMove.findBetween(piece.vector, rook.vector)
                if thisMove.emptyBetween(board, between) and not len(between) % 2:
                    kingTarget, _ = thisMove.getTargets(between)
                    walked = thisMove.findBetween(piece.vector, kingTarget)
                    for vec in walked:
                        if board.isThreatened(vec, piece.color):
                            break
                    else:
                        destList.append(kingTarget)
        return destList

    @classmethod
    def action(thisMove, *args, **kwargs) -> str:
        """Performs the action of move

        Moves piece according to move rules.
        Returns the notation of the castling move
        Call pieceCondition() and getDestinations() classmethods prior.

        :param startPiece: Piece to be moved
        :param targetVec: Destination of piece move
        :param board: Board to perform move in
        :returns: Notation of move
        :rtype: str
        """
        super().action(*args, **kwargs)
        return "O-O"


class CastleQ(_Castling):

    @classmethod
    def getDestinations(thisMove, piece: Piece, board: Board, *args, **kwargs) -> List[ChessVector]:
        """Get possible destinations of piece

        Returns all possible castling moves of piece.
        Call pieceCondition() classmethod prior.

        :param piece: Piece to get moves from
        :param board: Board which piece is stored in
        :returns: list of possible destinations
        :rtype: list
        """
        destList = []
        if not board.getChecks(piece.color):
            for rook in thisMove.findRooks(piece, board):
                between = thisMove.findBetween(piece.vector, rook.vector)
                if thisMove.emptyBetween(board, between) and len(between) % 2:
                    kingTarget, _ = thisMove.getTargets(between)
                    walked = thisMove.findBetween(piece.vector, kingTarget)
                    for vec in walked:
                        if board.isThreatened(vec, piece.color):
                            break
                    else:
                        destList.append(kingTarget)
        return destList

    @classmethod
    def action(thisMove, *args, **kwargs) -> str:
        """Performs the action of move

        Moves piece according to move rules.
        Returns the notation of the castling move
        Call pieceCondition() and getDestinations() classmethods prior.

        :param startPiece: Piece to be moved
        :param targetVec: Destination of piece move
        :param board: Board to perform move in
        :returns: Notation of move
        :rtype: str
        """
        super().action(*args, **kwargs)
        return "O-O-O"


class EnPassant(Move):
    """Special move en-passant
    """

    @classmethod
    def pieceCondition(thisMove, piece: Piece, *args, **kwargs) -> bool:
        """Moving piece must satisfy this condition

        Piece must be of instance ``Pawn``

        :param piece: Piece to check
        :returns: If piece satisfies requirements
        :rtype: ``bool``
        """
        return isinstance(piece, Pawn)

    @classmethod
    def getDestinations(thisMove, piece: Piece, board: Board, *args, **kwargs) -> List[ChessVector]:
        """Get possible destinations of piece

        Returns all possible en-passant moves of piece.
        Call pieceCondition() classmethod prior.

        :param piece: Piece to get moves from
        :param board: Board which piece is stored in
        :returns: list of possible destinations
        :rtype: list
        """
        destList = []
        for diagVec in (piece.lDiagVec, piece.rDiagVec):
            checkVec = (piece.vector - piece.forwardVec) + diagVec
            try:
                if isinstance(board[checkVec], Pawn) and board[checkVec].passed and board[checkVec].forwardVec == -piece.forwardVec:
                    destList.append(piece.vector + diagVec)
            except IndexError:
                pass
        return destList

    @classmethod
    def action(thisMove, piece: Piece, targetVec: ChesVector, board: Board, *args, **kwargs) -> str:
        """Performs the action of move

        Moves piece according to move rules.
        Returns the notation of the en-passant move
        Call pieceCondition() and getDestinations() classmethods prior.

        :param startPiece: Piece to be moved
        :param targetVec: Destination of piece move
        :param board: Board to perform move in
        :returns: Notation of move
        :rtype: str
        """
        notation = createNotation(board, piece, targetVec,
            isPawn=True, capture=True)

        board[targetVec - piece.forwardVec] = Empty(targetVec - piece.forwardVec)
        board.swapPositions(piece.vector, targetVec)
        return notation
