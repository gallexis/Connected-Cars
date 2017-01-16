import socket
import time
import _thread

import CCP.packets
from Main_Controller.global_queues import *

import sys
# IP of all masters: 192.168.1.1
# IP of all slaves:  192.168.1.2

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
                try:
                    self.sock.send(data.encode('utf-8'))
                except Exception as e:
                    print("Error send to master: ")
                    print(e)

    def receive_from_master(self):
        while self.master_alive:
            try:
                data = self.sock.recv(255)
                if sys.getsizeof(data) <= 0:
                    print("remote car disconnected")
                    self.master_alive = False
                    return

                msg = CCP.packets.get_message(data)
                if msg == None:
                    print("error decoding received packet... (receive_from_master)")
                    continue

                msg["from"] = "master"

                CONTROLLER_IN_Q.put(msg)


            except Exception as e:
                print("error receive_from_master")
                print(e)
                self.master_alive = False


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
                try:
                    self.sock.send(data)
                except Exception as e:
                    print("Error send_to_slave: ")
                    print(e)

    def receive_from_slave(self):
        while self.slave_alive:
            try:
                data = self.sock.recv(255)
                if data <= 0:
                    print("remote car disconnected")
                    self.slave_alive = False
                    return

                msg = CCP.packets.get_message(data)
                if msg == None:
                    print("error decoding received packet... (receive_from_slave)")
                    continue

                msg["from"] = "slave"
                CONTROLLER_IN_Q.put(msg)

            except Exception as e:
                print("error receive_from_slave")
                print(e)
                self.slave_alive = False
                return
