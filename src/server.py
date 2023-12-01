import socket
import threading
from storage import Storage

class Server:
    def __init__(self, host, port, path):
        self.host = host
        self.port = port
        self.storage = Storage(path)
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connections = []

    def __str__(self):
        return '{}:{}'.format(self.host, self.port)

    def start(self):
        try:
            self.socket.bind((self.host, self.port))
            self.socket.listen(5)
            print('Server started on {}'.format(str(self)))

            while True:
                client_socket, client_address = self.socket.accept()
                print('Connection established with {}'.format(client_address))

                thread = threading.Thread(target = self.handle_client, args = (client_socket,))
                thread.start()

                self.connections.append(thread)

        except socket.error as e:
            print('Failed to start the server: ', e)

    def handle_client(self, client_socket):
        try:
            while True:
                cmd = client_socket.recv(1024).decode()

                if not cmd or cmd == "exit":
                    print(f"Client {client_socket.getpeername()} requested to close the connection.")
                    break

                self.execute_command(client_socket, cmd)

        except ConnectionResetError:
            print(f"Client {client_socket.getpeername()} forcibly closed the connection.")
        except OSError as e:
            print(f"Error with client {client_socket.getpeername()}: {e}")
        finally:
            if client_socket.fileno() != -1:
                client_socket.close()

    def execute_command(self, client_socket, cmd):
        if cmd == "list":
            print('List requested.')
            client_socket.send(self.storage.list().encode())

        elif cmd == "upload":
            print('Upload requested')
            client_socket.send('Upload functionality to be implemented.'.encode())
            pass

        elif cmd == "download":
            print('Download requested')
            client_socket.send('Download functionality to be implemented.'.encode())
            pass

        elif cmd == "delete":
            print('Delete requested')
            client_socket.send('Delete functionality to be implemented.'.encode())
            pass

    def stop(self):
        self.socket.close()
        print("Server stopped.")
        for connection in self.connections:
            connection.join()
