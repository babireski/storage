from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

class Handler(FileSystemEventHandler):
    def __init__(self, storage):
        self.storage = storage

    def on_any_event(self, event):
        self.storage.updateFileList()

def watch(storage):
    handler = Handler(storage)
    observer = Observer()
    observer.schedule(handler, storage.path)
    observer.start()
