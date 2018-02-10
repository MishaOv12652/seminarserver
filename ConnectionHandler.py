import socket
import threading
import ReqResHandler
import EncDycrpt


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
            threading.Thread(target=self.listen_to_client, args=(client, address, enc_dec_obj)).start()

    def listen_to_client(self, client, address, enc_dec_obj):
        sand_box = {'__builtins__': {}}
        size = 2048
        print("Client with the data: " + str(address) + " Connected......")
        while True:
            key_to_send = enc_dec_obj.priv_pub_keys_dict['bin_pub_key']
            client.send(key_to_send)
            password = client.recv(size)
            if enc_dec_obj.decrypt_data(password) != "Mrort987":
                client.send("you are not autherized, shutting down")
                client.close()
                return False
            else:
                client.send(str(enc_dec_obj.priv_pub_keys_dict['bin_priv_key']))
                break

        while True:
            try:
                data = client.recv(size)
                data = enc_dec_obj.decrypt_data(data)
                if data:
                    response = ReqResHandler.ReqRes((str(data))).process_req(sand_box)
                    self.sand_box.update(sand_box)
                    client.send(enc_dec_obj.encrypt_data(str(response)))
                else:
                    raise StandardError('Client disconnected')

            except StandardError:
                client.close()
                return False
