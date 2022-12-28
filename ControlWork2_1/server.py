import socket
import threading

connections = []
total_connections = 0
tasks = []


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
                data = str(data).replace("b'", " ")
                data = data.replace("'", " ")
                data = data[1:]
                if '/new' in data:
                    tasks.append(data[4:])
                    for client in connections:
                        if client.id != self.id:
                            client.socket.sendall(str.encode('Запись добавлена'))
                    print('Запись добавлена')
                elif '/edit' in data:
                    if len(tasks) != 0:
                        try:
                            spl = data[6:]
                            print(spl)
                            task_id = int(data[6:spl.find(' ') + 6])
                            new_task = data[spl.find(' ') + 7:]
                            print('new', new_task)
                            tasks.remove(tasks[task_id])
                            tasks.insert(task_id, new_task)
                            print('Запись изменена')
                        except:
                            print('Ошибка в команде')
                    else:
                        print('Записи отсутствуют')
                elif '/delete' in data:
                    if len(tasks) != 0:
                        try:
                            task_id = int(data[7:])
                            tasks.remove(tasks[task_id])
                            print('Запись удалена')
                        except:
                            print('Ошибка в команде')
                    else:
                        print('Записи отсутствуют')
                elif '/show' in data:
                    if len(tasks) != 0:
                        print('Текущие записи:')
                        for i in range(len(tasks)):
                            print(f' {i} - {tasks[i]}')
                    else:
                        print('Записи отсутствуют')
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
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind(('localhost', 8080))
    sock.listen(5)

    newConnectionsThread = threading.Thread(target=newConnections, args=(sock,))
    newConnectionsThread.start()


main()