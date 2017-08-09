import socket
import os

HOST = ''
PORT = 3333

class Server(object):

    def __init__(self):
        # Create a UDP socket
        self.serversocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

        # Accepts connections from outside sources on this PORT
        self.serversocket.bind((HOST, PORT))

        # Listen to up to 5 requests at a time.
        #self.serversocket.listen(5)

        self.clients = {}

    def update(self):

        data, addr = self.serversocket.recvfrom(1024)

        reply = "We hear you loud and clear, alpha"

        self.serversocket.sendto(reply, addr)
        print('Message from {}:{} - {}'.format(addr[0], addr[1], data.strip()))

def start():
    game_server = Server()
    while True:
        game_server.update()

if __name__ == "__main__":
    start()
