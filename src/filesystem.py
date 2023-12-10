import os

class Filesystem:
    def __init__(self, path):
        path = path
        walk = os.walk(path)
        fork = '├── '
        last = '└── '
        more = '│   '
        none = '    '

    def tree(self, prefix = ''):
        pass
