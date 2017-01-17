from Main_Controller.global_queues import *
from CCP.packets import *


class Slave_controller:
    def __init__(self):
        pass

    def handle_message(self, data):
        self.data = data
        self.type = data["message_type"]
        self.order = data["message_order"]
        self.args = data["args"]

    def routing(self):
        if self.type == "alert":
            self.alert_manager()
        elif self.type == "driving":
            # The slave must not send driving packets to his master
            pass
        elif self.type == "connection":
            self.connection_manager()
        else:
            print("error routing in Slave_controller")


    def alert_manager(self):
        pass

    def connection_manager(self):
        pass


