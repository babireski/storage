import socket
import threading
from storage import Storage

class Server:
    def __init__(self, host, port, path, log = 'log'):
        self.host = host
        self.port = port
        self.storage = Storage(path)
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connections = []
        self.log = log

    def __str__(self):
        return '{}:{}'.format(self.host, self.port)

    def start(self):
        try:
            self.socket.bind((self.host, self.port))
            self.socket.listen(5)
            print('Server started on {}'.format(str(self)))

            while True:
                client_socket, client_address = self.socket.accept()
                print('Connection established with {}.'.format(client_address))

                thread = threading.Thread(target = self.handle_client, args = (client_socket,))
                thread.start()

                self.connections.append((thread, client_socket))

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

        for index, (_, sock) in enumerate(self.connections):
            if sock == client_socket:
                del self.connections[index]
                break

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
            client.send('Ready to receive file. Send file details (name.extension,size)'.encode())
            file_details = client.recv(1024).decode()
            file_info = file_details.split(',')
            file_name, file_size = file_info[0], int(file_info[1])

            file_data = b''
            while len(file_data) < file_size:
                chunk = client.recv(4096)
                if not chunk:
                    break
                file_data += chunk

            upload_result = self.storage.upload(file_name, file_data)
            client.send(upload_result.encode())

        elif cmd.startswith('download,'):
            print('Download requested.')
            _, file_to_download = cmd.split(',', 1)
            file_to_download = file_to_download.strip()

            if file_to_download in self.storage.files:
                self.storage.download(file_to_download, client)
            else:
                print(f'{file_to_download} does not exist or cannot be downloaded')
                client.send(f'Cannot download {file_to_download}. File not found.\n'.encode())

        elif cmd.startswith('delete,'):
            print('Delete requested.')
            _, file_to_delete = cmd.split(',', 1)
            file_to_delete = file_to_delete.strip()

            if file_to_delete in self.storage.files:
                delete_result = self.storage.delete(file_to_delete)
                print(delete_result)
                client.send(delete_result.encode())
            else:
                print(f'{file_to_delete} does not exist or cannot be deleted')
                client.send('Cannot delete {}. File not found.\n'.format(file_to_delete).encode())

    def stop(self):
        self.socket.close()
        print('Server stopped.')
        for connection in self.connections:
            connection.send('Server stopped.'.encode())
            connection.join()
