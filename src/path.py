import os

class Path:
    def __init__(self, path):
        self.path = os.path.join(*path.split('/'))

    def __str__(self):
        return self.path
