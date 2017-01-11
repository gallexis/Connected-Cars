import socket
import gevent
import CCP.packets
import time

# IP of all masters: 192.168.1.1
# IP of all slaves:  192.168.1.2

class Master_connection:
    def __init__(self, Controller_IN, To_master):
        self.Controller_IN = Controller_IN
        self.To_master = To_master

        self.sock = self.connect_to_master()
        if self.sock == None:
            print("sock == none, cannot connect to master.")
            return

        self.master_alive = True

        gevent.joinall([
            gevent.spawn(self.receive_from_master()),
            gevent.spawn(self.send_to_master()),
        ])

    def connect_to_master(self):
        connected = 5
        sock = None

        while connected > 0:
            try:
                print("Connection to master...")
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.bind(("192.168.1.2", 0))
                sock.connect(("192.168.1.1", 3000))
                break
            except:
                connected -= 1
                print("Error master connection")
                time.sleep(1)

        return sock

    def send_to_master(self):
        while self.master_alive:
            if not self.To_master.empty():
                data = self.To_master.get()
                self.sock.send(data)

    def receive_from_master(self):
        while self.master_alive:
            try:
                data = self.sock.recv(255)
                if data <= 0:
                    print("remote car disconnected")
                    self.master_alive = False
                    return

                msg = CCP.packets.get_message(data)
                msg["from"] = "master"
                self.Controller_IN.put(msg)

            except:
                print("error receive_from_master")
                self.master_alive = False


class Slave_connection:
    def __init__(self, Controller_IN, To_slave):
        self.Controller_IN = Controller_IN
        self.To_slave = To_slave

        self.sock = self.wait_for_slave_connection()
        if self.sock == None:
            print("sock == none, cannot connect to slave.")
            return

        self.slave_alive = True

        gevent.joinall([
            gevent.spawn(self.receive_from_slave()),
            gevent.spawn(self.send_to_slave()),
        ])

    def wait_for_slave_connection(self):
        connected = False
        car_sock = None
        tries = 5

        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.bind(('', 15555))
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
                time.sleep(1)

        return car_sock

    def send_to_slave(self):
        while self.slave_alive:
            if not self.To_slave.empty():
                data = self.To_slave.get()
                self.sock.send(data)

    def receive_from_slave(self):
        while self.slave_alive:
            try:
                data = self.sock.recv(255)
                if data <= 0:
                    print("remote car disconnected")
                    self.slave_alive = False
                    return

                msg = CCP.packets.get_message(data)
                msg["from"] = "slave"
                self.Controller_IN.put(msg)

            except:
                print("error receive_from_slave")
                self.slave_alive = False
                return
