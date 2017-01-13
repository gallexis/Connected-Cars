import threading

from Main_Controller.global_queues import *
from Main_Controller.sub_controllers import Master_controller, Slave_controller  # ,Camera_controller


class Main_Controller(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)

        self.master_controller = Master_controller.Master_controller()
        self.slave_controller = Slave_controller.Slave_controller()
        # self.camera_controller = Camera_controller.Camera_controller()

    def run(self):
        while True:
            if not CONTROLLER_IN_Q.empty():
                data = CONTROLLER_IN_Q.get()
                self.routing(data)

    def routing(self, data):
        message_from = data["from"]

        if message_from == "master":
            self.master_controller.handle_message(data)
        elif message_from == "slave":
            self.slave_controller.handle_message(data)
        elif message_from == "camera":
            #self.camera_controller.handle_message(data)
            pass
        else:
            print("Unknown destination")
