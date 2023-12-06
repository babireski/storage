from client import Client
import threading
import os
import time
import csv
from matplotlib import pyplot as plt

def download(client, barrier):
    barrier.wait()
    start = time.time()
    for _ in range(downloads):
        client.socket.send('download,{}'.format(file).encode())
        file_size = int(client.socket.recv(1024).decode())
        client.socket.send(b"OK")

        received_data = b''
        while len(received_data) < file_size:
            chunk = client.socket.recv(4096)
            if not chunk:
                break
            received_data += chunk

        if received_data.startswith(b'Error'):
            print(received_data.decode())
        else:
            save_path = os.path.join(client.path, file)
            with open(save_path, 'wb') as f:
                f.write(received_data)
            # print(f"{file} downloaded and saved successfully.")
            break
    performance.append(int((time.time() - start) * 1000))

def graphic():
    if os.path.exists(f"out") == False:
        os.makedirs(f"out")
    with open("out/performance.csv", "r") as spreadsheet:
        reader = csv.DictReader(spreadsheet)
        data = {field: [] for field in reader.fieldnames}
        for row in reader:
            for field in reader.fieldnames:
                if field != 'Threads':
                    data[field].append(float(row[field]))
        if "Threads" in data:
            if any(data.values()):
                plt.plot(data["Time"], label='Time', color='b')
                plt.title(f'Performance for {downloads} downloads')
                plt.xlabel('Threads')
                plt.ylabel('Time in ms')
                plt.legend()
                plt.savefig(f"out/performance.png")
                plt.close()
            else:
                print(f"No data available in performance.csv")
        else:
            print(f"Missing 'Time' data in performance.csv")

def start():
    global performance
    with open('./out/performance.csv', 'w') as spreadsheet:
        print('Threads,Time', file=spreadsheet)
        for n in range(connections):
            barrier = threading.Barrier(n + 1)
            client = Client('192.168.15.20', 50000, './client-test-data/{}'.format(n + 1))
            client.connect(interaction=False)
            clients.append(client)
            threads = []
            performance = []
            for client in clients:
                thread = threading.Thread(target=download, args=(client, barrier))
                threads.append(thread)
                thread.start()
            for thread in threads:
                thread.join()
            # print(len(performance))
            # print(performance)
            print('{},{}'.format(n + 1, sum(performance) / len(performance) if performance else 0), file=spreadsheet)

connections = 500
downloads = 10000
clients = []
threads = []
performance = []
file = 'bobo.mp4'
start()
graphic()
