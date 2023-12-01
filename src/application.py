import typer

from server import Server
from client import Client
from path import Path

application = typer.Typer()

@application.command()
def server(host = "127.0.0.1", port = 50000, path = Path("data/")):
    server = Server(host, port, path)
    server.start()

@application.command()
def client(host = "127.0.0.1", port = 50000):
    client = Client(host, port)
    client.connect()

if __name__ == "__main__":
    application()
