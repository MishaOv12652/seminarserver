import ConnectionHandler


def main():
    while True:
        port_num = 5200 #input("Port? ")
        try:
            port_num = int(port_num)
            break
        except ValueError:
            pass

    ConnectionHandler.ThreadedServer('127.0.0.1', port_num).listen()


if __name__ == '__main__':
    main()
