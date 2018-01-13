from Crypto.PublicKey import RSA


class EncDyc():

    def __init__(self, data):
        self.data = data
        self.key = RSA.generate(2048)
        self.priv_pub_keys_dict = {}

    def create_private_public_key(self):
        bin_priv_key = self.key.exportKey('DER')
        bin_pub_key = self.key.publickey().exportKey('DER')
        self.priv_pub_keys_dict.update({"bin_priv_key": bin_priv_key}, {"bin_pub_key": bin_pub_key})

    def encrypt_data(self):
        privKeyObj = RSA.importKey(binPrivKey)
        pubKeyObj = RSA.importKey(binPubKey)

        msg = "attack at dawn"
        emsg = pubKeyObj.encrypt(msg, 'x')[0]
        dmsg = privKeyObj.decrypt(emsg)
        return "encryptData"

    def dycrypt_data(self):
        privKeyObj = RSA.importKey(self.priv_pub_keys_dict[bin_priv_key])
        pubKeyObj = RSA.importKey(binPubKey)

        msg = "attack at dawn"
        emsg = pubKeyObj.encrypt(msg, 'x')[0]
        dmsg = privKeyObj.decrypt(emsg)
        return "encryptData"




