from enum import Enum

class Command(Enum):
    LIST = 'list'
    DOWNLOAD = 'download'
    UPLOAD = 'upload'
    DELETE = 'delete'
    SHUTDOWN = 'shutdown'
    EXIT = 'exit'
