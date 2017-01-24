import socket
import sys
import os, time


class Sender:
    def __init__(self):
        self.orders_available = [
            'stop',
            'move_forward',
            'move_backward',
            'turn_left',
            'turn_right',
        ]
        self.sock_addr = '/tmp/connected_cars.sock'

        self.sock = self.connect()
        if self.sock is None:
            print
            "Error connection to server"
            sys.exit(1)

    def connect(self):
        sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        sock.bind(self.sock_addr)
        tries = 3

        while tries > 0:
            try:
                sock.connect(self.sock_addr)
                return sock
            except socket.error, msg:
                print
                sys.stderr, msg
                tries -= 1
                time.sleep(1)

        return None

    def send(self, order):
        if order in self.orders_available:
            self.sock.send(order)
