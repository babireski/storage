class File:
    def __init__(self, name, extension, size, data):
        self.name = name
        self.extension = extension
        self.size = size
        self.data = data

    def __str__(self):
        return self.name + '.' + self.extension

    def __eq__(self, other):
        return self.name == other.name and self.extension == other.extension