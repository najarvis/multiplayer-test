import socket
import sys
import pickle
import base64

HOST = '104.236.8.97'
PORT = 3333

class Client(object):

    def __init__(self, host=HOST):
        self.clientsocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.host = host

    def send_message(self, msg):
        # TODO: Make this a separate thread and interpolate until an update comes in.
        self.clientsocket.sendto(msg, (self.host, PORT))
        self.clientsocket.settimeout(1)

        try:
            reply, addr = self.clientsocket.recvfrom(1024)

            return pickle.loads(base64.b64decode(reply))

        except socket.timeout:
            print("Lost a packet! Using the last recieved data.")
            return None
