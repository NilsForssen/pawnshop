from Pieces import *
from abc import ABC, abstractclassmethod
from Utils import createNotation

class Move(ABC):

    @abstractclassmethod
    def pieceCondition(thisMove, piece) -> bool:
        """Test if piece satisfies move requirement"""
        raise NotImplementedError

    @abstractclassmethod
    def getDestinations(thisMove, piece, board) -> list:
        """Return list of possible destinations"""
        raise NotImplementedError

    @abstractclassmethod
    def action(thisMove, startPiece, targetPos, board) -> str:
        """Move the piece"""
        raise NotImplementedError


class Standard(Move):

    @classmethod
    def pieceCondition(thisMove, *args):
        return True

    @classmethod
    def getDestinations(thisMove, piece, board):
        return piece.getStandardMoves(board)

    @classmethod
    def action(thisMove, startPiece, targetVec, board):
        capture = False
        targetPiece = board[targetVec]

        if not isinstance(targetPiece, Empty):
            capture = True
            board.swapPositions(startPiece.vector, targetVec)
            board[startPiece.vector] = Empty(startPiece.vector)
        else:
            board.swapPositions(startPiece.vector, targetVec)
            board[startPiece.vector].vector = startPiece.vector

        notation = createNotation(
            board, startPiece, targetVec,
            isPawn=isinstance(startPiece, Pawn), capture=capture)
        startPiece.move(targetVec)
        return notation


class _Castling(Move):

    @classmethod
    def pieceCondition(thisMove, piece):
        return piece.firstMove and isinstance(piece, King)

    @classmethod
    def action(thisMove, startPiece, targetVec, board):
        for rook in thisMove.findRooks(startPiece, board):
            between = thisMove.findBetween(startPiece.vector, rook.vector)
            if targetVec in between:
                kingTarget, rookTarget = thisMove.getTargets(between)
                board.swapPositions(startPiece.vector, kingTarget)
                board.swapPositions(rook.vector, rookTarget)
                startPiece.move(kingTarget)
                rook.move(rookTarget)
                break
        else:
            raise ValueError(f"Piece cannot move to {targetVec }")

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
            return bool(vec2.row - vec1.row) != bool(vec2.col - vec2.row) and (not vec2.row - vec1.row or not vec2.col - vec2.col)

        rookList = []
        for p in board.pieces[piece.color]:
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
    def getDestinations(thisMove, piece, board):
        destList = []
        for rook in thisMove.findRooks(piece, board):
            between = thisMove.findBetween(piece.vector, rook.vector)
            if thisMove.emptyBetween(board, between) and not len(between) % 2:
                kingTarget, _ = thisMove.getTargets(between)
                destList.append(kingTarget)
        return destList

    @classmethod
    def action(thisMove, *args, **kwargs):
        super().ation(*args, **kwargs)
        return "0-0"


class CastleQ(_Castling):

    @classmethod
    def getDestinations(thisMove, piece, board):
        destList = []
        for rook in thisMove.findRooks(piece, board):
            between = thisMove.findBetween(piece.vector, rook.vector)
            if thisMove.emptyBetween(board, between) and len(between) % 2:
                kingTarget, _ = thisMove.getTargets(between)
                destList.append(kingTarget)
        return destList

    @classmethod
    def action(thisMove, *args, **kwargs):
        super().action(*args, **kwargs)
        return "0-0-0"


class EnPassant(Move):

    @classmethod
    def pieceCondition(thisMove, piece):
        return isinstance(piece, Pawn)

    @classmethod
    def getDestinations(thisMove, piece, board):
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
    def action(thisMove, piece, targetVec, board):
        board[targetVec - piece.forwardVec] = Empty(targetVec - piece.forwardVec)
        board.swapPositions(piece.vector, targetVec)
        notation = createNotation(board, piece, targetVec,
            isPawn=True, capture=True)
        piece.move(targetVec)
        print("Passant")
        return notation


if __name__ == "__main__":

    # Do some testing
    pass
