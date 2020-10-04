from Pieces import King, Rook, Pawn, _Empty
from abc import ABC, abstractclassmethod
from Utils import createNotation

class Move(ABC):

    @abstractclassmethod
    def pieceCondition(thisMove, startPiece) -> bool:
        """Test if piece satisfies move requirement"""
        raise NotImplementedError

    @abstractclassmethod
    def getDestinations(thisMove, startPiece, board) -> list:
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
    def getDestinations(thisMove, startPiece, board):
        return startPiece.getStandardMoves(board)

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
            isPawn=isinstance(startPiece, Pawn), capture=capture
        )

        startPiece.move(targetPos)

        return notation


class _Castling(Move):

    @classmethod
    def pieceCondition(thisMove, piece):
        return piece.firstMove and isinstance(piece, King)

    @classmethod
    def action(thisMove, startPiece, target, board):
        for rook in thisMove.findRooks(piece, board):
            between = thisMove.findBetween(piece.position, rook.position)
            if target in between:
                kingTarget, rookTarget = thisMove.getTarget(between)
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


class Castle_K(_Castling):

    @classmethod
    def getDestinations(thisMove, piece, board):
        destList = []
        for rook in thisMove.findRooks(piece, board):
            between = thisMove.findBetween(piece.position, rook.position)
            if thisMove.emptyBetween(between) and not between % 2:
                kingTarget, _ = thisMoves.getTargets(between)
                destList.append(kingTarget)
        return destList

    @classmethod
    def action(thisMove, *args, **kwargs):
        super().ation(*args, **kwargs)
        return "0-0"


class Castle_Q(_Castling):

    @classmethod
    def getDestinations(thisMove, piece, board):
        destList = []
        for rook in thisMove.findRooks(piece, board):
            between = thisMove.findBetweenn(piece.position, rook.position)
            if thisMove.emptyBetween(between) and between % 2:
                kingTarget, _ thisMove.getTargets(between)
                destList.append(kingTarget)
        return destList

    @classmethod
    def action(thisMove, *args, **kwargs):
        super().action(*args, **kwargs)
        return "0-0-0"


# class _Castling(Move):

#     def pieceConditions(p1, p2):
#         return (isinstance(p1, King) and isinstance(p2, Rook)) and p1.firstMove and p2.firstMove and p1.color == p2.color

#     def posConditions(pos1, pos2):
#         return bool(pos2[0] - pos1[0]) != bool(pos2[1] - pos1[1]) and (not pos2[0] - pos1[0] or not pos2[1] - pos1[1])

#     def findBetween(pos1, pos2):

#         rowStep = pos1[0] - pos2[0] and (1, -1)[pos1[0] - pos2[0] < 0]
#         colStep = pos1[1] - pos2[1] and (1, -1)[pos1[1] - pos2[1] < 0]

#         if not rowStep:
#             colRange = range(pos2[1] + colStep, pos1[1], colStep)
#             rowRange = [pos1[0]]*len(colRange)
#         else:
#             rowRange = range(pos2[0] + rowStep, pos1[0], rowStep)
#             colRange = [pos1[1]]*len(rowRange)

#         return tuple(zip(rowRange, colRange))

#     def emptyBetween(board, between):
#         for pos in between:

#             if not isinstance(board[pos], _Empty):
#                 return False
#         else:
#             return True

#     def getTarget(between):

#         if not len(between) % 2:
#             target1 = between[int((len(between)/2)-1)]
#             target2 = between[int((len(between)/2))]

#         else:
#             target1 = between[int((len(between)/2) - 0.5)]
#             target2 = between[int((len(between)/2) + 0.5)]

#         return (target1, target2)

#     def pathNotThreatened(board, path, color):
#         for pos in path:
#             if board.isThreatened(pos, color):
#                 return False
#         else:
#             return True

#     @classmethod
#     def condition(thisMove, board, startPos, targetPos, startPiece, targetPiece, between, ignoreCheck, **kwargs):

#         if thisMove.pieceConditions(startPiece, targetPiece) and thisMove.posConditions(startPos, targetPos) and (ignoreCheck or not board.checkDict[startPiece.color]):

#                 kingTarget, _ = thisMove.getTarget(between)

#                 kingPath = thisMove.findBetween(startPos, kingTarget)

#                 return thisMove.emptyBetween(board, between) and thisMove.pathNotThreatened(board, kingPath, startPiece.color)

#         return False


#     @classmethod
#     def action(thisMove, board, startPos, targetPos, startPiece, targetPiece, **kwargs):

#         between = thisMove.findBetween(startPos, targetPos)

#         kingTarget, rookTarget = thisMove.getTarget(between)

#         board.swapPositions(startPos, kingTarget)
#         board.swapPositions(targetPos, rookTarget)
#         # board[startPos], board[kingTarget] = board[kingTarget], startPiece
#         # board[targetPos], board[rookTarget] = board[rookTarget], targetPiece

#         startPiece.move(kingTarget)
#         targetPiece.move(rookTarget)


# class Castle_K(_Castling):

#     @classmethod
#     def condition(thisMove, **kwargs):
#         between = thisMove.findBetween(kwargs["startPos"], kwargs["targetPos"])
#         if not len(between) % 2:
#             return super().condition(between=between, **kwargs)


#     @classmethod
#     def action(thisMove, **kwargs):
#         super().ation(**kwargs)
#         return "0-0"


# class Castle_Q(_Castling):

#     @classmethod
#     def condition(thisMove, **kwargs):
#         between = thisMove.findBetween(kwargs["startPos"], kwargs["targetPos"])
#         if len(between) % 2:
#             return super().condition(between=between, **kwargs)


#     @classmethod
#     def action(thisMove, **kwargs):
#         super().action(**kwargs)
#         return "0-0-0"
class En_Passant(Move):

    @classmethod
    def pieceCondition(thisMove, piece):
        return isinstance(piece, Pawn)

    @classmethod
    def getDestinations(thisMove, piece, board):

        return destList

    @classmethod
    def action(thisMove, startPiece, targetPos, board):

        return

class En_Passant(Move):

    @classmethod
    def condition(thisMove, board, startPiece, targetPiece, startPos, targetPos, **kwargs):
        if isinstance(startPiece, Pawn) and isinstance(targetPiece, _Empty):

            for diagonal in (startPiece.diagonal_1, startPiece.diagonal_2):

                if targetPos == startPiece.getDest(*diagonal):

                    nextTo = (startPos[0] - startPiece.forward[0] + diagonal[0], startPos[1] - startPiece.forward[1] + diagonal[1])
                    if isinstance(board[nextTo], Pawn) and board[nextTo].passed:
                        return True

        return False


    @classmethod
    def action(thisMove, **kwargs):
        print("action")
        return "hehe"


if __name__ == "__main__":

    # Do some testing
    pass

test=Standard()
test.pieceCondition((((()))))
