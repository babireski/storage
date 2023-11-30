import socket

from storage import Storage

class Server:
    def __init__(self, host, port, path):
        self.host = host
        self.port = port
        self.storage = Storage(path)
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def __str__(self):
        return self.host + ':' + self.port

    def start(self):
        try:
            self.socket.bind((self.host, self.port))
            self.socket.listen(5)
            print('Server started on ' + self)
        except socket.error as e:
            print('Failed to start the server: ', e)