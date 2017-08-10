import socket
import os
import pickle
import base64
import time
import client_data

HOST = ''
PORT = 3333

class Server(object):

    def __init__(self):
        # Create a UDP socket
        self.serversocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

        # Accepts connections from outside sources on this PORT
        self.serversocket.bind((HOST, PORT))
        print("Server started on {}:{}".format(HOST, PORT))

        # Store the positions of all players
        self.clients = {}

        self.curr_time = time.time()
        self.time_since_last_update = 0
        self.update_length = 1/30 # Update 30x per second

    def handle_input(self):
        # Get data and decode it.
        data, addr = self.serversocket.recvfrom(1024)

        if not data:
            return

        formatted = pickle.loads(base64.b64decode(data.strip()))

        # If we don't know about the player, list them.
        if addr not in self.clients:
            print("New client - {} Connected!".format(addr))
            self.clients[addr] = client_data.ClientData(addr)
            # self.clients[addr] = [0, 0, 0] # x_pos, y_pos, time_since_last_msg

        # Reset the how long it has been since we've seen them.
        self.clients[addr].CLIENT_AGE = 0
        self.clients[addr].last_input = formatted

    def update(self):

        # Find how long it has been since the last update
        # TODO: Make this it's own function
        old_time = self.curr_time
        self.curr_time = time.time()
        delta = self.curr_time - old_time
        self.time_since_last_update += delta

        for client in list(self.clients.keys()):
            # increase how long it has been since we've seen each client
            self.clients[client].CLIENT_AGE += delta;

            # If it has been over 3 seconds, assume they left
            if self.clients[client].CLIENT_AGE > 3:
                del self.clients[client]

        if self.time_since_last_update < self.update_length:
            return

        self.time_since_last_update -= self.update_length

        for addr in self.clients.keys():
            try:
                self.clients[addr].update(self.clients[addr].last_input)
                # if formatted[3]: FIRE

                # So we respond to the player with an array in the form:
                # [their pos, [all other players positions]]
                reply = [
                  self.clients[addr].get_transmit_data(),
                  [c_data.get_transmit_data() for c_data in self.clients.values() if c_data.id != addr]]

                # encode the reply and send it off
                enc_reply = base64.b64encode(pickle.dumps(reply))
                self.serversocket.sendto(enc_reply, addr)

            except IndexError:
                print("Bad data format!")
                self.serversocket.sendto(base64.b64encode(pickle.dumps("Bad data format!")), addr)

def start():
    game_server = Server()
    while True:
        game_server.handle_input()
        game_server.update()


if __name__ == "__main__":
    start()
