from Crypto.PublicKey import RSA
import ast


class EncDec(object):

    def __init__(self):
        self.key = RSA.generate(2048)
        self.priv_pub_keys_dict = {}

    def create_private_public_key(self):
        bin_priv_key = self.key.exportKey('DER')
        bin_pub_key = self.key.publickey().exportKey('DER')
        self.priv_pub_keys_dict.update({"bin_priv_key": bin_priv_key})
        self.priv_pub_keys_dict.update({"bin_pub_key": bin_pub_key})

    def encrypt_data(self, data_to_encrypt):
        public_key = RSA.importKey(self.priv_pub_keys_dict["bin_pub_key"])
        encrypted_msg = public_key.encrypt(str(data_to_encrypt), 32)
        return encrypted_msg

    def decrypt_data(self, data_to_decrypt):
        private_key = RSA.importKey(self.priv_pub_keys_dict["bin_priv_key"])
        decrypted_msg = private_key.decrypt(ast.literal_eval(str(data_to_decrypt)))
        return decrypted_msg


def main():
    enc_dec_obj = EncDec()
    enc_dec_obj.create_private_public_key()
    data_to_encrypt = 'def Misha(): print "misha"'
    encrypted_data = enc_dec_obj.encrypt_data(data_to_encrypt)

    print ("data before encryption is :" + str(data_to_encrypt))
    print ("data after encryption is: " + str(encrypted_data))
    print ("data after decryption is: " + enc_dec_obj.decrypt_data(encrypted_data))


if __name__ == '__main__':
    main()
