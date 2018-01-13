import socket

import socket


def Main():
    host = '127.0.0.1'
    port = 5200

    mySocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    mySocket.connect((host, port))

    message = input(" ? ")

    while message != 'q':
        mySocket.send(message)
        data = mySocket.recv(1024)

        print ('Received from server: ' + data)

        message = input(" ? ")


# mySocket.close()

if __name__ == '__main__':
    Main()
# def main():
#     host = '127.0.0.1'
#     port = 5000
#
#     s = socket.socket()
#     s.connect((host, port))
#
#     messege = input("-> ")
#     while messege != 'q':
#         s.send(messege)
#         data = s.recv(1024)
#         print("Recieved from server: " + data)
#         messege = input("-> ")
#
#     s.close()
#
#
# if __name__ == '__main__':
#     main()
