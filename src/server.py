import socket

from storage import Storage

class Server:
    def __init__(self, host, port, path):
        self.host = host
        self.port = port
        self.storage = Storage(path)
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def start(self):
        try:
            self.socket.bind((self.host, self.port))
            self.socket.listen(5)
            print("Server started on ", self.host, ":", self.port)
        except socket.error as e:
            print("Failed to start the server: ", e)