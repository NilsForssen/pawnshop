import socket
import pickle
import _thread
from ChessBoard import initClassic
from Exceptions import PromotionError, Illegal

server = "0.0.0.0"
port = 10000

MANDATORYFLAGS = {
    "ignoreOrder": False,
    "ignoreMate": False,
    "ignoreCheck": False,
    "checkForCheck": True,
    "checkForMate": True,
    "checkMove": True,
    "printOut": False
}

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

s.bind((server, port))
s.settimeout(1.0)

s.listen()
print("Waiting for connection, server started")
ALLGAMES = {}


def client(conn, addr, color, gameID):
    conn.send(pickle.dumps(color))
    global players
    global ALLGAMES
    while True:
        try:
            data = pickle.loads(conn.recv(1024))
        except EOFError:
            del ALLGAMES[gameID]
            break
        try:
            board = ALLGAMES[gameID]
        except KeyError:
            break

        if data == "break":
            break
        else:
            if not board.ready:
                conn.send(pickle.dumps("waiting"))
                continue
            if data != "get":
                # Data is of format (args, kwargs)
                args, kwargs = data

                if color == board.currentTurn == color:
                    try:
                        ALLGAMES[gameID].movePiece(*args, **{**kwargs, **MANDATORYFLAGS})
                    except PromotionError:
                        conn.send(pickle.dumps("promote"))
                        continue
                    except Illegal:
                        conn.send(pickle.dumps("illegal"))
                        continue

        conn.send(pickle.dumps(ALLGAMES[gameID]))

    conn.close()
    players -= 1
    print("Disconnected from ", addr)
    return


players = 0
try:
    while True:
        try:
            conn, addr = s.accept()
        except socket.timeout:
            continue

        if players % 2 == 0:
            ALLGAMES[players // 2] = initClassic()
            ALLGAMES[players // 2].ready = False

            _thread.start_new_thread(client, (conn, addr, "white", players // 2))
        else:
            ALLGAMES[players // 2].ready = True
            _thread.start_new_thread(client, (conn, addr, "black", players // 2))

        players += 1
        print("Connected to ", addr)

except KeyboardInterrupt:
    s.close()
