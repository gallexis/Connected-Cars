import queue
import sys
import subprocess

import gevent



def main():

    # computer
    if len(sys.argv) > 1:
        from CCP.Computer import Computer_controller

        Computer_controller.Computer_controller()


    #car
    else:
        from Motor_controller import car_controller
        from Images_Recognition import void
        from CCP import connection_manager
        from Main_Controller import Main_Controller

        gevent.joinall([
            gevent.spawn(connection_manager.Master_connection),
            gevent.spawn(connection_manager.Slave_connection),
            gevent.spawn(car_controller.move_car),
            gevent.spawn(Main_Controller.Main_Controller),
        ])



        # images_recognition.images_recognition(Controller_IN)

        # controller.start()



if __name__ == '__main__':
    main()


    # TODO: replace prints by loggings
