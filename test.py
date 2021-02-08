from pawnshop import ChessBoard, ChessVector


board = ChessBoard.initClassic()
vector = ChessVector.ChessVector

board.getKings()

board.movePiece(vector((1, 1)), vector((2, 1)), ignoreOrder=True)

board.checkForCheck()

print(board.getChecks(), board.getCheckmates(), board.getKings())
