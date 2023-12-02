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

        except socket.error as error:
            print('Failed to start the server: ', error)

    def handle_client(self, client_socket):
        try:
            while True:
                cmd = client_socket.recv(1024).decode()

                if not cmd or cmd == 'exit':
                    print('Client {} requested to close the connection.'.format(client_socket.getpeername()))
                    break

                self.execute_command(client_socket, cmd)

        except ConnectionResetError:
            print('Client {} forcibly closed the connection.'.format(client_socket.getpeername()))
        except OSError as e:
            print('Error with client {}: {}'.format(client_socket.getpeername(), e))
        finally:
            if client_socket.fileno() != -1:
                client_socket.close()

    def execute_command(self, client, cmd):
        if cmd == 'list':
            print('List requested.')
            if self.storage.files:
                files_list = ','.join(self.storage.files)
                client.send(files_list.encode())
            else:
                client.send('Directory empty.'.encode())

        elif cmd == 'upload':
            print('Upload requested.')
            client.send('Upload functionality to be implemented.\n'.encode())

        elif cmd == 'download':
            print('Download requested.')
            client.send('Download functionality to be implemented.\n'.encode())

        elif cmd.startswith('delete,'):
            _, file_to_delete = cmd.split(',', 1)
            file_to_delete = file_to_delete.strip()

            if file_to_delete in self.storage.files:
                self.storage.delete(file_to_delete)
                print(f'{file_to_delete} removed successfully.')
                client.send('Deleted {}.\n'.format(file_to_delete).encode())
            else:
                print(f'{file_to_delete} does not exist or cannot be deleted')
                client.send('Cannot delete {}. File not found.\n'.format(file_to_delete).encode())

    def stop(self):
        self.socket.close()
        print('Server stopped.')
        for connection in self.connections:
            connection.send('Server stopped.'.encode())
            connection.join()
