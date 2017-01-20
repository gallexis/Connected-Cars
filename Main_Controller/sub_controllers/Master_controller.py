from Main_Controller.global_queues import *
from CCP.packets import message_type


class Master_controller:
    def __init__(self):
        pass

    def handle_message(self, data):
        self.data = data
        self.type = data["message_type"]
        self.order = data["message_order"]
        self.args = data["args"]

        self.routing()

    def routing(self):

        if self.type == "alert":
            self.alert_manager()
        elif self.type == "driving":
            self.driving_manager()
        elif self.type == "connection":
            self.connection_manager()
        else:
            print("error routing in Master_controller")

    def alert_manager(self):
        pass

    def driving_manager(self):
        # send the same driving order to the slave
        TO_SLAVE_Q.put(self.data)

        # send the order "move_forward" to the motors
        #TO_MOTORS_Q.put((self.order, self.args))


    def connection_manager(self):
        pass

