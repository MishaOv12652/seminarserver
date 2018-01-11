import socket


def main():
    host = '127.0.0.1'
    port = 5000

    s = socket.socket()
    s.connect((host, port))

    messege = input("-> ")
    while messege != 'q':
        s.send(messege)
        data = s.recv(1024)
        print("Recieved from server: " + data)
        messege = input("-> ")

    s.close()


if __name__ == '__main__':
    main()
