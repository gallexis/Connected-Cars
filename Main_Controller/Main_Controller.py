import socket
import os
import gevent

from Main_Controller.global_queues import *
from Main_Controller.sub_controllers import Master_controller, Slave_controller  # ,Camera_controller


class Controller:
    def __init__(self):
        pass

    def start(self):
        while True:
            if not CONTROLLER_IN_Q.empty():
                data = CONTROLLER_IN_Q.get()
                self.routing(data)

    def routing(self, data):
        message_from = data["from"]

        if message_from == "master":
            Master_controller.Master_controller(data)
        elif message_from == "slave":
            Slave_controller.Slave_controller(data)
        elif message_from == "camera":
            # Camera_controller.Camera_controller(data)
            pass
        else:
            print("Unknown destination")
