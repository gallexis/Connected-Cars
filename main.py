import queue
import sys
import subprocess


def networks_created(arg=""):
    networkCreated = -1
    tries = 3

    while networkCreated != 0 and tries > 0:
        networkCreated = subprocess.call("connection.sh " + arg)
        tries -= 1
        print("Netword created: ", networkCreated == 0)

    if networkCreated == 0:
        return True
    else:
        return False


def main():

    # computer
    if len(sys.argv) > 1:
        from CCP.Computer import Computer_controller

        if not networks_created("wlan0"):
            print("Failed to create the ad-hoc network")
            return

        Computer_controller.Computer_controller()


    #car
    else:
        from Motor_controller import car_controller
        from Images_Recognition import void
        from CCP import connection_manager

        Controller_IN = queue.Queue()

        To_master = queue.Queue()
        To_slave = queue.Queue()
        To_Motors = queue.Queue()

        if not networks_created():
            print("Failed to create the ad-hoc networks")
            return

        connection_manager.Master_connection(Controller_IN, To_master)
        connection_manager.Slave_connection(Controller_IN, To_slave)

        car_controller.move_car(To_Motors)

        # images_recognition.images_recognition(Controller_IN)

        # controller.start()



if __name__ == '__main__':
    main()