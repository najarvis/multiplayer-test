import socket
import sys

HOST = '104.236.8.97'
PORT = 3333

class Client(obect):

    def __init__(self):
        self.clientsocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

        #self.clientsocket.connect((host, port))

    def send_message(self, msg):
        self.clientsocket.sendto(msg, (HOST, PORT))

        reply, addr = self.clientsocket.recvfrom(1024)

        print("Server reply: {}".format(reply))

def run():
    client = Client()
    for i in range(10):
        client.send_message(str(i))

if __name__ == "__main__":
    run()
