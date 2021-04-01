# ChessVector.py

from typing import Union, Tuple, List, TYPE_CHECKING
from .Utils import toAlpha, inverseIdx, countAlpha
# import pawnshop.ChessBoard

if TYPE_CHECKING:
    from pawnshop.ChessBoard import Board


class ChessVector(object):
    """ChessVector object

    Object to store position on chessboard
    Initialize object with position in (row, col) or string notation format
    If a string notation format is given, the board must also be given
    The vector supports common operations such as addition, multiplication with other vectors

    :param position: Tuple or string notation position on chessboard
    :param board: Board to use when determining position given by string notation (default is None)
    """

    def __init__(self, position: Union[Tuple[int, int], str], board=None):
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
                    row = board.getRows() - int(num)
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

    def tuple(self) -> Tuple[int, int]:
        """Return tuple format of vector

        :returns: (row, col) tuple
        :rType: ´´tuple´´
        """
        return (self._row, self._col)

    def getStr(self, board: "Board") -> str:
        """Return string notation format of vector

        :param board: Board to determine string position from
        :returns: string notation of vector position
        :rType: ´´str´´
        """
        notation = ""
        notation += toAlpha(self.col)
        notation += inverseIdx(self.row, board)
        return notation

    def matches(self, otherVecs: List["ChessVector"]) -> bool:
        """Check if vector matches any of other vectors

        :param otherVecs: List of other vectors
        :returns: If match is found or not
        :rType: ´´bool´´
        """
        for vec in otherVecs:
            if self.row == vec.row and self.col == vec.col:
                return True
        else:
            return False

    def copy(self) -> "ChessVector":
        """Create a new copy of this vector

        :returns: Copy of this vector
        :rType: ´´ChessVector´´
        """
        return ChessVector((self.row, self.col))


if __name__ == "__main__":

    # Do some testing
    pass
