from Crypto.PublicKey import RSA
import ast

class EncDec(object):

    def __init__(self, data):
        self.data = data
        self.key = RSA.generate(2048)
        self.priv_pub_keys_dict = {}

    def create_private_public_key(self):
        bin_priv_key = self.key.exportKey('DER')
        bin_pub_key = self.key.publickey().exportKey('DER')
        self.priv_pub_keys_dict.update({"bin_priv_key": bin_priv_key})
        self.priv_pub_keys_dict.update({"bin_pub_key": bin_pub_key})

    def encrypt_data(self):
        public_key = RSA.importKey(self.priv_pub_keys_dict["bin_pub_key"])
        encrypted_msg = public_key.encrypt(str(self.data), 32)
        return encrypted_msg

    def decrypt_data(self, encrypted_data):
        private_key = RSA.importKey(self.priv_pub_keys_dict["bin_priv_key"])
        decrypted_msg = private_key.decrypt(ast.literal_eval(str(encrypted_data)))
        return decrypted_msg


def main():
    data_to_encrypt = EncDec('def Misha(): print "misha"')
    data_to_encrypt.create_private_public_key()
    print ("data before encryption is Misha\n")
    print ("data after encryption is :" + str(data_to_encrypt.encrypt_data()))
    data_to_decrypt = data_to_encrypt.encrypt_data()
    print ("data after decryption is :" + data_to_encrypt.decrypt_data(data_to_decrypt))

if __name__ == '__main__':
    main()