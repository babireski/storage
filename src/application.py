import typer
from server import Server
from client import Client

application = typer.Typer()

@application.command()
def server(host : str = '127.0.0.1', port : int = 50000, path : str = 'data/'):
    server = Server(host, port, path)
    server.start()

@application.command()
def client(host : str = '127.0.0.1', port : int = 50000):
    client = Client(host, port)
    client.connect()

if __name__ == "__main__":
    application()
