import file
import os

class Storage:
    def __init__(self, path, files):
        self.path = path
        self.files = files

    def list(self):
        # return list(map(lambda file: str(file), self.files))
        return self.files

    def upload(self, file):
        filepath = self.path + file.name + '.' + file.extension if file.extension else self.path + file.name
        with open(filepath, 'wb') as document:
            document.write(file.data)
        self.files.append(file)

    def download():
        pass

    def delete(self, file):
        if file in self.files:
            filename = str(file)
            filepath = self.path + filename
            try:
                os.remove(filepath)
                self.files.remove(file)
                return 'File {} removed successfully.'.format(filename)
            except:
                return 'The file {} does not exist in the repository.'.format(filename)
        return 'The file {} was not found in the repository.'.format(filename)