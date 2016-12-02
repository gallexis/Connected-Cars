import queue
import sys

def main():
    # computer
    if len(sys.argv) > 1:

        import computer

        computer.server()
        q = queue.Queue()





    #car
    else:
        from Motor_controller import car_controller

        receving_queue = queue.Queue()
        sending_queue = queue.Queue()

        car_controller.move_car(receving_queue, sending_queue)



if __name__ == '__main__':
    main()