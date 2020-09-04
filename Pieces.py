from Utils import _catchOutofBounce, _positivePos, infiRange

_directions = {
    "up": ((-1,0), (-1,1), (-1,-1)),
    "down": ((1,0), (1,1), (1,-1)), 
    "right": ((0,-1), (1,-1), (-1,-1)),
    "left": ((0,1), (1,1), (-1,1))
}

class Piece():
    def __init__(self, color, value, symbol):
        self._position = None
        self.color = color
        self.value = value
        self.symbol = symbol
        self.firstMove = True


    def __str__(self):
        return self.color[0] + self.symbol


    @property
    def position(self):
        return self._position


    @position.setter
    def position(self, pos):
        self._position = pos


    def move(self, destPos):
        self.position = destPos
        self.firstMove = False


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


    def _getMovesInLine(self, board, rowIter=infiRange(0, step=0), colIter=infiRange(0, step=0)):

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

        direction = direction.lower()
        if direction in _directions.keys():
            self.direction, self.diagonal_1, self.diagonal_2 = _directions[direction]
        else:
            raise ValueError("Given direction is not any of \"up\", \"down\", \"left\" or \"right\".")


    def getMoves(self, board):
        """
        Returns list of possible destinations
        """

        destList = []

        dest = self.getDest(*self.direction)
        if self.canWalk(dest, board):
            destList.append(dest)

            if self.firstMove:
                dest = self.getDest(*(self.direction[0]*2, self.direction[1]*2))
                if self.canWalk(dest, board):
                    destList.append(dest)

        dest = self.getDest(*self.diagonal_1)
        if self.canCapture(dest, board):
            destList.append(dest)

        dest = self.getDest(*self.diagonal_2)
        if self.canCapture(dest, board):
            destList.append(dest)

        return destList


class Rook(Piece):
    def __init__(self, color):
        super().__init__(color, 5, "R")


    def getMoves(self, board):
        """
        Returns list of possible destinations
        """

        destList = []
        
        destList.extend(self._getMovesInLine(board, rowIter=infiRange(1, step=1)))

        destList.extend(self._getMovesInLine(board, rowIter=infiRange(-1, step=-1)))

        destList.extend(self._getMovesInLine(board, colIter=infiRange(1, step=1)))

        destList.extend(self._getMovesInLine(board, colIter=infiRange(-1, step=-1)))

        return destList


class Knight(Piece):
    def __init__(self, color):
        super().__init__(color, 3, "N")


    def getMoves(self, board):
        """
        Returns list of possible destinations
        """

        destList = []

        # As with the king these offsets can be generated by an algorithm but
        # I figured this is more readable even though it requires additional memory
        offsetList = [
        (1,2),
        (1,-2),
        (-1,2),
        (-1,-2),
        (2,1),
        (2,-1),
        (-2,1),
        (-2,-1)]

        for offx, offy in offsetList:
            
            dest = self.getDest(offx, offy)
            if self.canMove(dest, board):
                destList.append(dest)

        return destList


class Bishop(Piece):
    def __init__(self, color):
        super().__init__(color, 3, "B")


    def getMoves(self, board):
        """
        Returns list of possible destinations
        """

        destList = []

        destList.extend(self._getMovesInLine(board, rowIter=infiRange(1, step=1), colIter=infiRange(1, step=1)))

        destList.extend(self._getMovesInLine(board, rowIter=infiRange(1, step=1), colIter=infiRange(-1, step=-1)))

        destList.extend(self._getMovesInLine(board, rowIter=infiRange(-1, step=-1), colIter=infiRange(1, step=1)))

        destList.extend(self._getMovesInLine(board, rowIter=infiRange(-1, step=-1), colIter=infiRange(-1, step=-1)))

        return destList


class King(Piece):
    def __init__(self, color):
        super().__init__(color, int(1e10), "K")


    def getMoves(self, board):
        """
        Returns list of possible destinations
        """

        destList = []

        # As with the knight these offsets can be generated by an algorithm but
        # I figured this is more readable even though it requires additional memory
        offsetList = [
        (1,0),
        (1,1),
        (0,1),
        (-1,1),
        (-1,0),
        (-1,-1),
        (0,-1),
        (1,-1)]

        for offx, offy in offsetList:

            dest = self.getDest(offx, offy)
            if self.canMove(dest, board):
                destList.append(dest)

        return destList


class Queen(Piece):
    def __init__(self, color):
        super().__init__(color, 9, "Q")


    def getMoves(self, board):
        """
        Returns list of possible destinations
        """

        destList = []

        destList.extend(self._getMovesInLine(board, rowIter=infiRange(1, step=1)))

        destList.extend(self._getMovesInLine(board, rowIter=infiRange(-1, step=-1)))

        destList.extend(self._getMovesInLine(board, colIter=infiRange(1, step=1)))

        destList.extend(self._getMovesInLine(board, colIter=infiRange(-1, step=-1)))

        destList.extend(self._getMovesInLine(board, rowIter=infiRange(1, step=1), colIter=infiRange(1, step=1)))

        destList.extend(self._getMovesInLine(board, rowIter=infiRange(1, step=1), colIter=infiRange(-1, step=-1)))

        destList.extend(self._getMovesInLine(board, rowIter=infiRange(-1, step=-1), colIter=infiRange(1, step=1)))

        destList.extend(self._getMovesInLine(board, rowIter=infiRange(-1, step=-1), colIter=infiRange(-1, step=-1)))

        return destList


class _Disabled():
    def __str__(self):
        return " "


class _Empty():
    def __str__(self):
        return "_"
