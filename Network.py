import socket
import pickle


class Network:
    def __init__(self, server="localhost", port=6001):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def connect(self, ip="127.0.0.1", port=5555):
        self.client.connect((ip, port))
        echo = pickle.loads(self.client.recv(15))
        return echo

    def send(self, data):
        self.client.send(pickle.dumps(data))
        try:
            echo = pickle.loads(self.client.recv(4096 * 4))
        except EOFError:
            return None
        else:
            return echo

    def close(self):
        self.client.close()
