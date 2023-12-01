import os

class Storage:
    def __init__(self, path: str):
        if not os.path.exists(path):
            os.makedirs(path)

        self.path = path
        self.updateFileList()

    def updateFileList(self):
        self.files = os.listdir(self.path)

    def list(self):
        if self.files:
            return '\n'.join(self.files) + '\n'
        return 'Storage is empty.\n'

    def upload(self, file):
        filepath = os.path.join(self.path, file.name + '.' + file.extension) if file.extension else os.path.join(self.path, file.name)
        with open(filepath, 'wb') as document:
            document.write(file.data)
        self.update_file_list()

    def download():
        pass

    def delete(self, filename):
        filepath = os.path.join(self.path, filename)
        try:
            os.remove(filepath)
            self.update_file_list()
            return 'File {} removed successfully.'.format(filename)
        except FileNotFoundError:
            return 'The file {} does not exist in the repository.'.format(filename)
        except Exception as e:
            return 'Error occurred while deleting {}: {}'.format(filename, e)
