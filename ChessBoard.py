from copy import deepcopy, copy
from Pieces import King, _Disabled, _Empty
from Exceptions import *
from Utils import countAlpha

class Board():
    def __init__(self, rows, cols, moveList):
        self._board = [[_Empty() for col in range(cols)] for row in range(rows)]

        self._rows = rows
        self._cols = cols

        self.resetDicts()

        self.moves = []
        self.history = []

        for move in moveList:
            self.moves.append(move)


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
                raise DisabledError((row, col))

            item1 = self._board[row][col]
            item2 = item[i]

            if not isinstance(item2, _Disabled):

                if not isinstance(item1, _Empty):
                    self._removePiece(item1)

                if not isinstance(item2, _Empty):

                    if item2 in [p for pList in self.pieceDict.values() for p in pList]:   
                        pass
                    else:
                        self._addPiece(item2, (row, col))

            self._board[row][col] = item2


    def swapPositions(self, pos1, pos2):

        self._board[pos1[0]][pos1[1]], self._board[pos2[0]][pos2[1]] = self._board[pos2[0]][pos2[1]], self._board[pos1[0]][pos1[1]]


    def __getitem__(self, index): 

        rows, cols = self._unpackIndexSlices(index)

        res = []

        for rowIdx in range(rows.start, rows.stop, rows.step or 1 ):
            for colIdx in range(cols.start, cols.stop, cols.step or 1):
                if isinstance(self._board[rowIdx][colIdx], _Disabled):
                    raise DisabledError((rowIdx, colIdx))
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


    def _removePiece(self, piece):

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


    def isThreatened(self, pos, alliedColor):

        hostilePieces = [piece for col, pList in self.pieceDict.items() if col != alliedColor for piece in pList]

        for hp in hostilePieces:
            hostile = hp.getMoves(self)
            if pos in hostile:
                return True
        else:
            return False


    def checkForCheck(self, ignoreMate=False):

        colorList = list(self.pieceDict.keys())

        for color in self.pieceDict.keys():

            for alliedKing in self.kingDict[color]:

                if self.isThreatened(alliedKing.position, color):
                    self.checkDict[color] = True
                    break
            else:
                self.checkDict[color] = False


            if self.checkDict[color] and not ignoreMate:

                alliedPiecesPos = map(lambda p : p.position, self.pieceDict[color])

                for alliedPos in list(alliedPiecesPos):

                    for move in self[alliedPos].getMoves(self):

                        try:
                            self.movePiece(alliedPos, move, raw=True, ignoreMate=True, testMove=True, checkForMate=False)

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


    def movePiece(self, startPos, targetPos, raw=False, ignoreCheck=False, ignoreMate=False, testMove=False, checkForCheck=True, checkForMate=True, **kwargs):

        startPiece = self[startPos]

        if isinstance(startPiece, _Empty):
            raise EmptyError(startPos)

        if self.checkMateDict[startPiece.color] and not ignoreMate:
            raise CheckMate(startPiece.color)

        allParams = locals()

        del allParams["self"]

        for board in (deepcopy(self), self):

            allParams["startPiece"] = board[startPos]
            allParams["targetPiece"] = board[targetPos]

            allParams["board"] = board

            for rule in board.moves:
                if raw or rule.condition(**allParams):
                    notation = rule.action(**allParams)

                    if checkForCheck:
                        board.checkForCheck(ignoreMate=not checkForMate)

                        if not ignoreCheck and board.checkDict[startPiece.color]:
                            raise Check(startPos, targetPos)

                    break
            else:
                raise IllegalMove(startPos, targetPos)

            if testMove:
                break

        if not testMove:
            for color in self.checkDict.keys():
                if self.checkMateDict[color]:
                    print(f"{color} in Checkmate!")
                    if not "#" in notation: 
                        notation += "#"

                elif self.checkDict[color]:
                    print(f"{color} in Check!")
                    if not "+" in notation: 
                        notation += "+"

            for piece in [p for pList in self.pieceDict.values() for p in pList]:
                
                if not piece is startPiece:
                    piece.postAction(board)

            self.history.append(notation)

        return notation


def init_classic(*moves):
    board = Board(8,8, moveList=moves)

    return board


def init_4P(*moves):
    board = Board(14,14, moveList=moves)

    board.disablePositions([
        (0,0), (0,1), (1,0), (1,1), (0,2), (2,0), (1,2), (2,1), (2,2),
        (11,13), (13,11), (11,11), (12,11), (11,12), (12,12), (12,13), (13,12), (13,13),
        (0,13), (0,12), (0,11), (1,13), (1,12), (1,11), (2,13), (2,12), (2,11),
        (13,0), (12,0), (11,0), (13,1), (12,1), (11,1), (13,2), (12,2), (11,2)])

    return board



if __name__ == "__main__":

    # Do some testing
    pass