import socket
import os
import pickle
import base64

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

        # Store the positions of all players
        self.clients = {}

    def update(self):

        data, addr = self.serversocket.recvfrom(1024)
        formatted = pickle.loads(base64.b64decode(data.strip()))

        print('Message from {}:{} - {}'.format(addr[0], addr[1], formatted))

        # If we don't know about the player, list them.
        if addr not in self.clients:
            self.clients[addr] = [0, 0]

        try:
            # [w, a, s, d]
            if formatted[0]: self.clients[addr][1] -= 5 # w
            if formatted[2]: self.clients[addr][1] += 5 # s
            if formatted[1]: self.clients[addr][0] -= 5 # a
            if formatted[3]: self.clients[addr][0] += 5 # d

            reply = [self.clients[addr], [pos for pos in self.clients.values() if pos != self.clients[addr]]]
            enc_reply = base64.b64encode(pickle.dumps(self.clients[addr]))

            self.serversocket.sendto(reply, addr)

        except IndexError:
            print("Bad data format!")
            self.serversocket.sendto(base64.b64encode(pickle.dumps("Bad data format!")), addr)

def start():
    game_server = Server()
    while True:
        game_server.update()

if __name__ == "__main__":
    start()
