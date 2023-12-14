import os
import socket
import inquirer
from commands import Command

class Client:
    def __init__(self, host, port, defaultPath):
        self.host = host
        self.port = port
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.defaultPath = os.path.join(os.getcwd(), defaultPath)
        self.connected = False

        if not os.path.exists(self.defaultPath):
            os.makedirs(self.defaultPath)

    def connect(self, interaction = True) -> None:
        if not self.connected:
            try:
                self.socket.connect((self.host, self.port))
                self.connected = True
                print(f"Connected to server at {self.host}:{self.port}")
                if interaction:
                    self.start_interaction()
            except ConnectionRefusedError:
                print("Connection refused. Make sure the server is running.")

    def _answer_inquirer(self, name: str, message: str, choices: list[str]) -> str:
        options = [inquirer.List(name = name, message = message, choices = choices)]
        answers = inquirer.prompt(options)

        if not answers:
            return ''

        return answers[name]

    def download(self, basename, pathToSave) -> str:
        if not os.path.exists(pathToSave):
            os.makedirs(pathToSave)
        download_command = f"download,{basename}"
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
            return received_data.decode()
        else:
            save_path = os.path.join(pathToSave, basename)
            if os.path.exists(save_path):
                count = 1
                while True:
                    new_basename = f"{os.path.splitext(basename)[0]}({count}){os.path.splitext(basename)[1]}"
                    save_path = os.path.join(pathToSave, new_basename)
                    if not os.path.exists(save_path):
                        break
                    count += 1

            with open(save_path, 'wb') as file:
                file.write(received_data)
            return f"{os.path.basename(save_path)} downloaded and saved successfully at {pathToSave}."

    def upload(self, basename):
        try:
            self.socket.send('upload'.encode())
            with open(basename, 'rb') as file:
                file_data = file.read()
                file_size = len(file_data)
                file_info = f"{os.path.basename(basename)},{file_size}"
                self.socket.send(file_info.encode())
                response = self.socket.recv(1024).decode()

                if response.startswith('Ready'):
                    self.socket.sendall(file_data)
                    response = self.socket.recv(1024).decode()
                    return response
                else:
                    return response
        except FileNotFoundError:
            return "File not found."

    def list(self) -> list[str]:
        self.socket.send(Command.LIST.value.encode())
        response = self.socket.recv(1024).decode()
        if response == 'Directory empty.':
            return []
        return response.split(',')

    def delete(self, basename: str) -> str:
        delete_command = f"{Command.DELETE.value},{basename}"
        self.socket.send(delete_command.encode())

        delete_response = self.socket.recv(1024).decode()

        if delete_response == 'Success.':
            return 'File deleted successfully.'
        else:
            return delete_response.split('.', 1)[-1]

    def start_interaction(self) -> None:
        try:
            while True:
                if self.list():
                    availableCommands = [Command.LIST.value, Command.UPLOAD.value, Command.DOWNLOAD.value, Command.DELETE.value, Command.EXIT.value]
                else:
                    availableCommands = [Command.UPLOAD.value, Command.EXIT.value]
                cmd = self._answer_inquirer('Command', 'Choose a command', availableCommands)

                if cmd == Command.EXIT.value:
                    self.socket.send(cmd.encode())
                    break

                elif cmd == Command.LIST.value:
                    listResponse = self.list()

                    if listResponse == []:
                        print('Directory is empty, fill it by uploading files!')
                    else:
                        print('Files in storage:\n    ' + '\n    '.join(listResponse) + '\n')

                elif cmd == Command.DELETE.value:
                    while True:
                        listResponse = self.list()
                        if not listResponse:
                            print("No files to delete")
                            break
                        listResponse.append('Return to main menu')
                        answer = self._answer_inquirer('Filename', "Choose file to delete", listResponse)

                        if answer == listResponse[-1]:
                            break
                        else:
                            print(self.delete(answer))
                            break

                elif cmd == Command.DOWNLOAD.value:
                    while True:
                        listResponse = self.list()
                        if not listResponse:
                            print('No Files to download')
                            break
                        listResponse.append('Return to main menu')
                        fileToDownloadAnswer = self._answer_inquirer('Filename', "Choose file to download", listResponse)

                        if fileToDownloadAnswer == listResponse[-1]:
                            break

                        folderOptions = ['Enter path', 'Navigate through directories', 'Return to main menu']
                        folderToSaveAnswer = self._answer_inquirer('Folder', "Choose the path to save the selected file", folderOptions)
                        path = self.defaultPath
                        download = False
                        if folderToSaveAnswer == folderOptions[-1]:
                            break
                        elif folderToSaveAnswer == folderOptions[0]:
                            path = input("Enter the path where the file will be saved: ")
                            if os.path.exists(path):
                                download = True
                        else:
                            while True:
                                if not os.path.exists(path):
                                    print("Directory doesn't exist.")
                                    break

                                current_folders = [item + '/' for item in os.listdir(path) if os.path.isdir(os.path.join(path, item))]
                                current_folders.insert(0, '.')
                                current_folders.insert(1, '..')
                                current_folders.append('Return to main menu')

                                selected_path = self._answer_inquirer('Path', 'Choose directory to save the file. Select \'.\' to choose actual dir and \'..\' to go one directory above.', current_folders)

                                if selected_path == current_folders[1]:
                                    if path != '/':
                                        path = os.path.dirname(path)
                                elif selected_path == current_folders[0]:
                                    download = True
                                    break
                                elif selected_path == current_folders[-1]:
                                    break
                                else:
                                    new_path = os.path.join(path, selected_path)
                                    path = new_path
                        if download:
                            print(self.download(fileToDownloadAnswer, path))
                        break

                elif cmd == Command.UPLOAD.value:
                    while True:
                        upload = False
                        folderOptions = ['Enter path', 'Navigate through directories', 'Return to main menu']
                        folderToSaveAnswer = self._answer_inquirer('Folder', "Choose the path of the file", folderOptions)
                        file_path = self.defaultPath
                        if folderToSaveAnswer == folderOptions[-1]:
                            break
                        elif folderToSaveAnswer == folderOptions[0]:
                            file_path = input("Enter the path of the file you want to upload: ")
                            if os.path.exists(file_path):
                                upload = True
                                break
                        else:
                            while True:
                                if not os.path.exists(file_path):
                                    print("Directory doesn't exist.")
                                    break

                                current_contents = [item + '/' if os.path.isdir(os.path.join(file_path, item)) else item for item in os.listdir(file_path)]
                                current_contents.insert(0, '.')
                                current_contents.insert(1, '..')
                                current_contents.append('Return to main menu')

                                selected_path = self._answer_inquirer('Path', 'Choose directory to save the file. Select \'.\' to choose the actual dir to compact and send it; and \'..\' to go one directory above.', current_contents)

                                if selected_path == current_contents[1]:
                                    if file_path != '/':
                                        file_path = os.path.dirname(file_path)
                                elif selected_path == current_contents[0]:
                                    # add functionality to zip the folder
                                    pass
                                elif selected_path == current_contents[-1]:
                                    break
                                else:
                                    new_path = os.path.join(file_path, selected_path)
                                    if os.path.isdir(new_path):
                                        file_path = new_path
                                    else:
                                        file_path = new_path
                                        upload = True
                                        break
                        if upload:
                            print(self.upload(file_path))
                        break
                else:
                    print('Option not reconized')

        except ConnectionError:
            print("Connection lost.")
        finally:
            self.socket.close()
