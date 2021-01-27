from network import Network
from ChessBoard import Board
import time
from ChessVector import ChessVector

vectorList = [("b8", "a6"), ("a6", "b8")]
connection = Network()
i = 0

while True:
    time.sleep(5)
    message = connection.send("get")
    print("Message: \n\n", message)
    if isinstance(message, Board):
        board = connection.send("get")
        break
    else:
        continue

while True:
    time.sleep(5)
    payload = (ChessVector(vectorList[i][0], board), ChessVector(vectorList[i][1], board))
    board = connection.send(payload)
    print(board)

    i += 1
    if i == 100:
        connection.send("break")
