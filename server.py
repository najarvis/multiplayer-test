import socket
import time

PORT = 3333

def start():
    serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    host = socket.gethostname()
    serversocket.bind(('0.0.0.0', PORT))

    serversocket.listen(5)

    while True:
        clientsocket, addr = serversocket.accept()

        print("Got a connection from {}".format(str(addr)))
        currentTime = time.ctime(time.time()) + "\r\n"
        clientsocket.send(currentTime.encode('ascii'))
        clientsocket.close()

if __name__ == "__main__":
    start()
