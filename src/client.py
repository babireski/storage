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
                questions = [inquirer.List('command', message = "Choose a command", choices = ['list', 'upload', 'download', 'delete', 'exit'])]
                answers = inquirer.prompt(questions)

                if not answers:
                    break

                cmd = answers['command']

                if cmd == "exit":
                    self.socket.send(cmd.encode())
                    break

                self.socket.send(cmd.encode())

                if cmd != "exit":
                    response = self.socket.recv(1024).decode()
                    print(response)

        except ConnectionError:
            print("Connection lost.")
        finally:
            self.socket.close()
