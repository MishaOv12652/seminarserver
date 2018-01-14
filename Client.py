import socket


def main():
    host = '127.0.0.1'
    port = 5200
    mySocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    mySocket.connect((host, port))
    filepath = './cla.txt'  # './misha'
    with open(filepath) as fp:
        line = fp.readline()
        cnt = 1
        while line:
            print("Line {}: {}".format(cnt, line.strip()))
            mySocket.send(line)
            data = mySocket.recv(1024)
            print ('Received from server: ' + data)
            line = fp.readline()
            cnt += 1


if __name__ == '__main__':
    main()
