from storage import Storage

class Server:
    def __init__(self, host, port, path):
        self.host = host
        self.port = port
        self.storage = Storage(path)

    def start():
        pass