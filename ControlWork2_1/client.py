import socket
import threading
import sys

def receive(socket, signal):
    while signal:
        try:
            data = socket.recv(32)
            print(str(data.decode("utf-8")))
        except:
            print("Вы были отключены от сервера")
            signal = False
            break

host = input("Host: ")
port = int(input("Port: "))

try:
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((host, port))
except:
    print("Ошибка подключения")
    input("Enter - выход")
    sys.exit(0)

receiveThread = threading.Thread(target = receive, args = (sock, True))
receiveThread.start()

while True:
    message = input()
    sock.sendall(str.encode(message))