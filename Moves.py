from Pieces import King, Rook, Pawn, _Empty
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
    def action(thisMove, startPiece, targetPos, board):
        capture = False
        targetPiece = board[targetPos]

        if not isinstance(targetPiece, _Empty):
            capture = True
            board.swapPositions(startPiece.position, targetPos)
            board[startPiece.position] = _Empty()
        else:
            board.swapPositions(startPiece.position, targetPos)

        notation = createNotation(
            board, startPiece, targetPos,
            isPawn=isinstance(startPiece, Pawn), capture=capture)
        startPiece.move(targetPos)
        return notation


class _Castling(Move):

    @classmethod
    def pieceCondition(thisMove, piece):
        return piece.firstMove and isinstance(piece, King)

    @classmethod
    def action(thisMove, startPiece, targetPos, board):
        for rook in thisMove.findRooks(startPiece, board):
            between = thisMove.findBetween(startPiece.position, rook.position)
            if targetPos in between:
                kingTarget, rookTarget = thisMove.getTargets(between)
                board.swapPositions(startPiece.position, kingTarget)
                board.swapPositions(rook.position, rookTarget)
                startPiece.move(kingTarget)
                rook.move(rookTarget)
                break
        else:
            raise ValueError(f"Piece cannot move to {targetPos}")

    def findBetween(pos1, pos2):
        rowStep = pos1[0] - pos2[0] and (1, -1)[pos1[0] - pos2[0] < 0]
        colStep = pos1[1] - pos2[1] and (1, -1)[pos1[1] - pos2[1] < 0]

        if not rowStep:
            colRange = range(pos2[1] + colStep, pos1[1], colStep)
            rowRange = [pos1[0]]*len(colRange)
        else:
            rowRange = range(pos2[0] + rowStep, pos1[0], rowStep)
            colRange = [pos1[1]]*len(rowRange)

        return tuple(zip(rowRange, colRange))

    def emptyBetween(board, between):
        for pos in between:
            if not isinstance(board[pos], _Empty):
                return False
        else:
            return True

    def findRooks(piece, board):
        def posCondition(pos1, pos2):
            return bool(pos2[0] - pos1[0]) != bool(pos2[1] - pos1[1]) and (not pos2[0] - pos1[0] or not pos2[1] - pos1[1])

        rookList = []
        for p in board.pieceDict[piece.color]:
            if isinstance(p, Rook) and p.firstMove and posCondition(piece.position, p.position):
                rookList.append(p)
        return rookList

    def getTargets(between):
        if not len(between) % 2:
            target1 = between[int((len(between)/2)-1)]
            target2 = between[int((len(between)/2))]
        else:
            target1 = between[int((len(between)/2) - 0.5)]
            target2 = between[int((len(between)/2) + 0.5)]
        return (target1, target2)


class CastleK(_Castling):

    @classmethod
    def getDestinations(thisMove, piece, board):
        destList = []
        for rook in thisMove.findRooks(piece, board):
            between = thisMove.findBetween(piece.position, rook.position)
            if thisMove.emptyBetween(board, between) and not len(between) % 2:
                kingTarget, _ = thisMoves.getTargets(between)
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
            between = thisMove.findBetween(piece.position, rook.position)
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
        for diag in (piece.diagL, piece.diagR):
            offset = thisMove.getPassed(piece.forward, diag)
            pos = piece.getDest(*offset)
            try:
                if isinstance(board[pos], Pawn) and board[pos].passed:
                    destList.append(piece.getDest(*diag))
            except IndexError:
                pass
        return destList

    @classmethod
    def action(thisMove, startPiece, targetPos, board):
        board[thisMove.getPassed(startPiece.forward, targetPos)] = _Empty()
        board.swapPositions(startPiece.position, targetPos)
        notation = createNotation(board, startPiece, targetPos, 
            isPawn=True, capture=True)
        startPiece.move(targetPos)
        return notation

    def getPassed(forw, diag):
        return (diag[0] - forw[0], diag[1] - forw[1])


if __name__ == "__main__":

    # Do some testing
    pass
