import socket
import time
import _thread
import struct


import CCP.packets
from Main_Controller.global_queues import *

# IP of all masters: 192.168.1.1
# IP of all slaves:  192.168.1.2

##########
# MASTER
##########
class Master_connection:
    def __init__(self):
        self.sock = self.connect_to_master()
        if self.sock == None:
            print("sock == none, cannot connect to master.")
            return

        self.master_alive = True

        try:
            _thread.start_new_thread(self.receive_from_master, ())
            _thread.start_new_thread(self.send_to_master, ())
        except:
            print("Error: unable to start Master_connection's thread")


    def connect_to_master(self):
        connected = 5
        sock = None

        while connected > 0:
            try:
                print("Connection to master...")
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.bind(("192.168.43.41", 0))
                sock.connect(("192.168.43.202", 3000))
                print("Connected to master")
                break
            except:
                connected -= 1
                print("Error master connection")
                time.sleep(4)

        return sock

    def send_to_master(self):
        while self.master_alive:
            if not TO_MASTER_Q.empty():
                data = TO_MASTER_Q.get()
                to_send(self.sock, data)


    def receive_from_master(self):
        while self.master_alive:
            self.master_alive = to_receive(self.sock, "master")


##########
# SLAVE
##########
class Slave_connection:
    def __init__(self):
        self.sock = self.wait_for_slave_connection()
        if self.sock == None:
            print("sock == none, cannot connect to slave.")
            return

        self.slave_alive = True

        try:
            _thread.start_new_thread(self.receive_from_slave, ())
            _thread.start_new_thread(self.send_to_slave, ())
        except:
            print("Error: unable to start Slave_connection's thread")

    def wait_for_slave_connection(self):
        connected = False
        car_sock = None
        tries = 5

        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.bind(('', 3000))
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.listen(5)

        while not connected and tries > 0:
            try:
                print("waiting for incoming slave car connection...")
                car_sock, _ = sock.accept()
                connected = True
            except:
                print("Error slave connection")
                tries -= 1
                time.sleep(4)

        return car_sock

    def send_to_slave(self):
        while self.slave_alive:
            if not TO_SLAVE_Q.empty():
                data = TO_SLAVE_Q.get()
                to_send(self.sock, data)

    def receive_from_slave(self):
        while self.slave_alive:
            self.slave_alive = to_receive(self.sock, "slave")


###
# Generic functions
###
def to_send(sock, data):
    try:
        length = len(data)
        data = struct.pack("<H", length) + data
        print("to send:")
        print(data)
        sock.send(data)

    except Exception as e:
        print("Error to_send: ")
        print(e)


def to_receive(sock, rout_from):
    try:
        length = sock.recv(2)
        length = struct.unpack("<H", length)[0]

        data = recvall(sock, length)
        if len(data) <= 0:
            raise ("remote car disconnected")

        msg = CCP.packets.get_message(data)
        print("debug:::")
        print(msg)
        if msg == None:
            print("error decoding received packet... ")
            return True

        msg["from"] = rout_from
        CONTROLLER_IN_Q.put(msg)

    except Exception as e:
        print("error to_receive")
        print(e)
        return False


def recvall(sock, length):
    parts = []

    while length > 0:
        print("loop")
        part = sock.recv(length)
        if not part:
            raise EOFError('socket closed with %d bytes left in this part'.format(length))

        length -= len(part)
        parts.append(part)

    return b''.join(parts)
