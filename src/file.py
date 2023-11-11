class File:
    def __init__(self, name, extension, size):
        self.name = name
        self.extension = extension
        self.size = size

    def __eq__(self, other):
        return self.name == other.name and self.extension == other.extension