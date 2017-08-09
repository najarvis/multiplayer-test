import socket
import os
import pickle
import base64
import time

HOST = ''
PORT = 3333

class Server(object):

    def __init__(self):
        # Create a UDP socket
        self.serversocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

        # Accepts connections from outside sources on this PORT
        self.serversocket.bind((HOST, PORT))

        # Store the positions of all players
        self.clients = {}

        self.curr_time = time.time()

    def update(self):

        # Find how long it has been since the last update
        # TODO: Make this it's own function
        old_time = self.curr_time
        self.curr_time = time.time()
        delta = self.curr_time - old_time

        for client in list(self.clients.keys()):
            # increase how long it has been since we've seen each client
            self.clients[client][2] += delta;

            # If it has been over 3 seconds, assume they left
            if self.clients[client][2] > 3:
                del self.clients[client]

        # Get data and decode it.
        data, addr = self.serversocket.recvfrom(1024)

        if not data:
            return

        formatted = pickle.loads(base64.b64decode(data.strip()))

        # print('Message from {}:{} - {}'.format(addr[0], addr[1], formatted))


        # If we don't know about the player, list them.
        if addr not in self.clients:
            self.clients[addr] = [0, 0, 0] # x_pos, y_pos, time_since_last_msg

        # Reset the how long it has been since we've seen them.
        self.clients[addr][2] = 0
        try:
            # [w, a, s, d]
            if formatted[0]: self.clients[addr][1] -= 5 # w
            if formatted[2]: self.clients[addr][1] += 5 # s
            if formatted[1]: self.clients[addr][0] -= 5 # a
            if formatted[3]: self.clients[addr][0] += 5 # d

            # So we respond to the player with an array in the form:
            # [their pos, [all other players positions]]
            reply = [
              (self.clients[addr][0], self.clients[addr][1])
              [(pos[0], pos[1]) for pos in self.clients.values() if pos != self.clients[addr]]]

            # encode the reply and send it off
            enc_reply = base64.b64encode(pickle.dumps(reply))
            self.serversocket.sendto(enc_reply, addr)

        except IndexError:
            print("Bad data format!")
            self.serversocket.sendto(base64.b64encode(pickle.dumps("Bad data format!")), addr)

def start():
    game_server = Server()
    while True:
        game_server.update()


if __name__ == "__main__":
    start()
