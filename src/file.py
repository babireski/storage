class File:
    def __init__(self, name, extension, size, data):
        self.name = name
        self.extension = extension
        self.size = size
        self.data = data

    def __str__(self):
        return '{}.{}'.format(self.name, self.extension)

    def __eq__(self, other):
        return self.name == other.name and self.extension == other.extension

    def send(self, filepath, client):
        with open(filepath, 'rb') as file:
            data = file.read(1024)
            while data:
                client.send(data)
                data = file.read(1024)
        print("File sent successfully.")

    def recv(self, filepath, client):
        with open(filepath, 'wb') as file:
            data = client.recv(1024)
            while data:
                file.write(data)
                data = client.recv(1024)
        print("File received successfully.")
