# ChessBoard.py

import json
import os
from copy import deepcopy, copy
from functools import wraps
from typing import Union, List, Dict, Generator

from .ChessVector import ChessVector
from .Pieces import *
from .Moves import *
from .configurations import ClassicConfig, FourPlayerConfig
from .Utils import countAlpha, getResourcePath
from .Exceptions import *


def _defaultColors(func):
    @wraps(func)
    def wrapper(self, *colors):
        if not colors:
            colors = self.getColors()
        returned = func(self, *colors)
        if isinstance(returned, dict) and len(returned) == 1:
            returned = returned.pop(*colors)
        return returned
    return wrapper


class Board():
    """Board object for storing and moving pieces

    :param config: Board configuration (defaults to emtpy board)
    """

    def __init__(self, config={}):

        self._board = []
        with open(getResourcePath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "configurations\\DefaultConfig.JSON")), "r") as default:
            dConfig = json.load(default)

            self._rows = config.get("rows") or dConfig.get("rows")
            self._cols = config.get("cols") or dConfig.get("cols")
            self._pieces = config.get("pieces") or dConfig.get("pieces")
            self._moves = config.get("moves") or dConfig.get("moves")
            self._promoteTo = config.get("promoteTo") or dConfig.get("promoteTo")
            self._promoteFrom = config.get("promoteFrom") or dConfig.get("promoteFrom")
            self._promoteAt = config.get("promoteAt") or dConfig.get("promteAt")
            self._turnorder = config.get("turnorder") or dConfig.get("turnorder")

            try:
                self.currentTurn = self._turnorder[0]
            except IndexError:
                self.currentTurn = None
            self._board = [[Empty(ChessVector((row, col))) for col in range(self._cols)] for row in range(self._rows)]

            for color, pieceList in self._pieces.items():
                for piece in pieceList:
                    self[piece.vector] = piece

            for vec in config.get("disabled") or dConfig.get("disabled"):
                self[vec] = Disabled(vec)

        self._checks = {key: False for key in self._pieces.keys()}
        self._checkmates = copy(self._checks)
        self._kings = {key: [piece for piece in self._pieces[key] if isinstance(piece, King)] for key in self._pieces.keys()}
        self._history = []

        self.checkForCheck()

    def __eq__(self, other):
        for p1, p2 in zip(self, other):
            if type(p1) == type(p2):
                continue
            else:
                break

        else:
            return True
        return False

    def __ne__(self, other):
        return not self == other

    def __iter__(self):
        """Iterates through all positions in board

        Use iterPieces() method to iterate through pieces of board.
        """
        for p in [p for row in self._board for p in row]:
            yield p

    def __str__(self):
        string = "\n"
        ending = "\t|\n\n\t\t__" + ("\t__" * self._cols) + "\n\n\t\t"
        alpha = countAlpha()

        for row in self._board:

            num, char = next(alpha)

            string += str(self._rows - num) + "\t|\t\t"

            for piece in row:
                string += str(piece) + "\t"

            string += "\n\n"

            ending += "\t" + char.upper()

        return string + ending + "\n\n"

    def __setitem__(self, index, item):

        try:
            iter(item)
        except TypeError:
            item = [item]

        try:
            iter(index)
        except TypeError:
            index = [index]

        if len(index) != len(item):
            raise ValueError("List index expected {0} values to unpack but {1} were given".format(
                len(item), len(index)))

        for i, vec in enumerate(index):

            if isinstance(self._board[vec.row][vec.col], Disabled):
                raise DisabledError(vec.getStr(self))

            item1 = self._board[vec.row][vec.col]
            item2 = item[i]

            if not isinstance(item2, Disabled):

                if not isinstance(item1, Empty):
                    self._removePiece(item1)

                if not isinstance(item2, Empty):

                    if item2 in self.iterPieces(item2.color):
                        pass
                    else:
                        self._addPiece(item2, vec)

            self._board[vec.row][vec.col] = item2

    def __getitem__(self, index):
        res = []

        try:
            iter(index)
        except TypeError:
            index = [index]

        for vec in index:
            if isinstance(self._board[vec.row][vec.col], Disabled):
                raise DisabledError(vec.getStr(self))
            res.append(self._board[vec.row][vec.col])

        if len(res) == 1:
            return res.pop()
        else:
            return res

    def getRows(self) -> int:
        """Get rows in board

        :returns: Number of rows in board
        :rtype: ``int``
        """
        return self._rows

    def getCols(self) -> int:
        """Get columns in board

        :returns: Number of columns in board
        :rtype: ``int``
        """
        return self._cols

    def getHistory(self) -> list:
        """Get history list of board

        :returns: History of board
        :rtype: ``list``
        """
        return self._history


    def getTurnorder(self) -> list:
        """Get turnorder list of board

        :returns: Turnorder of board
        :rtype: ``list``
        """
        return self._turnorder

    @_defaultColors
    def getChecks(self, *colors: str) -> Union[bool, Dict[str, bool]]:
        """Get checks in board

        If more than one color is given, this returns a ``dict``
        with a ``bool`` corresponding to each color.

        :param *colors: Colors to return
        :returns: If colors are in check or not
        :rtype: ``bool`` or ``dict``
        """
        return {col: self._checks[col] for col in colors}

    @_defaultColors
    def getCheckmates(self, *colors: str) -> Union[bool, Dict[str, bool]]:
        """Get checkmates in board

        If more than one color is given, this returns a ``dict``
        with a ``bool`` corresponding to each color.

        :param *colors: Colors to return
        :returns: If colors are in checkmate or not
        :rtype: ``bool`` or ``dict``
        """
        return {col: self._checkmates[col] for col in colors}

    @_defaultColors
    def getKings(self, *colors: str) -> Union[List[King], Dict[str, List[King]]]:
        """Get kings in board

        If more than one color is given, this returns a ``dict``
        with a ``list`` of kings corresponding to each color.

        :param *colors: Colors to return
        :returns: All kings of colors in board
        :rtype: ``list`` or ``dict``
        """
        return {col: self._kings[col] for col in colors}

    @_defaultColors
    def getMoves(self, *colors: str) -> Union[List[Move], Dict[str, List[Move]]]:
        """Get moves of board

        If more than one color is given, this returns a ``dict``
        with a ``list`` of moves corresponding to each color.

        :param *colors: Colors to return
        :returns: All moves of colors in board
        :rtype: ``list`` or ``dict``
        """
        return {col: self._moves[col] for col in colors}

    @_defaultColors
    def getPromoteAt(self, *colors: str) -> Union[int, Dict[str, int]]:
        """Get promotion position of board

        If more than one color is given, this returns a ``dict``
        with a ``int`` corresponding to each color.

        :param *colors: Colors to return
        :returns: The promotion position of colors in board
        :rtype: ``list`` or ``dict``
        """
        return {col: self._promoteAt[col] for col in colors}

    @_defaultColors
    def getPromoteFrom(self, *colors: str) -> Union[List[Piece], Dict[str, List[Piece]]]:
        """Get promotion starting pieces of board

        If more than one color is given, this returns a ``dict``
        with a ``list`` corresponding to each color.

        :param *colors: Colors to return
        :returns: The promotion starting piece types of colors in board
        :rtype: ``list`` or ``dict``
        """
        return {col: self._promoteFrom[col] for col in colors}

    @_defaultColors
    def getPromoteTo(self, *colors: str) -> Union[List[Piece], Dict[str, List[Piece]]]:
        """Get promotion target pieces of board

        If more than one color is given, this returns a ``dict``
        with a ``list`` corresponding to each color.

        :param *colors: Colors to return
        :returns: The promotion target piece types of colors in board
        :rtype: ``list`` or ``dict``
        """
        return {col: self._promoteTo[col] for col in colors}

    def getColors(self) -> List[str]:
        """Get all colors of board

        :returns: List of colors in board
        :rtype: ``list``
        """
        return self._pieces.keys()

    @_defaultColors
    def iterPieces(self, *colors: str) -> Generator[Piece, None, None]:
        """Iterate through pieces of board

        Use __iter__ to iterate through all positions of the board.

        :param *colors: Colors of pieces to iterate through (default is all colors)
        :yields: Every piece in board
        :ytype: ``generator``
        """
        for col in colors:
            for p in self._pieces[col]:
                yield p

    @_defaultColors
    def eval(self, *colors: str) -> Dict[str, int]:
        """Evaluate board

        Returns the sum of all pieces' values of colors in board

        :param *colors: Colors to evaluate (defaults to all colors of board)

        :returns: Colors with corresponding sum of pieces
        :rtype: ``dict``
        """
        return {col: sum(list(map(lambda p: p.value, list(self.iterPieces(col))))) for col in colors}

    def removeColor(self, color: str) -> None:
        """Remove color from board

        :param color: Color to remove
        """
        vectors = list(map(lambda p: p.vector, list(self.iterPieces(color))))
        self[vectors] = [Empty(vector) for vector in vectors]
        self.checkForCheck()

    def swapPositions(self, vec1: ChessVector, vec2: ChessVector) -> None:
        """Swap position of two pieces

        :param vec1: Starting position of first piece
        :param vec2: Starting position of second piece
        """
        self._board[vec1.row][vec1.col].move(vec2)
        self._board[vec2.row][vec2.col].move(vec1)
        self._board[vec1.row][vec1.col], self._board[vec2.row][vec2.col] = self._board[vec2.row][vec2.col], self._board[vec1.row][vec1.col]

    def isEmpty(self, vec: ChessVector) -> bool:
        """Check if position is empty

        :param vec: Position to check
        :returns: True if position is empty, else False
        :rtype: ``bool``
        """
        return isinstance(self[vec], Empty)

    def isThreatened(self, vec: ChessVector, alliedColor: str) -> bool:
        """Check if position is threatened by enemy pieces

        :param vector: Position to check for threats
        :param alliedColor: Color to exclude from enemy pieces
        :returns: True if position is threatened, else False
        :rtype: ``bool``
        """
        hostilePieces = [piece for col in self.getColors() if col != alliedColor for piece in self.iterPieces(col)]

        for hp in hostilePieces:
            hostile = hp.getMoves(self, ignoreCheck=True)
            if vec in hostile:
                return True
        else:
            return False

    def checkForCheck(self, checkForMate=True) -> None:
        """Check for any checks in board

        If checkForMate is True and king is in check,
        method checks if any allied pieces can move to
        interfere with the threatened check.

        :param checkForMate: Flag False to ignore checkmate (default is True)
        :returns: None, stores result in attributes ``checks`` and ``checkmates``
        """
        for color in self.getColors():

            for alliedKing in self._kings[color]:

                if self.isThreatened(alliedKing.vector, color):
                    self._checks[color] = True
                    break
            else:
                self._checks[color] = False

            if self._checks[color] and checkForMate:

                alliedPiecesPos = map(lambda p: p.vector, list(self.iterPieces(color)))

                for alliedPos in list(alliedPiecesPos):
                    for move in self[alliedPos].getMoves(self, ignoreCheck=True):
                        testBoard = deepcopy(self)
                        for pieceType in [None, *self._promoteTo[color]]:
                            try:
                                testBoard.movePiece(alliedPos, move, ignoreMate=True,
                                                    checkForMate=False, promote=pieceType,
                                                    printout=False, checkMove=False, ignoreOrder=True)
                            except PromotionError:
                                continue
                            else:
                                break

                        if testBoard._checks[color]:
                            continue
                        else:
                            self._checkmates[color] = False
                            break
                    else:
                        continue
                    break
                else:
                    self._checkmates[color] = True

    def advanceTurn(self) -> None:
        """Advance the turn according to turnorder
        """
        newidx = self._turnorder.index(self.currentTurn) + 1
        try:
            self.currentTurn = self._turnorder[newidx]
        except IndexError:
            self.currentTurn = self._turnorder[0]

    def movePiece(self, startVec: ChessVector, targetVec: ChessVector,
                  ignoreOrder=False, ignoreMate=False, ignoreCheck=False,
                  checkForCheck=True, checkForMate=True, checkMove=True,
                  printout=True, promote=None) -> str:
        """Move piece on board

        :param startVec: Position of moving piece
        :param targetVec: Destination of moving piece
        :param **Flags: Flags altering move rules, see below
        :returns: Notation of move
        :rtype: ``str``

        :**Flags:
            :ignoreOrder (False): Ignore the turnorder
            :ignoreMate (False): Ignore if any pieces are in checkmate
            :ignoreCheck (False): Ignore if any pieces are in check
            :checkForCheck (True): Check for any checks after move
            :checkForMate (True): Check for any checkmates after move
            :checkMove (True): Check if piece is able to move to destination
            :printout (True): Print the results of the move; checks, checkmates and move notation
            :promote (None): Piece type to promote to
        """

        if self.isEmpty(startVec):
            raise EmptyError(startVec.getStr(self))

        startPiece = self[startVec]

        if not ignoreOrder and self.currentTurn != startPiece.color:
            raise TurnError

        if self._checkmates[startPiece.color] and not ignoreMate:
            raise CheckMate

        if checkMove and not targetVec.matches(startPiece.getMoves(self, ignoreCheck=ignoreCheck, ignoreMate=ignoreMate)):
            raise IllegalMove(startVec.getStr(self), targetVec.getStr(self))

        for move in self._moves[startPiece.color]:
            if move.pieceCondition(startPiece):
                if targetVec in move.getDestinations(startPiece, self):
                    notation = move.action(startPiece, targetVec, self, promote)
                    if checkForCheck:
                        self.checkForCheck(checkForMate=checkForMate)
                    break

        else:
            raise IllegalMove(startVec.getStr(self), targetVec.getStr(self))

        for color in self._checks.keys():
            if self._checkmates[color]:
                if printout:
                    print(f"{color} in Checkmate!")
                if not "#" in notation:
                    notation += "#"

            elif self._checks[color]:
                if printout:
                    print(f"{color} in Check!")
                if not "+" in notation:
                    notation += "+"

        for piece in self.iterPieces():

            if not piece is startPiece:
                piece.postAction(self)

        self._history.append(notation)
        if printout:
            print(notation)

        self.advanceTurn()
        return notation

    def _addPiece(self, piece: Piece, vec: ChessVector) -> None:
        if not piece.color in self.getColors():
            self._pieces[piece.color] = []
            self._kings[piece.color] = []
            self._checks[piece.color] = False
            self._checkmates[piece.color] = False

        self._pieces[piece.color].append(piece)

        if isinstance(piece, King):
            self._kings[piece.color].append(piece)

        piece.vector = vec

    def _removePiece(self, piece: Piece) -> None:

        self._pieces[piece.color].remove(piece)

        if isinstance(piece, King) and piece in self._kings[piece.color]:
            self._kings[piece.color].remove(piece)

        if not self._pieces[piece.color]:
            del self._pieces[piece.color]
            del self._promoteTo[piece.color]
            del self._promoteFrom[piece.color]
            del self._promoteAt[piece.color]
            del self._kings[piece.color]
            del self._checks[piece.color]
            del self._checkmates[piece.color]

            self._turnorder.remove(piece.color)

        piece.vector = None


def initClassic() -> Board:
    """Initialize a chessBoard setup for 2 players, classic setup

    :returns: Classic chessboard
    :rtype: ``Board``
    """
    board = Board(deepcopy(ClassicConfig.CONFIG))
    return board


def init4P() -> Board:
    """Initialize a chessboard setup for four players

    :returns 4 player chessboard
    :rtype: ``Board``
    """
    board = Board(deepcopy(FourPlayerConfig.CONFIG))
    return board
