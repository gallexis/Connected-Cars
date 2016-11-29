import gevent
from gevent import Greenlet
import socket
import sys

def server():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(('', 15555))

    while True:
        s.listen(5)
        client, address = s.accept()
        print("{} connected".format(address))

        response = client.recv(255)
        if response != "":
            print(response)

    print("Close")
    client.close()
    stock.close()

def client():
    hote = "localhost"
    port = 15555

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((hote, port))
    print("Connection on {}".format(port))

    s.send(u"Hey my name is Olivier!")

    print("Close")
    s.close()


t1 = gevent.spawn(server)
t1.join()

gevent.joinall([
    gevent.spawn(server),
    gevent.spawn(client),
])





