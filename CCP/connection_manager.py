import os, sys
import socket
import threading
import time
import _thread
import struct

import logging

import CCP.packets
from Main_Controller.global_queues import *

# IP of all masters: 192.168.1.1
# IP of all slaves:  192.168.1.2

##########
# Camera
##########
class Images_Recognition(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)

        self.orders_available = [
            'stop',
            'move_forward',
            'move_backward',
            'turn_left',
            'turn_right',
        ]
        self.sock_addr = '/tmp/connected_cars.sock'

        # Make sure the socket does not already exist
        try:
            os.unlink(self.sock_addr)
        except:
            if os.path.exists(self.sock_addr):
                os.remove(self.sock_addr)
                logging.warning("removed " + self.sock_addr)

        self.sock = self.wait_for_camera()
        if self.sock is None:
            logging.warning("Error connection to server")
            sys.exit(1)

    def wait_for_camera(self):
        sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        sock.bind(self.sock_addr)

        logging.info('Waiting for connection to camera module')

        try:
            connection, client_address = sock.accept()
            return connection
        except Exception as e:
            logging.warning("Error waiting for camera: " + e.__str__())
            return None

    def run(self):
        while True:
            order = self.sock.recv(20)
            if order in self.orders_available:
                # the orders from the camera are considered as the same as the masters' orders
                CONTROLLER_IN_Q.put({"from": "master", "message_type": "driving", "message_order": order, "args": None})
            else:
                logging.warning("order not in orders_available: ")
                logging.warning(order)


##########
# MASTER
##########
class Master_connection:
    def __init__(self):
        self.sock = self.connect_to_master()
        if self.sock == None:
            logging.warning("sock == none, cannot connect to master.")
            return

        self.master_alive = True

        try:
            _thread.start_new_thread(self.receive_from_master, ())
            _thread.start_new_thread(self.send_to_master, ())
        except Exception as e:
            logging.warning("Error: unable to start Master_connection's thread: " + e.__str__())


    def connect_to_master(self):
        connected = 5
        sock = None

        while connected > 0:
            try:
                logging.info("Connection to master...")
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                #sock.bind(("192.168.43.3", 0))
                sock.connect(("192.168.43.202", 3000))
                logging.info("Connected to master")
                break
            except Exception as e :
                connected -= 1
                logging.warning("Error master connection")
                logging.warning(e.__str__())
                time.sleep(4)

        return sock

    def send_to_master(self):
        TO_MASTER_Q_get = TO_MASTER_Q.get

        while self.master_alive:
            data = TO_MASTER_Q_get()
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
            logging.warning("sock == none, cannot connect to slave.")
            return

        self.slave_alive = True

        try:
            _thread.start_new_thread(self.receive_from_slave, ())
            _thread.start_new_thread(self.send_to_slave, ())
        except Exception as e:
            logging.warning("Error: unable to start Slave_connection's thread" + e.__str__())

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
                logging.info("Waiting for incoming slave car connection...")
                car_sock, _ = sock.accept()
                connected = True
            except:
                logging.info("Error slave connection")
                tries -= 1
                time.sleep(4)

        return car_sock

    def send_to_slave(self):
        TO_SLAVE_Q_get = TO_SLAVE_Q.get

        while self.slave_alive:
            data = TO_SLAVE_Q_get()
            print("to send", data)
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
        sock.send(data)

    except Exception as e:
        logging.warning("Error to_send: " + e.__str__())


def to_receive(sock, rout_from):
    try:
        length = sock.recv(2)
        length = struct.unpack("<H", length)[0]

        data = recvall(sock, length)
        if len(data) <= 0:
            raise ("remote car disconnected")

        msg = CCP.packets.get_message(data)
        #print("debug CCP.packets.get_message:")
        #print(msg)
        if msg == None:
            logging.warning("Error decoding received packet... ")
            return True

        msg["from"] = rout_from
        CONTROLLER_IN_Q.put(msg)
        return True

    except Exception as e:
        logging.warning("Error to_receive:" + e.__str__())
        return False


def recvall(sock, length):
    parts = []
    recv = sock.recv
    append = parts.append

    while length > 0:
        part = recv(length)
        if not part:
            raise EOFError('Socket closed with %d bytes left in this part'.format(length))

        length -= len(part)
        append(part)

    return b''.join(parts)
