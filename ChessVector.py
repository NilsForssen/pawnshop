from Utils import countAlpha, inverseIdx, toAlpha


class ChessVector(object):
    def __init__(self, position, board=None):
        """
        Initialize Vector with optional col and row position.
        Vector position can also be set later by changing col/row
        or using setPos method with a position string.

        DO NOT CHANGE VECTOR IN RUNTIME!
        """

        self._row = 0
        self._col = 0

        if isinstance(position, tuple):
            row, col = position
            self.row = int(row)
            self.col = int(col)
        elif isinstance(position, str) and not board is None:
            position = position.lower()
            for char in position:
                if char.isdigit():
                    i = position.find(char)
                    if i == 0:
                        raise ValueError("Position does not include column!")
                    alpha = position[:i]
                    num = position[i::]
                    row = board.rows - int(num)
                    for n, a in countAlpha():
                        if a == alpha:
                            col = n
                            break
                    else:
                        continue
                    break
            else:
                raise ValueError("position does not include row!")
            self.row = row
            self.col = col
        else:
            raise ValueError("Position is not a string or a tuple!")

    @property
    def col(self):
        return self._col

    @col.setter
    def col(self, newCol):
        self._col = newCol

    @property
    def row(self):
        return self._row

    @row.setter
    def row(self, newRow):
        self._row = newRow

    def __sub__(self, other):
        if isinstance(other, ChessVector):
            return ChessVector((self.row - other.row, self.col - other.col))
        else:
            return ChessVector((self.row - other, self.col - other))

    def __rsub__(self, other):
        if isinstance(other, ChessVector):
            return ChessVector((other.row - self.row, other.col - self.col))
        else:
            raise ValueError(f"Cannot subtract {type(self)} from non-{type(self)}!")

    def __add__(self, other):
        if isinstance(other, ChessVector):
            return ChessVector((self.row + other.row, self.col + other.col))
        else:
            return ChessVector((self.row + other, self.col + other))

    def __radd__(self, other):
        if isinstance(other, ChessVector):
            return ChessVector((other.row + self.row, other.col + self.col))
        else:
            raise ValueError(f"Cannot add {type(self)} to non-{type(self)}!")

    def __mul__(self, other):
        if isinstance(other, ChessVector):
            return ChessVector((self.row * other.row, self.col * other.col))
        else:
            return ChessVector((self.row * other, self.col * other))

    def __rmul__(self, other):
        if isinstance(other, ChessVector):
            return ChessVector((other.row * self.row, other.col * self.col))
        else:
            raise ValueError(f"Cannot multiply non-{type(self)} by {type(self)}!")

    def __div__(self, other):
        if isinstance(other, ChessVector):
            return ChessVector((self.row / other.row, self.col / other.col))
        else:
            return ChessVector((self.row / other, self.col / other))

    def __rdiv__(self, other):
        if isinstance(other, ChessVector):
            return ChessVector((other.row / self.row, other.col / self.col))
        else:
            raise ValueError(f"Cannot divide non-{type(self)} by {type(self)}!")

    def __neg__(self):
        return ChessVector((-self.row, -self.col))

    def __pos__(self):
        return ChessVector((+self.row, +self.col))

    def __eq__(self, other):
        if isinstance(other, ChessVector):
            return self.row == other.row and self.col == other.col
        else:
            raise ValueError(f"Cannot compare {type(self)} with {type(other)}!")

    def __ne__(self, other):
        return not self == other

    def __lt__(self, other):
        if isinstance(other, ChessVector):
            return self.row < other.row and self.col < other.col
        else:
            raise ValueError(f"Cannot compare {type(self)} with {type(other)}!")

    def __gt__(self, other):
        return not self < other

    def __le__(self, other):
        return self < other or self == other

    def __ge__(self, other):
        return self > other or self == other

    def __repr__(self):
        return str((self.row, self.col))

    def __str__(self):
        return str((self.row, self.col))

    def tuple(self):
        return (self._row, self._col)

    def getStr(self, board):
        notation = ""
        notation += toAlpha(self.col)
        notation += inverseIdx(self.row, board)
        return notation

    def matches(self, otherVecs):
        for vec in otherVecs:
            if self.row == vec.row and self.col == vec.col:
                return True
        else:
            return False


if __name__ == "__main__":

    # Do some testing
    pass
