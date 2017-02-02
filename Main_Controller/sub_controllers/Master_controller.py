import logging
from Main_Controller.global_queues import *
from Main_Controller.sub_controllers.Generic_sub_controller import *
from CCP.packets import create_message

class Master_controller(Generic_sub_controller):
    def __init__(self):
        super().__init__()

    def alert_manager(self):
        pass

    def driving_manager(self):
        # send the same driving order to the slave
        TO_SLAVE_Q.put(create_message(self.type, self.order, self.args))

        # send the order "move_forward" to the motors
        TO_MOTORS_Q.put((self.order, self.args))

    def connection_manager(self):
        pass
