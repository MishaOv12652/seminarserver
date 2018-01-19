import socket
import cPickle
from Crypto.PublicKey import RSA
import ast

def main():
    host = '127.0.0.1'
    port = 5200
    mySocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    mySocket.connect((host, port))
    while True:
        data = mySocket.recv(2048)
        key = cPickle.loads(data)
        pub_key = RSA.importKey(key)
        break
    filepath = './cla.txt'#'./functions.txt'#'./cla.txt'  # './misha'
    with open(filepath) as fp:
        line = fp.readline()
        cnt = 1
        while line:
            print("Line {}: {}".format(cnt, line.strip()))
            line = cPickle.dumps(pub_key.encrypt(line, 32))
            mySocket.send(line)
            data = mySocket.recv(2048)
            data = cPickle.loads(str(data))
            p_key_file = open('p_key.pem', "r")
            p_key = RSA.importKey(p_key_file.read())
            data = p_key.decrypt(ast.literal_eval(str(data)))
            print ('Received from server: ' + str(data))
            line = fp.readline()
            cnt += 1


if __name__ == '__main__':
    main()
