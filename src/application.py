import typer
import os

from client import Client
from server import Server
from typing import Optional

application = typer.Typer()

@application.command()
def client(host : Optional[str] = '127.0.0.1', port : Optional[int] = 50000, folder : Optional[str] = './'):
    client = Client(host, port, folder)
    client.connect()

@application.command()
def server(host : Optional[str] = '127.0.0.1', port : Optional[int] = 50000, folder : Optional[str] = './'):
    server = Server(host, port, folder)
    server.start()

if __name__ == "__main__":
    application()
