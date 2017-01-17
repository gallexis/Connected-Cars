import sys
import logging


def main():
    logging.basicConfig(filename='example.log', level=logging.DEBUG)

    # computer
    if sys.argv == "pc":
        from CCP.Computer import Computer_controller
        Computer_controller.Computer_controller()


    elif sys.argv == "cali":
        import Motor_Controller.calibration_client_car
        Motor_Controller.calibration_client_car.main()


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
        print("main_controller thread: terminated")
        car_controller.join()
        print("car_controller thread: terminated")



if __name__ == '__main__':
    main()
    # TODO: replace prints by loggings