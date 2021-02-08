from .Pieces import *
from abc import ABC, abstractclassmethod
from .Utils import createNotation
from .Exceptions import PromotionError

class Move(ABC):

    @abstractclassmethod
    def pieceCondition(thisMove, piece, *args, **kwargs) -> bool:
        """Test if piece satisfies move requirement"""
        raise NotImplementedError

    @abstractclassmethod
    def getDestinations(thisMove, piece, board, *args, **kwargs) -> list:
        """Return list of possible destinations"""
        raise NotImplementedError

    @abstractclassmethod
    def action(thisMove, startPiece, targetPos, board, *args, **kwargs) -> str:
        """Move the piece"""
        raise NotImplementedError


class Standard(Move):

    @classmethod
    def pieceCondition(thisMove, *args):
        return True

    @classmethod
    def getDestinations(thisMove, piece, board, *args, **kwargs):
        return piece.getStandardMoves(board)

    @classmethod
    def action(thisMove, startPiece, targetVec, board, promote=None, *args, **kwargs):

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

    @classmethod
    def pieceCondition(thisMove, piece, *args, **kwargs):
        return piece.firstMove and isinstance(piece, King)

    @classmethod
    def action(thisMove, startPiece, targetVec, board, *args, **kwargs):
        for rook in thisMove.findRooks(startPiece, board):
            between = thisMove.findBetween(startPiece.vector, rook.vector)
            if targetVec in between:
                kingTarget, rookTarget = thisMove.getTargets(between)
                board.swapPositions(startPiece.vector, kingTarget)
                board.swapPositions(rook.vector, rookTarget)
                break
        else:
            raise ValueError(f"Piece cannot move to {targetVec}")

    def findBetween(vec1, vec2):
        rowStep = vec1.row - vec2.row and (1, -1)[vec1.row - vec2.row < 0]
        colStep = vec1.col - vec2.col and (1, -1)[vec1.col - vec2.col < 0]

        if not rowStep:
            colRange = range(vec2.col + colStep, vec1.col, colStep)
            rowRange = [vec1.row] * len(colRange)
        else:
            rowRange = range(vec2.row + rowStep, vec1.row, rowStep)
            colRange = [vec1.col] * len(rowRange)

        return [ChessVector(idx) for idx in zip(rowRange, colRange)]

    def emptyBetween(board, between):
        for vector in between:
            if not isinstance(board[vector], Empty):
                return False
        else:
            return True

    def findRooks(piece, board):
        def vecCondition(vec1, vec2):
            return bool(vec2.row - vec1.row) != bool(vec2.col - vec1.col) and (not vec2.row - vec1.row or not vec2.col - vec2.col)

        rookList = []
        for p in board.iterPieces(piece.color):
            if isinstance(p, Rook) and p.firstMove and vecCondition(piece.vector, p.vector):
                rookList.append(p)
        return rookList

    def getTargets(between):
        if not len(between) % 2:
            target1 = between[int((len(between) / 2) - 1)]
            target2 = between[int((len(between) / 2))]
        else:
            target1 = between[int((len(between) / 2) - 0.5)]
            target2 = between[int((len(between) / 2) + 0.5)]
        return (target1, target2)


class CastleK(_Castling):

    @classmethod
    def getDestinations(thisMove, piece, board, *args, **kwargs):
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
    def action(thisMove, *args, **kwargs):
        super().action(*args, **kwargs)
        return "O-O"


class CastleQ(_Castling):

    @classmethod
    def getDestinations(thisMove, piece, board, *args, **kwargs):
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
    def action(thisMove, *args, **kwargs):
        super().action(*args, **kwargs)
        return "O-O-O"


class EnPassant(Move):

    @classmethod
    def pieceCondition(thisMove, piece, *args, **kwargs):
        return isinstance(piece, Pawn)

    @classmethod
    def getDestinations(thisMove, piece, board, *args, **kwargs):
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
    def action(thisMove, piece, targetVec, board, *args, **kwargs):

        notation = createNotation(board, piece, targetVec,
            isPawn=True, capture=True)

        board[targetVec - piece.forwardVec] = Empty(targetVec - piece.forwardVec)
        board.swapPositions(piece.vector, targetVec)
        return notation


if __name__ == "__main__":

    # Do some testing
    pass
