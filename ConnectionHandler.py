import socket
import threading
import ReqResHandler
import EncDycrpt
import cPickle


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
        print('Server started on port 5200....')
        print('Waiting For Clients.........')
        while True:
            client, address = self.sock.accept()
            # client.settimeout(60)
            # enc_dec_obj = EncDycrpt.EncDec()
            # enc_dec_obj.create_private_public_key()
            # pub_key_to_client = enc_dec_obj.priv_pub_keys_dict['bin_pub_key']
            threading.Thread(target=self.listen_to_client, args=(client, address)).start()

    def listen_to_client(self, client, address):
        print("Client Connected......")
        size = 1024
        while True:
            try:
                # self.t_lock.acquire()
                data = client.recv(size)
                if data:
                    response = ReqResHandler.ReqRes((str(data))).process_req()
                    client.send(str(response))
                    # self.t_lock.release()
                else:
                    # self.t_lock.acquire()
                    raise StandardError('Client disconnected')

            except StandardError:
                # self.t_lock.acquire()
                client.close()
                # return False


if __name__ == "__main__":
    while True:
        port_num = 5200  # input("Port? ")
        try:
            port_num = int(port_num)
            break
        except ValueError:
            pass

    ThreadedServer('127.0.0.1', port_num).listen()
