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

    def alert_manager(self):
        pass

    def driving_manager(self):
        # decoded_order = reversed_message_order[self.order]

        # send the same driving order to the slave
        TO_SLAVE_Q.put(self.data)

        # send the order "move_forward" to the motors
        TO_MOTORS_Q.put(self.order, self.args)


    def connection_manager(self):
        pass

    def routing(self):
        type = message_type[self.type]

        if type == "alert":
            self.alert_manager()
        elif type == "driving":
            self.driving_manager()
        elif type == "connection":
            self.connection_manager()
