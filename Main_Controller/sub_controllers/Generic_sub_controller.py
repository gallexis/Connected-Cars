import logging
from abc import ABC, abstractmethod

class Generic_sub_controller(ABC):
    @abstractmethod
    def __init__(self):
        pass

    def handle_message(self, data):
        self.data = data
        self.type = data["message_type"]
        self.order = data["message_order"]
        self.args = data["args"]

        self.struct = {
            "alert": self.alert_manager,
            "driving": self.driving_manager,
            "connection": self.connection_manager,
        }

        self.routing()

    def routing(self):
        if self.type in ["alert", "driving", "connection"]:
            self.struct[self.type]()
        else:
            logging.warning("Error routing in Master_controller")

    @abstractmethod
    def alert_manager(self):
        raise NotImplementedError('subclass must be implemented')

    @abstractmethod
    def driving_manager(self):
        raise NotImplementedError('subclass must be implemented')

    @abstractmethod
    def connection_manager(self):
        raise NotImplementedError('subclass must be implemented')
