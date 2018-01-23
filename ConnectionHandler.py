import socket
import threading
import ReqResHandler
import EncDycrpt
import cPickle


class ThreadedServer(object):

    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.bind((self.host, self.port))
        self.sand_box = {'__builtins__': {}}

    def listen(self):
        self.sock.listen(10)
        print('Server started on port 5200....')
        print('Waiting For Clients.........')
        enc_dec_obj = EncDycrpt.EncDec()
        enc_dec_obj.create_private_public_key()
        while True:
            client, address = self.sock.accept()
            threading.Thread(target=self.listen_to_client, args=(client, address, enc_dec_obj, self.sand_box)).start()

    def listen_to_client(self, client, address, enc_dec_obj, sand_box):
        size = 2048
        print("Client with the data: " + str(address) + " Connected......")
        while True:
            key_to_send = enc_dec_obj.priv_pub_keys_dict['bin_pub_key']
            client.send(key_to_send)
            password = client.recv(size)
            if str(enc_dec_obj.decrypt_data(password)) != "Mrort987":
                client.send("you are not autherized, please try again")
                client.close()
                return False
            else:
                break

        while True:
            try:
                data = client.recv(size)
                data = enc_dec_obj.decrypt_data(data)
                if data:
                    response = ReqResHandler.ReqRes((str(data))).process_req(sand_box)
                    self.sand_box.update(sand_box)
                    client.send(str(enc_dec_obj.encrypt_data(response)))
                    #client.send(str(response))
                else:
                    raise StandardError('Client disconnected')

            except StandardError:
                client.close()
                return False


if __name__ == "__main__":
    while True:
        port_num = 5200  # input("Port? ")
        try:
            port_num = int(port_num)
            break
        except ValueError:
            pass

    ThreadedServer('127.0.0.1', port_num).listen()
