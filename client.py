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
        #self.clientsocket.connect((host, port))

    def send_message(self, msg):
        self.clientsocket.sendto(msg, (self.host, PORT))

        reply, addr = self.clientsocket.recvfrom(1024)

        return pickle.loads(base64.b64decode(reply))

def run():
    client = Client()
    b64_msg = base64.b64encode(pickle.dumps([1, 2, 3, 4]))
    print(client.send_message(b64_msg))

if __name__ == "__main__":
    run()
