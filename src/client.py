import os
import socket
import inquirer
from storage import Storage

class Client:
    def __init__(self, host, port, path):
        self.host = host
        self.port = port
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.path = os.path.join(os.getcwd(), path)
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
                        print('Files:\n    ' + response.replace(',', '\n    ') + '\n')

                elif cmd == "delete":
                    while True:
                        self.socket.send("list".encode())
                        response = self.socket.recv(1024).decode()
                        if response == 'Directory empty.':
                            print(response + '\n')
                            break
                        filenames = response.split(',')
                        filenames.append('Return to main menu')
                        options = [inquirer.List('filename', message = "Choose file to delete", choices = filenames)]
                        answers = inquirer.prompt(options)

                        if not answers:
                            break

                        option = answers['filename']

                        if option == "Return to main menu":
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
                        filenames.append('Return to main menu')
                        options = [inquirer.List('filename', message="Choose file to download", choices=filenames)]
                        answers = inquirer.prompt(options)

                        if not answers:
                            break

                        option = answers['filename']

                        if option == "Return to main menu":
                            break
                        else:
                            download_command = f"download,{option}"
                            self.socket.send(download_command.encode())

                        file_size = int(self.socket.recv(1024).decode())
                        self.socket.send(b"OK")

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
                    while True:
                        file_path = self.path
                        choices = ['Enter path of the file', 'Navigate through directories', 'Return to main menu']
                        options = [inquirer.List('path', message="Choose file to upload", choices=choices)]
                        answers = inquirer.prompt(options)

                        if not answers:
                            break

                        selected_option = answers['path']
                        if selected_option == choices[0]:
                            file_path = input("Enter the path of the file: ")
                        elif selected_option == choices[-1]:
                            break
                        else:
                            while True:
                                if not os.path.exists(file_path):
                                    print("Directory doesn't exist.")
                                    break

                                current_contents = os.listdir(file_path)
                                current_contents.insert(0, '..')
                                current_contents.append('Return to main menu')
                                options = [inquirer.List('path', message='Choose dir or file', choices=current_contents)]
                                answer = inquirer.prompt(options)

                                if not answer:
                                    break

                                selected_path = answer['path']

                                if selected_path == '..':
                                    if file_path != '/':
                                        file_path = os.path.dirname(file_path)
                                else:
                                    new_path = os.path.join(file_path, selected_path)

                                    if os.path.isdir(new_path):
                                        file_path = new_path
                                    else:
                                        file_path = new_path
                                        break
                        if file_path != self.path and selected_option != choices[-1] and os.path.exists(file_path):
                            try:
                                self.socket.send('upload'.encode())
                                with open(file_path, 'rb') as file:
                                    file_data = file.read()
                                    file_size = len(file_data)
                                    file_info = f"{os.path.basename(file_path)},{file_size}"
                                    self.socket.send(file_info.encode())
                                    response = self.socket.recv(1024).decode()

                                    if response.startswith('Ready'):
                                        self.socket.sendall(file_data)
                                        response = self.socket.recv(1024).decode()
                                        print(response)
                                    else:
                                        print(response)
                                break
                            except FileNotFoundError:
                                print("File not found.")
                        else:
                            break
                else:
                    print('Option not reconized')
                    break

        except ConnectionError:
            print("Connection lost.")
        finally:
            self.socket.close()
