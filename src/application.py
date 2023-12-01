import typer
from server import Server
from client import Client

application = typer.Typer()

@application.command()
def server(host: str = "127.0.0.1", port: int = 50000, path: str = "data/"):
    server_instance = Server(host, port, path)
    server_instance.start()

@application.command()
def client(host: str = "127.0.0.1", port: int = 50000):
    client_instance = Client(host, port)
    client_instance.connect()

if __name__ == "__main__":
    application()
