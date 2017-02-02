import logging
from Main_Controller.global_queues import *
from Main_Controller.sub_controllers.Generic_sub_controller import *
from CCP.packets import create_message


class Slave_controller(Generic_sub_controller):
    def __init__(self):
        super().__init__()

    def alert_manager(self):
        pass

    def driving_manager(self):
        pass

    def connection_manager(self):
        pass
