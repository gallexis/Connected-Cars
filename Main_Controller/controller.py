import socket
import os
import gevent


class Master_manager:
    def __init__(self, data, Controller_IN, To_master, To_slave, To_Motors):
        self.type = data["message_type"]
        self.order = data["message_order"]
        self.args = data["args"]

        self.Controller_IN = Controller_IN

        self.To_master = To_master
        self.To_slave = To_slave
        self.To_Motors = To_Motors

    def alert_manager(self):
        pass

    def driving_manager(self):
        if self.order == "move_forward":
            pass
        elif self.order == "move_backward":
            pass

    def connection_manager(self):
        pass

    def routing(self):
        if self.type == "alert":
            self.alert_manager()
        elif self.type == "driving":
            self.driving_manager()
        elif self.type == "connection":
            self.connection_manager()


class Controller:
    def __init__(self, Controller_IN, To_master, To_slave, To_Motors):
        self.Controller_IN = Controller_IN

        self.To_master = To_master
        self.To_slave = To_slave
        self.To_Motors = To_Motors

        gevent.joinall([
            gevent.spawn(self.manager_ccp_receive),
            gevent.spawn(self.manager_ccp_send),
            gevent.spawn(self.manager_images)
        ])

    def start(self):
        while True:
            if not self.Controller_IN.empty():
                data = self.Controller_IN.get()
                self.routing(data)

    def routing(self, data):
        message_is_from = data["from"]

        if message_is_from == "master":
            Master_manager(data)
        elif message_is_from == "slave":
            self.Slave_manager(data)
        elif message_is_from == "camera":
            self.Camera_manager(data)
        else:
            print("unknown destination")

    def Slave_manager(self, data):

    def Motors_manager(self, data):

    def Camera_manager(self, data):
        pass


    """
    def controller(self):
        pass


    def manager_images(self):
        while True:
            data=self.queue_images.get()
            if interprete_image(data) == obstacle:
                self.queue_motor.put(stop)
                self.CCP.send(obstacle)

    def manager_ccp_receive(self):
        while True:
            data = self.queue_ccp_receive.get()

            if data == motor
                self.queue_motor.put(data)

    """
    def manager_ccp_send(self):
        while True:
            data = self.queue_ccp_send.get()

            if data == (image: obstacle):
            self.queue_motor.put(stop)
            self.queue_ccp_send.put(stop)
