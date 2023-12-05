import os
import watcher

class Storage:
    def __init__(self, path: str):
        if not os.path.exists(path):
            os.makedirs(path)
        self.path = path
        self.updateFileList()
        # watcher.watch(self)

    def updateFileList(self):
        self.files = os.listdir(self.path)

    def list(self):
        return self.files

    def upload(self, filename, file_data):
        try:
            filepath = os.path.join(self.path, filename)
            with open(filepath, 'wb') as file:
                file.write(file_data)
            self.updateFileList()
            return f'{filename} uploaded successfully.'
        except Exception as e:
            return f'Error occurred while uploading {filename}: {e}'

    def download(self, filename, client):
        filepath = os.path.join(self.path, filename)
        try:
            with open(filepath, 'rb') as file:
                file_data = file.read()
                file_size = len(file_data)
                client.send(str(file_size).encode())
                client.recv(1024)
                client.sendall(file_data)
        except FileNotFoundError:
            return f'The file {filename} does not exist in the repository.'
        except Exception as e:
            return f'Error occurred while downloading {filename}: {e}'

    def delete(self, filename):
        filepath = os.path.join(self.path, filename)
        try:
            os.remove(filepath)
            self.updateFileList()
            return f'File {filename} removed successfully.'
        except FileNotFoundError:
            return f'The file {filename} does not exist in the repository.'
        except Exception as e:
            return f'Error occurred while deleting {filename}: {e}'
