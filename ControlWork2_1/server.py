import socket
import threading

connections = []
total_connections = 0


class Client(threading.Thread):
    def __init__(self, socket, address, id, name, signal):
        threading.Thread.__init__(self)
        self.socket = socket
        self.address = address
        self.id = id
        self.name = name
        self.signal = signal

    def __str__(self):
        return str(self.id) + " " + str(self.address)

    def run(self):
        while self.signal:
            try:
                data = self.socket.recv(32)
            except:
                print("Клиент " + str(self.address) + " покинул сервер")
                self.signal = False
                connections.remove(self)
                break
            if data != "":
                print("Пользователь " + str(self.id) + ": " + str(data.decode("utf-8")))
                data = str(data).replace("b'", " ")
                data = data.replace("'", " ")
                data = data[1:]
                if '/new' in data:
                    pass
                elif '/edit' in data:
                    pass
                elif '/delete' in data:
                    pass
                else:
                    for client in connections:
                        if client.id != self.id:
                            client.socket.sendall(data)


def newConnections(socket):
    while True:
        sock, address = socket.accept()
        global total_connections
        connections.append(Client(sock, address, total_connections, "Name", True))
        connections[len(connections) - 1].start()
        print("Новое подключение: Пользователь " + str(connections[len(connections) - 1]))
        total_connections += 1


def main():
    host = input("Host: ")
    port = int(input("Port: "))

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind((host, port))
    sock.listen(5)

    newConnectionsThread = threading.Thread(target=newConnections, args=(sock,))
    newConnectionsThread.start()


main()