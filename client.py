import socket
import sys
import pickle
import base64

HOST = '104.236.8.97'
PORT = 3333

class Client(object):

    def __init__(self):
        self.clientsocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

        #self.clientsocket.connect((host, port))

    def send_message(self, msg):
        self.clientsocket.sendto(msg, (HOST, PORT))

        reply, addr = self.clientsocket.recvfrom(1024)

        print("Server reply: {}".format(reply))

def run():
    client = Client()
    b64_msg = base64.base64encode(pickle.dumps([1, 2, 3]))
    client.send_message(b64_msg)

if __name__ == "__main__":
    run()
