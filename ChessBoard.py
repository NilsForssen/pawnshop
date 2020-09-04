from copy import deepcopy, copy
from Pieces import King, _Disabled, _Empty
from Exceptions import *
"""
Maybe make Board inherit from numpy ndarray? 
"""

class Board():
    def __init__(self, rows, cols, ruleList):
        self._board = [[_Empty() for col in range(cols)] for row in range(rows)]

        self._rows = rows
        self._cols = cols

        self.resetDicts()

        self.rules = []

        for rule in ruleList:
            self.rules.append(rule)


    @property
    def rows(self):
        return self._rows


    @property
    def columns(self):
        return self._cols


    def resetDicts(self):

        self.pieceDict = {}
        self.kingDict = {}
        self.checkDict = {}
        self.checkMateDict = {}


    def __str__(self):

        string = "\n"

        for row in self._board:
            for piece in row:
                string += str(piece) + "\t"
            string += "\n\n"

        return string


    def __setitem__(self, index, item):

        rows, cols = self._unpackIndexSlices(index)

        idxList = []

        for rowIdx in range(rows.start, rows.stop, rows.step or 1):
            for colIdx in range(cols.start, cols.stop, cols.step or 1):
                idxList.append((rowIdx, colIdx))

        try:
            iter(item)
        except TypeError:
            item = [item]

        expectedLen = len(idxList)
        givenLen = len(item) or 1

        if expectedLen != givenLen:
            raise ValueError("List index expected {0} values to unpack but {1} were given".format(expectedLen, givenLen))

        for i, (row, col) in enumerate(idxList):

            if isinstance(self._board[row][col], _Disabled):
                raise DisabledError("Position {0} of board is disabled and thus unavailible".format((row, col)))

            item1 = self._board[row][col]
            item2 = item[i]

            self._board[row][col] = item2

            if not isinstance(item2, _Empty):

                if isinstance(item1, _Empty):
                    self._addPiece(item2, (row, col))
                else:
                    self.removePiece(item1)
                    
                    if len(self.pieceDict.values()) == 0:
                        self._addPiece(item2, (row, col))
                    else:
                        for pList in self.pieceDict.values():
                            if item2 not in pList:
                                self._addPiece(item[i], (row, col))
                                break
                            
            else:
                
                self.removePiece(item1)


    def __getitem__(self, index): 

        rows, cols = self._unpackIndexSlices(index)

        res = []

        for rowIdx in range(rows.start, rows.stop, rows.step or 1 ):
            for colIdx in range(cols.start, cols.stop, cols.step or 1):
                res.append(self._board[rowIdx][colIdx])


        if len(res) == 1: return res.pop()
        else: return res


    def _unpackIndexSlices(self, idx):
        try:
            r, c = idx
        except (TypeError, ValueError):
            raise ValueError("Index position must be 2-dimensional.") from None

        if type(r) is not slice: r = slice(r, r+1)
        if type(c) is not slice: c = slice(c, c+1)

        return r, c


    def disablePositions(self, posList):
        for pos in posList:
            self[pos] = _Disabled()


    def isEmpty(self, pos):
        return isinstance(self[pos], _Empty)


    def evalBoard(self):
        return dict([(k, 0) for k in self.colorList])


    def _addPiece(self, piece, pos):

        if not piece.color in self.pieceDict:
            self.pieceDict[piece.color] = []
            self.kingDict[piece.color] = []
            self.checkDict[piece.color] = False
            self.checkMateDict[piece.color] = False

        self.pieceDict[piece.color].append(piece)

        if isinstance(piece, King):
            self.kingDict[piece.color].append(piece)

        piece.position = pos


    def removePiece(self, piece):

        try:
            self.pieceDict[piece.color].remove(piece)

            if isinstance(piece, King) and piece in self.kingDict[piece.color]:
                self.kingDict[piece.color].remove(piece)

            if not self.pieceDict[piece.color]:
                self.pieceDict.pop(piece.color)
                self.kingDict.pop(piece.color)
                self.checkDict.pop(piece.color)
                self.checkMateDict.pop(piece.color)
        except:
            print("cant remove piece for some reason")

        piece.position = None


    def pieceSetup(self, pieceZip):

        self.resetDicts()

        for piece, pos in pieceZip:

            self[pos] = piece

        self.checkForCheck()


    def checkForCheck(self, ignoreMate=False):

        colorList = list(self.pieceDict.keys())

        for color in self.pieceDict.keys():

            hostilePieces = [piece for col, pList in self.pieceDict.items() if col != color for piece in pList]

            for hp in hostilePieces:

                hostile = hp.getMoves(self)

                for alliedKing in self.kingDict[color]:

                    if alliedKing.position in hostile:
                        self.checkDict[color] = True
                        break
                else:
                    continue

                break

            else:
                self.checkDict[color] = False


            if self.checkDict[color] and not ignoreMate:

                alliedPiecesPos = map(lambda p : p.position, self.pieceDict[color])

                for alliedPos in list(alliedPiecesPos):

                    for move in self[alliedPos].getMoves(self):

                        testBoard = deepcopy(self)

                        try:
                            testBoard.movePiece(alliedPos, move, raw=True, ignoreMate=True)

                        except Check:
                            pass

                        else:
                            self.checkMateDict[color] = False
                            break
                            
                    else:
                        continue

                    break

                else:
                    self.checkMateDict[color] = True
                    self.checkDict[color] = True
                    print(color + " in Checkmate!")
                    continue

                self.checkDict[color] = True
                print(color + " in Check!")


    def movePiece(self, startPos, targetPos, raw=False, ignoreCheck=False, ignoreMate=False, *args, **kwargs):

        piece = self[startPos]

        if isinstance(piece, _Empty):
            raise EmptyError("Given position {0} is empty".format(startPos))

        if self.checkMateDict[piece.color]:
            raise CheckMate("{0} is Checkmated!".format(piece.color))
        
        for board in (deepcopy(self), self):

            allParams = locals()
            allParams["board"] = allParams["self"]
            del allParams["self"]

            notation = ""

            if raw or targetPos in piece.getMoves(board):

                notation += piece.symbol

                if not isinstance(board[targetPos], _Empty):
                    notation += "x"
                    board[startPos], board[targetPos] = _Empty(), board[startPos]
                else:
                    board[startPos], board[targetPos] = board[targetPos], board[startPos]

                if not ignoreCheck:
                    board.checkForCheck(ignoreMate=ignoreMate)
                    if board.checkDict[piece.color]:
                        raise Check("Cannot move piece at {0} to {1} as your king is threatened.".format(startPos, targetPos))

                if board is self:
                    piece.move(targetPos)
                    
            else:
                for rule in board.rules:
                    if rule.condition(**allParams):
                        notation = rule.action(**allParams)
                        break
                else:
                    raise IllegalMove("Piece at {0} cannot move to {1}.".format(startPos, targetPos))

        return notation


def init_classic(*rules):
    board = Board(8,8, ruleList=rules)

    return board


def init_4P(*rules):
    board = Board(14,14, ruleList=rules)

    board.disablePositions([
        (0,0), (0,1), (1,0), (1,1), (0,2), (2,0), (1,2), (2,1), (2,2),
        (11,13), (13,11), (11,11), (12,11), (11,12), (12,12), (12,13), (13,12), (13,13),
        (0,13), (0,12), (0,11), (1,13), (1,12), (1,11), (2,13), (2,12), (2,11),
        (13,0), (12,0), (11,0), (13,1), (12,1), (11,1), (13,2), (12,2), (11,2)])

    return board



if __name__ == "__main__":

    thisBoard = Board(8,8, [])
    print(thisBoard[1:3, 1:3])
