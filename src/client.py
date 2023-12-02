import socket
import inquirer

class Client:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

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

                self.socket.send(cmd.encode('utf-8'))

                if cmd == "exit":
                    self.socket.send(cmd.encode('utf-8'))
                    break

                elif cmd == 'list':
                    response = self.socket.recv(1024).decode('utf-8')
                    if response == 'Directory empty.':
                        print(response + '\n')
                    else:
                        print('Files:\n\t' + response.replace(',', '\n\t') + '\n')

                elif cmd == "delete":
                    while True:
                        self.socket.send("list".encode('utf-8'))
                        response = self.socket.recv(1024).decode()
                        if (response == 'Directory empty.'):
                            print(response + '\n')
                            break
                        filenames = response.split(',')
                        filenames.append('Return')
                        options = [inquirer.List('filename', message="Choose file to delete", choices=filenames)]
                        answers = inquirer.prompt(options)

                        if not answers:
                            break

                        option = answers['filename']

                        if option == "Return":
                            break
                        else:
                            delete_command = f"delete,{option}"
                            self.socket.send(delete_command.encode())

                        delete_response = self.socket.recv(1024).decode('utf-8')
                        print(delete_response)

                elif cmd == 'download':
                    response = self.socket.recv(1024).decode('utf-8')
                    print('download: ' + response)

                elif cmd == 'upload':
                    response = self.socket.recv(1024).decode('utf-8')
                    print('upload: ' + response)

                else:
                    print('Option not reconized')
                    break

        except ConnectionError:
            print("Connection lost.")
        finally:
            self.socket.close()
