import typer
from server import Server
from client import Client

application = typer.Typer()

@application.command()
def server(host : str = '127.0.0.1', port : int = 50000, path : str = 'server-test-data/'):
    server = Server(host, port, path)
    server.start()

@application.command()
def client(host : str = '127.0.0.1', port : int = 50000, path : str = 'client-test-data/'):
    client = Client(host, port, path)
    client.connect()

if __name__ == "__main__":
    application()
