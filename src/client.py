import os
import socket
import inquirer
from storage import Storage

class Client:
    def __init__(self, host: str, port: int, path: str):
        self.host = host
        self.port = port
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.path = path
        self.storage = Storage(self.path)

    def connect(self):
        try:
            self.socket.connect((self.host, self.port))
            print(f"Connected to server at {self.host}:{self.port}")
            self.start_interaction()
        except ConnectionRefusedError:
            print("Connection refused. Make sure the server is running.")

    def start_interaction(self):
        try:
            while True:
                questions = [inquirer.List('command', message = 'Choose a command', choices = ['list', 'upload', 'download', 'delete', 'exit'])]
                answers = inquirer.prompt(questions)

                if not answers:
                    break

                cmd = answers['command']

                if cmd == "exit":
                    self.socket.send(cmd.encode())
                    break

                elif cmd == 'list':
                    self.socket.send(cmd.encode())
                    response = self.socket.recv(1024).decode()
                    if response == 'Directory empty.':
                        print(response + '\n')
                    else:
                        print('Files:\n\t' + response.replace(',', '\n\t') + '\n')

                elif cmd == "delete":
                    while True:
                        self.socket.send("list".encode())
                        response = self.socket.recv(1024).decode()
                        if response == 'Directory empty.':
                            print(response + '\n')
                            break
                        filenames = response.split(',')
                        filenames.append('Return')
                        options = [inquirer.List('filename', message = "Choose file to delete", choices = filenames)]
                        answers = inquirer.prompt(options)

                        if not answers:
                            break

                        option = answers['filename']

                        if option == "Return":
                            break
                        else:
                            delete_command = f"delete,{option}"
                            self.socket.send(delete_command.encode())

                        delete_response = self.socket.recv(1024).decode()
                        print(delete_response)
                        break

                elif cmd == 'download':
                    while True:
                        self.socket.send("list".encode())
                        response = self.socket.recv(1024).decode()
                        if response == 'Directory empty.':
                            print(response + '\n')
                            break
                        filenames = response.split(',')
                        filenames.append('Return')
                        options = [inquirer.List('filename', message="Choose file to download", choices=filenames)]
                        answers = inquirer.prompt(options)

                        if not answers:
                            break

                        option = answers['filename']

                        if option == "Return":
                            break
                        else:
                            download_command = f"download,{option}"
                            self.socket.send(download_command.encode())

                        file_size = int(self.socket.recv(1024).decode())
                        self.socket.send(b"ACK")

                        received_data = b''
                        while len(received_data) < file_size:
                            chunk = self.socket.recv(4096)
                            if not chunk:
                                break
                            received_data += chunk

                        if received_data.startswith(b'Error'):
                            print(received_data.decode())
                        else:
                            save_path = os.path.join(self.path, option)
                            with open(save_path, 'wb') as file:
                                file.write(received_data)
                            print(f"{option} downloaded and saved successfully.")
                            break

                elif cmd == 'upload':
                    response = self.socket.recv(4096).decode()
                    print('upload: ' + response)

                else:
                    print('Option not reconized')
                    break

        except ConnectionError:
            print("Connection lost.")
        finally:
            self.socket.close()
