from Pieces import King, Rook, _Empty
from abc import ABC, abstractclassmethod


class Move(ABC):

    @abstractclassmethod
    def condition(rule, **kwargs) -> bool:
        """
        returns whether the rule is aplicable on the given move or not
        """

        raise NotImplementedError("condition() not yet implmented in rule.")

    @abstractclassmethod
    def action(rule, **kwargs) -> str:
        """
        Proceeds to carry out the move

        returns the move-notation 
        """
        raise NotImplementedError("action() not yet implemented in rule.")

    @classmethod
    def finishMove(rule, startPiece, targetPos, **kwargs):
        """
        Move the piece instances

        This method is called after action() has been validated
        """
        startPiece.move(targetPos)


class Standard(Move):

    @classmethod
    def condition(rule, board, startPiece, targetPos, **kwargs):

        returned = targetPos in startPiece.getMoves(board)

        return returned

    @classmethod
    def action(rule, board, startPiece, targetPiece, startPos, targetPos, **kwargs):

        notation = startPiece.symbol

        print("DO SOME ACTION!")

        if not isinstance(targetPiece, _Empty):
            notation += "x"
        else:
            pass

        notation += str(targetPos)

        return notation


class Castle_K(Move):

    def findBetween(pos1, pos2):

        rowStep = pos1[0] - pos2[0] and (1, -1)[pos1[0] - pos2[0] < 0]
        colStep = pos1[1] - pos2[1] and (1, -1)[pos1[1] - pos2[1] < 0]

        if not rowStep: 
            colRange = range(pos2[1] + colStep, pos1[1], colStep)
            rowRange = [pos1[0]]*len(colRange)
        elif not colStep:
            rowRange = range(pos2[0] + rowStep, pos1[0], rowStep)
            colRange = [pos1[1]]*len(rowRange)

        return zip(rowRange, colRange)


    def pieceConditions(p1, p2):
        return (isinstance(p1, King) and isinstance(p2, Rook)) and p1.firstMove and p2.firstMove


    def posCondition(pos1, pos2):
        return bool(pos2[0] - pos1[0]) != bool(pos2[1] - pos1[1]) and (not pos2[0] - pos1[0] or not pos2[1] - pos1[1])


    def emptyBetween(board, posZip):
        for pos in posZip:

            if not isinstance(board[pos], _Empty):
                return False
        else:
            return True


    @classmethod
    def condition(move, board, startPos, targetPos, startPiece, targetPiece, **kwargs):

        if move.pieceConditions(startPiece, targetPiece) and move.posConditions(startPos, targetPos):
                
                between = move.findBetween(startPos, targetPos)

                return emptyBetween(board, between) and not len(between) % 2

        return False


    @classmethod
    def action(move, board, startPos, targetPos, **kwargs):

        between = tuple(move.findBetween(startPos, targetPos))

        piece1 = board[startPos]
        piece2 = board[targetPos]

        if not len(between) % 2:
            target1 = between[int((len(between)/2)-1)]
            target2 = between[int((len(between)/2))]

        else:
            target1 = between[int((len(between)/2) - 0.5)]
            target2 = between[int((len(between)/2) + 0.5)]

        print("DO SOME ACTION!")

        return "O-O"


class Castle_Q(Castle_K):

    @classmethod
    def condition(move, board, startPos, targetPos, startPiece, targetPiece, **kwargs):
        if move.pieceConditions(startPiece, targetPiece) and move.posConditions(startPos, targetPos):
                
            between = move.findBetween(startPos, targetPos)

            return emptyBetween(board, between) and len(between) % 2

        return False


    @classmethod
    def action(move, **kwargs):

        super().action(**kwargs)
        return "O-O-O"


class En_Passant(Move):

    def condition(**kwargs):
        return False 

    def action(board, *kwargs):
        return notation 