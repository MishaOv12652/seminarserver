import socket
import threading
import ReqResHandler


class ThreadedServer(object):
    t_lock = threading.Lock()

    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.bind((self.host, self.port))

    def listen(self):
        self.sock.listen(10)
        while True:
            client, address = self.sock.accept()
            client.settimeout(60)
            threading.Thread(target=self.listenToClient, args=(client, address)).start()

    def listenToClient(self, client, address):
        size = 1024
        while True:
            try:
                self.t_lock.acquire()
                data = client.recv(size)
                if data:
                    res = ReqResHandler.ReqRes((str(data))).process_req()
                    # Set the response to echo back the recieved data
                    response = res
                    print ("res: " + response)
                    client.send(response)
                    self.t_lock.release()
                else:
                    self.t_lock.acquire()
                    raise StandardError('Client disconnected')
            except:
                self.t_lock.acquire()
                client.close()
                return False


if __name__ == "__main__":
    while True:
        port_num = input("Port? ")
        try:
            port_num = int(port_num)
            break
        except ValueError:
            pass

    ThreadedServer('127.0.0.1', port_num).listen()
