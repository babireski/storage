import typer
import watcher

from client import Client
from server import Server
from typing import Optional

application = typer.Typer()

@application.command()
def client(host : Optional[str] = '0.0.0.0', port : Optional[int] = 50000, path : Optional[str] = './'):
    client = Client(host, port, path)
    client.connect()

@application.command()
def server(host : Optional[str] = '0.0.0.0', port : Optional[int] = 50000, path : Optional[str] = './'):
    server = Server(host, port, path)
    watcher.watch(server.storage)
    server.start()

if __name__ == "__main__":
    application()
