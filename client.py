import socket

def run():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    host = '104.236.8.97'
    port = 3333

    s.connect((host, port))
    tm = s.recv(1024)

    s.close()

    print("The time got from the server is {}".format(tm.decode('ascii')))

if __name__ == "__main__":
    run()
