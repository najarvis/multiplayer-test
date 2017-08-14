import socket
import os
import pickle
import base64
import time
import client_data
import threading

HOST = ''
PORT = 3333
EXIT_FLAG = False

class Server(object):

    def __init__(self):
        # Create a UDP socket
        self.serversocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

        # Accepts connections from outside sources on this PORT
        self.serversocket.bind((HOST, PORT))
        print("Server started on {}:{}".format(HOST, PORT))

        # Store the positions of all players
        self.clients = {}

class InputThread(threading.Thread):

    def __init__(self, threadID, server):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.server = server

    def run(self):
        while not EXIT_FLAG:
            try:
            # Get data and decode it.
                data = False
                data, addr = self.server.serversocket.recvfrom(1024)

                if not data:
                    # No data got sent.
                    continue

            except Exception:
                continue

            formatted = pickle.loads(base64.b64decode(data.strip()))

            # If we don't know about the player, list them.
            if addr not in self.server.clients:
                print("New client - {} Connected!".format(addr))
                self.server.clients[addr] = client_data.ClientData(addr)
                # self.clients[addr] = [0, 0, 0] # x_pos, y_pos, time_since_last_msg

            # Reset the how long it has been since we've seen them.
            self.server.clients[addr].CLIENT_AGE = 0
            self.server.clients[addr].last_input = formatted

class UpdateThread(threading.Thread):

    def __init__(self, threadID, server):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.server = server

        self.curr_time = time.time()
        self.time_since_last_update = 0
        self.update_length = 1/30 # Update 30x per second

    def run(self):
        while not EXIT_FLAG:
            # Find how long it has been since the last update
            old_time = self.curr_time
            self.curr_time = time.time()
            delta = self.curr_time - old_time
            self.time_since_last_update += delta

            for client in list(self.server.clients.keys()):
                # increase how long it has been since we've seen each client
                self.server.clients[client].CLIENT_AGE += delta;

                # If it has been over 3 seconds, assume they left
                if self.server.clients[client].CLIENT_AGE > 3:
                    del self.server.clients[client]

            # If we are multiple steps over, this will let the physics update as many times as needed.
            if self.time_since_last_update >= self.update_length:
                while self.time_since_last_update >= self.update_length:
                    self.time_since_last_update -= self.update_length

                    for addr in self.server.clients.keys():
                        try:
                            self.server.clients[addr].update(self.server.clients[addr].last_input)
                            # if formatted[3]: FIRE

                        except IndexError:
                            print("Bad data format!")
                            self.server.serversocket.sendto(base64.b64encode(pickle.dumps("Bad data format!")), addr)

                for addr in self.server.clients.keys():
                    # So we respond to the player with an array in the form:
                    # [their pos, [all other players positions]]
                    reply = [
                      self.server.clients[addr].get_transmit_data(),
                      [c_data.get_transmit_data() for c_data in self.server.clients.values() if c_data.id != addr]]

                    # encode the reply and send it off
                    enc_reply = base64.b64encode(pickle.dumps(reply))
                    self.server.serversocket.sendto(enc_reply, addr)

def start():
    game_server = Server()
    input_thread = InputThread(1, game_server)
    update_thread = UpdateThread(2, game_server)

    input_thread.start()
    update_thread.start()
    
    #while True:
        #game_server.handle_input()
        #game_server.update()


if __name__ == "__main__":
    start()
