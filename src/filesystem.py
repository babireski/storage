import os

class Filesystem:
    def __init__(self, path):
        self.path = path
        fork = '├── '
        last = '└── '
        more = '│   '
        none = '    '

    def tree(self, prefix = ''):
        pass
