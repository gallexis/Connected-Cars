import sys
import logging


def main():
    # logging.basicConfig(filename='example.log', level=logging.DEBUG)
    logging.basicConfig(level=logging.INFO)  # info - debug - warning

    if len(sys.argv) > 1:

        # computer
        if sys.argv[1] == "pc":
            from CCP.Computer import Computer_controller
            Computer_controller.Computer_controller()

        elif sys.argv[1] == "cali-car":
            import Motor_Controller.calibration_client_car
            Motor_Controller.calibration_client_car.main()

        elif sys.argv[1] == "cali-pc":
            import CCP.Computer.calibration_server_computer
            CCP.Computer.calibration_server_computer.main()

        else:
            logging.warning("error arg")

    #car
    else:
        from Motor_Controller import Car_Controller
        from Images_Recognition import void
        from CCP import connection_manager
        from Main_Controller import Main_Controller

        car_controller = Car_Controller.Car_Controller().start()
        main_controller = Main_Controller.Main_Controller().start()
        master_connection = connection_manager.Master_connection()
        slave_connection = connection_manager.Slave_connection()
        # images_recognition = Images_Recognition.Images_Recognition().start()


        main_controller.join()
        logging.info("main_controller thread: terminated")
        car_controller.join()
        logging.info("car_controller thread: terminated")



if __name__ == '__main__':
    main()