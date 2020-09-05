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


class Castle_K(Move):

    def pieceConditions(p1, p2):

        return (isinstance(p1, King) and isinstance(p2, Rook)) and p1.firstMove and p2.firstMove


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
    

    @classmethod
    def condition(move, board, startPos, targetPos, **kwargs):

        piece1 = board[startPos]
        piece2 = board[targetPos]

        if move.pieceConditions(piece1, piece2):

            if bool(targetPos[0] - startPos[0]) != bool(targetPos[1] - startPos[1]) and (not targetPos[0] - startPos[0] or not targetPos[1] - startPos[1]):

                between = move.findBetween(startPos, targetPos)

                for pos in between:

                    if not isinstance(board[pos], _Empty):
                        break
                else:
                    return True

        return False


    @classmethod
    def action(move, board, startPos, targetPos, **kwargs):

        between = tuple(move.findBetween(startPos, targetPos))

        piece1 = board[startPos]
        piece2 = board[targetPos]

        if len(between) % 2 == 0:
            target1 = between[int((len(between)/2)-1)]
            target2 = between[int((len(between)/2))]

        else:
            target1 = between[int((len(between)/2) - 0.5)]
            target2 = between[int((len(between)/2) + 0.5)]

        board[startPos], board[target1] = board[target1], board[startPos]
        board[targetPos], board[target2] = board[target2], board[targetPos]

        return "O-O"


class Castle_Q(Castle_K):

    @classmethod
    def action(move, **kwargs):

        super().action(**kwargs)
        return "O-O-O"


class En_Passant(Move):

    def condition(**kwargs):
        return True 

    def action(board, *kwargs):
        return notation 