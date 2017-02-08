import sys
import logging


def main():
    # logging.basicConfig(filename='example.log', level=logging.DEBUG)
    logging.basicConfig(level=logging.DEBUG)  # info - debug - warning
    master_address=""

    if len(sys.argv) > 2:


        #calibration car
        if sys.argv[1] == "cali-car":
            import Motor_Controller.calibration_client_car
            Motor_Controller.calibration_client_car.main(sys.argv[2])

        #car
        elif sys.argv[1] == "car":
            master_address = sys.argv[2]
            from Motor_Controller import Car_Controller
            from Images_Recognition import void
            from CCP import connection_manager
            from Main_Controller import Main_Controller

            car_controller = Car_Controller.Car_Controller().start()
            main_controller = Main_Controller.Main_Controller().start()
            master_connection = connection_manager.Master_connection(master_address)
            slave_connection = connection_manager.Slave_connection()
            images_recognition = connection_manager.Images_Recognition().start()

            main_controller.join()
            logging.info("main_controller thread: terminated")
            car_controller.join()
            logging.info("car_controller thread: terminated")

        else:
            logging.warning("error arg")



    elif len(sys.argv) == 2 :

        # computer
        if sys.argv[1] == "pc":
            from CCP.Computer import Computer_controller
            Computer_controller.Computer_controller()

        #calibration pc
        elif sys.argv[1] == "cali-pc":
            import CCP.Computer.calibration_server_computer
            CCP.Computer.calibration_server_computer.main()



if __name__ == '__main__':
    main()