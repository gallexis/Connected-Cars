import socket
import gevent
import CCP.packets

# IP of all masters: 192.168.1.1
# IP of all slaves:  192.168.1.2


class Slave_connection_manager:
    def __init__(self, receiving_queue, sending_queue):
        self.slave_receiving_queue = receiving_queue
        self.slave_sending_queue = sending_queue

        self.sock = self.wait_for_slave_connection()

        gevent.joinall([
            gevent.spawn(self.receive_from_slave()),
            gevent.spawn(self.send_to_slave()),
        ])

    def wait_for_slave_connection(self):
        connected = False
        car_sock = None

        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.bind(('', 15555))
        sock.listen(5)

        while not connected:
            try:
                print("waiting for incoming slave car connection...")
                car_sock, _ = sock.accept()
                connected = True
            except:
                print("Error slave connection")

        return car_sock

    def send_to_slave(self):
        while True:
            if not self.slave_sending_queue.empty():
                data = self.slave_sending_queue.get()
                self.sock.send(data)

    def receive_from_slave(self):
        while True:
            try:
                data = self.sock.recv(255)
                if data <= 0:
                    print("remote car disconnected")

                msg = CCP.packets.get_message(data)
                self.slave_receiving_queue.put(msg)

            except:
                print("error receive_from_slave")


class Master_connection_manager:
    def __init__(self, receiving_queue, sending_queue):
        self.master_receiving_queue = receiving_queue
        self.master_sending_queue = sending_queue

        self.sock = self.connect_to_master()
        if self.sock == None:
            print("sock == none, cannot connect to master.")
            return

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
                connected = 0
            except:
                connected -= 1
                print("Error master connection")

        return sock

    def send_to_master(self):
        while True:
            if not self.master_sending_queue.empty():
                data = self.master_sending_queue.get()
                self.sock.send(data)

    def receive_from_master(self):
        while True:
            try:

                data = self.sock.recv(255)
                if data <= 0:
                    print("remote car disconnected")

                msg = CCP.packets.get_message(data)
                self.master_receiving_queue.put(msg)

            except:
                print("error receive_from_master")
