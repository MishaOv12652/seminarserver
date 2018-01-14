import socket
import cPickle
from Crypto.PublicKey import RSA

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
    filepath = './encDecTes.txt'#'./cla.txt'  # './misha'
    with open(filepath) as fp:
        line = fp.readline()
        cnt = 1
        while line:
            print("Line {}: {}".format(cnt, line.strip()))
            line = cPickle.dumps(pub_key.encrypt(line, 32))
            mySocket.send(line)
            data = mySocket.recv(1024)
            data = cPickle.loads(pub_key.decrypt(data))
            print ('Received from server: ' + str(data))
            line = fp.readline()
            cnt += 1


if __name__ == '__main__':
    main()
