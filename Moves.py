from Pieces import King, Rook, Pawn, _Empty
from abc import ABC, abstractclassmethod
from Utils import createNotation


class Move(ABC):

    @abstractclassmethod
    def condition(thisMove, **kwargs) -> bool:
        """
        returns whether the move is aplicable on the given move or not
        """

        raise NotImplementedError("condition() not yet implmented in move.")

    @abstractclassmethod
    def action(thisMove, **kwargs) -> str:
        """
        Do the move

        returns the move-notation 
        """
        
        raise NotImplementedError("action() not yet implemented in move.")
        

class _Standard(Move):

    @classmethod
    def condition(thisMove, board, startPiece, targetPos, **kwargs):

        returned = targetPos in startPiece.getMoves(board)

        return returned

    @classmethod
    def action(thisMove, board, startPiece, targetPiece, startPos, targetPos, **kwargs):
        
        capture = False 
        if not isinstance(targetPiece, _Empty):
            capture = True
            board[startPos], board[targetPos] = _Empty(), startPiece
        else:
            board[startPos], board[targetPos] = targetPiece, startPiece

        startPiece.move(targetPos)

        return createNotation(board, startPiece, startPos, targetPos, isPawn=isinstance(startPiece, Pawn), capture=capture)


class _Castling(Move):

    def pieceConditions(p1, p2):
        return (isinstance(p1, King) and isinstance(p2, Rook)) and p1.firstMove and p2.firstMove and p1.color == p2.color

    def posConditions(pos1, pos2):
        return bool(pos2[0] - pos1[0]) != bool(pos2[1] - pos1[1]) and (not pos2[0] - pos1[0] or not pos2[1] - pos1[1])

    def findBetween(pos1, pos2):

        rowStep = pos1[0] - pos2[0] and (1, -1)[pos1[0] - pos2[0] < 0]
        colStep = pos1[1] - pos2[1] and (1, -1)[pos1[1] - pos2[1] < 0]

        if not rowStep: 
            colRange = range(pos2[1] + colStep, pos1[1], colStep)
            rowRange = [pos1[0]]*len(colRange)
        elif not colStep:
            rowRange = range(pos2[0] + rowStep, pos1[0], rowStep)
            colRange = [pos1[1]]*len(rowRange)

        return tuple(zip(rowRange, colRange))

    def emptyBetween(board, between):
        for pos in between:

            if not isinstance(board[pos], _Empty):
                return False
        else:
            return True

    def getTarget(between):

        if not len(between) % 2:
            target1 = between[int((len(between)/2)-1)]
            target2 = between[int((len(between)/2))]

        else:
            target1 = between[int((len(between)/2) - 0.5)]
            target2 = between[int((len(between)/2) + 0.5)]

        return (target1, target2)

    def pathNotThreatened(board, path, color):
        for pos in path:
            if board.isThreatened(pos, color):
                return False
        else:
            return True

    @classmethod
    def condition(thisMove, board, startPos, targetPos, startPiece, targetPiece, between, ignoreCheck, **kwargs):

        if thisMove.pieceConditions(startPiece, targetPiece) and thisMove.posConditions(startPos, targetPos) and (ignoreCheck or not board.checkDict[startPiece.color]):

                kingTarget, _ = thisMove.getTarget(between)

                kingPath = thisMove.findBetween(startPos, kingTarget)

                return thisMove.emptyBetween(board, between) and thisMove.pathNotThreatened(board, kingPath, startPiece.color)

        return False


    @classmethod
    def action(thisMove, board, startPos, targetPos, startPiece, targetPiece, **kwargs):

        between = thisMove.findBetween(startPos, targetPos)

        kingTarget, rookTarget = thisMove.getTarget(between)

        board[startPos], board[kingTarget] = board[kingTarget], startPiece
        board[targetPos], board[rookTarget] = board[rookTarget], targetPiece

        startPiece.move(kingTarget)
        startPiece.move(rookTarget)


class Castle_K(_Castling):

    @classmethod
    def condition(thisMove, **kwargs):
        between = thisMove.findBetween(kwargs["startPos"], kwargs["targetPos"])
        if not len(between) % 2:
            return super().condition(between=between, **kwargs)


    @classmethod
    def action(thisMove, **kwargs):
        super().ation(**kwargs)
        return "0-0"


class Castle_Q(_Castling):

    @classmethod
    def condition(thisMove, **kwargs):
        between = thisMove.findBetween(kwargs["startPos"], kwargs["targetPos"])
        if len(between) % 2:
            return super().condition(between=between, **kwargs)


    @classmethod
    def action(thisMove, **kwargs):
        super().action(**kwargs)
        return "0-0-0"


class En_Passant(Move):

    def condition(**kwargs):
        return False 

    def action(board, *kwargs):
        return notation 