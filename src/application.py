import typer

from client import Client
from server import Server
from typing import Optional

application = typer.Typer()

@application.command()
def client(host : Optional[str] = '0.0.0.0', port : Optional[int] = 50000, defaultPath : Optional[str] = './default-client-path'):
    client = Client(host, port, defaultPath)
    client.connect()

@application.command()
def server(host : Optional[str] = '0.0.0.0', port : Optional[int] = 50000, path : Optional[str] = './default-server-path'):
    server = Server(host, port, path)
    server.start()

if __name__ == "__main__":
    application()
