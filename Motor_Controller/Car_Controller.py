import threading

import Motor_Controller.video_dir
import Motor_Controller.car_dir
import Motor_Controller.motor
from Main_Controller.global_queues import *

offset = 0

class Car_Controller(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)

        Motor_Controller.video_dir.setup()
        Motor_Controller.car_dir.setup()
        Motor_Controller.motor.setup()  # Initialize the Raspberry Pi GPIO connected to the DC motor.
        Motor_Controller.video_dir.home_x_y()
        Motor_Controller.car_dir.home()

        self.ctrl_cmd = {
            'stop': Motor_Controller.motor.stop,  # Stop
            'move_forward': Motor_Controller.motor.forward,
            'move_backward': Motor_Controller.motor.backward,
            #'turn_left': Motor_Controller.car_dir.turn_left,
            #'turn_right': Motor_Controller.car_dir.turn_right,
            'turn_left': self.fine_turn_left(0),
            'turn_right': self.fine_turn_right(0),
            'forward_speed': lambda args: self.forward_speed(args),
            'backward_speed': lambda args: self.backward_speed(args),
            'set_angle': lambda args: self.setAngle(args),
            'x+': Motor_Controller.video_dir.move_increase_x,  # X+
            'x-': Motor_Controller.video_dir.move_decrease_x,  # X-
            'y+': Motor_Controller.video_dir.move_increase_y,  # Y+
            'y-': Motor_Controller.video_dir.move_decrease_y,  # Y-
            'xy_home': Motor_Controller.video_dir.home_x_y,  # home X_Y
            'set_speed': lambda args: self.setSpeed(args),
            'home': Motor_Controller.car_dir.home,
            'get_cpu_value': self.get_cpu_value,
        }

    def run(self):
        TO_MOTORS_Q_empty = TO_MOTORS_Q.empty
        TO_MOTORS_Q_get = TO_MOTORS_Q.get

        while True:
            if not TO_MOTORS_Q_empty():
                order, args = TO_MOTORS_Q_get()
                try:
                    if args is None:
                        self.ctrl_cmd[order]()
                    else:
                        self.ctrl_cmd[order](args)
                except Exception as e:
                    print("Error motor order:")
                    print(e)

    def setSpeed(self, speed):
        spd = int(speed)
        print('spd(int) =', spd)
        if spd < 24:
            spd = 24
        Motor_Controller.motor.setSpeed(spd)

    def fine_turn_left(self, val):
        global offset
        offset -= 1
        Motor_Controller.car_dir.calibrate(int(offset))

    def fine_turn_right(self, val):
        global offset
        offset += 1
        Motor_Controller.car_dir.calibrate(int(offset))


    def setAngle(self, angle):
        try:
            angle = int(angle)
            Motor_Controller.car_dir.turn(angle)
        except:
            print('Error: angle =', angle)

    def forward_speed(self, speed):
        try:
            spd = int(speed)
            Motor_Controller.motor.forwardWithSpeed(spd)
        except:
            print('Error speed =', speed)

    def backward_speed(self, speed):
        try:
            spd = int(speed)
            Motor_Controller.motor.backwardWithSpeed(spd)
        except:
            print('Error speed =', speed)

    def get_cpu_value(self):
        print('read cpu temp...')
        # temp = cpu_temp.read()
        # tcpCliSock.send('[%s] %0.2f' % (ctime(), temp))
