from Main_Controller.global_queues import *
from CCP.packets import reversed_message_type
from CCP.packets import reversed_message_order


class Slave_controller:
    def __init__(self):
        pass

    def handle_message(self, data):
        self.data = data
        self.type = data["message_type"]
        self.order = data["message_order"]
        self.args = data["args"]

    def alert_manager(self):
        pass

    def connection_manager(self):
        pass

    def routing(self):
        type = reversed_message_type[self.type]

        if type == "alert":
            self.alert_manager()
        elif type == "driving":
            # The slave must not send driving packets to his master
            pass
        elif type == "connection":
            self.connection_manager()
