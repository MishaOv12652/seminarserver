from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP, PKCS1_v1_5
import ast


class EncDec(object):

    def __init__(self):
        self.key = RSA.generate(2048)
        self.priv_pub_keys_dict = {}

    def create_private_public_key(self):
        # path = "c:/test/"
        # pub_key_file = open(path+'/public.pem')
        # pub_key = RSA.importKey(pub_key_file.read())
        # private_key_file = open(path + '/privkey.pem')
        # private_key = RSA.importKey(private_key_file.read())
        # self.priv_pub_keys_dict.update({"bin_priv_key": private_key})
        # self.priv_pub_keys_dict.update({"bin_pub_key": pub_key})

        bin_priv_key = self.key.exportKey('PEM')
        file_name = "p_key.pem"
        file_to_write = open(file_name, 'w')
        file_to_write.write(bin_priv_key)
        file_to_write.close()
        bin_pub_key = self.key.publickey().exportKey('PEM')
        self.priv_pub_keys_dict.update({"bin_priv_key": bin_priv_key})
        self.priv_pub_keys_dict.update({"bin_pub_key": bin_pub_key})

    def encrypt_data(self, data_to_encrypt):
        public_key = RSA.importKey(self.priv_pub_keys_dict["bin_pub_key"])
        cipher = PKCS1_OAEP.new(public_key)
        # cipher = PKCS1_OAEP.new(self.priv_pub_keys_dict['bin_pub_key'])
        encrypted_msg = cipher.encrypt(data_to_encrypt)
        # encrypted_msg = public_key.encrypt(str(data_to_encrypt), 32)
        return encrypted_msg

    def decrypt_data(self, data_to_decrypt):
        private_key = RSA.importKey(self.priv_pub_keys_dict["bin_priv_key"])
        cipher = PKCS1_OAEP.new(private_key)
        # cipher = PKCS1_OAEP.new(self.priv_pub_keys_dict['bin_priv_key'])
        decrypted_msg = cipher.decrypt(data_to_decrypt)
        # decrypted_msg = private_key.decrypt(data_to_decrypt)
        return decrypted_msg
