import threading

import Motor_Controller.video_dir
import Motor_Controller.car_dir
import Motor_Controller.motor
from Main_Controller.global_queues import *


class Car_Controller(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)

        Motor_Controller.video_dir.setup()
        Motor_Controller.car_dir.setup()
        Motor_Controller.motor.setup()  # Initialize the Raspberry Pi GPIO connected to the DC motor.
        Motor_Controller.video_dir.home_x_y()
        Motor_Controller.car_dir.home()

        self.ctrl_cmd = {
            '0': Motor_Controller.motor.ctrl(0),  # Stop
            '1': Motor_Controller.motor.forward,
            '2': Motor_Controller.motor.backward,
            '3': Motor_Controller.car_dir.turn_left,
            '4': Motor_Controller.car_dir.turn_right,
            '5': lambda args: self.forward_speed(args),
            '6': lambda args: self.backward_speed(args),
            '7': lambda args: self.setAngle(args),
            '8': Motor_Controller.video_dir.move_increase_x,  # X+
            '9': Motor_Controller.video_dir.move_decrease_x,  # X-
            '10': Motor_Controller.video_dir.move_increase_y,  # Y+
            '11': Motor_Controller.video_dir.move_decrease_y,  # Y-
            '12': Motor_Controller.video_dir.home_x_y,  # home X_Y
            '13': lambda args: self.setSpeed(args),
            '14': Motor_Controller.car_dir.home,
            '15': self.set_cpu_value,
        }

    def run(self):
        while True:
            if not TO_MOTORS_Q.empty():
                order, args = TO_MOTORS_Q.get()
                try:
                    if None == args:
                        self.ctrl_cmd[order]()
                    else:
                        self.ctrl_cmd[order](args)
                except Exception as e:
                    print("Error motor order:")
                    print(e)

    def setSpeed(self, speed):
        spd = int(speed)
        print(('spd(int) = %d' % spd))
        if spd < 24:
            spd = 24
        Motor_Controller.motor.setSpeed(spd)

    def setAngle(self, angle):
        try:
            angle = int(angle)
            Motor_Controller.car_dir.turn(angle)
        except:
            print(('Error: angle =', angle))

    def forward_speed(self, speed):
        try:
            spd = int(speed)
            Motor_Controller.motor.forwardWithSpeed(spd)
        except:
            print(('Error speed =', speed))

    def backward_speed(self, speed):
        try:
            spd = int(speed)
            Motor_Controller.motor.backwardWithSpeed(spd)
        except:
            print(('Error speed =', speed))

    def set_cpu_value(self):
        print('read cpu temp...')
        # temp = cpu_temp.read()
        # tcpCliSock.send('[%s] %0.2f' % (ctime(), temp))
