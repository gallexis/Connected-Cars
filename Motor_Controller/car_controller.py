import video_dir
import car_dir
import motor
from Main_Controller.global_queues import *

#ctrl_cmd = {'0': lambda x:   motor.forward(*arg),
#            'backward', 'left', 'right', 'stop', 'read cpu_temp', 'home', 'distance', 'x+', 'x-', 'y+', 'y-',
#            'xy_home'}

ctrl_cmd = {
    '0': motor.ctrl(0),  # Stop
    '1': motor.forward,
    '2': motor.backward,
    '3': car_dir.turn_left,
    '4': car_dir.turn_right,
    '5': lambda args: forward_speed(args),
    '6': lambda args: backward_speed(args),
    '7': lambda args: setAngle(args),
    '8': video_dir.move_increase_x,  # X+
    '9': video_dir.move_decrease_x,  # X-
    '10': video_dir.move_increase_y,  # Y+
    '11': video_dir.move_decrease_y,  # Y-
    '12': video_dir.home_x_y,  # home X_Y
    '13': lambda args: setSpeed(args),
    '14': car_dir.home,
    '15': print  # set_cpu_value,
}

video_dir.setup()
car_dir.setup()
motor.setup()  # Initialize the Raspberry Pi GPIO connected to the DC motor.
video_dir.home_x_y()
car_dir.home()

def setSpeed(speed):
    spd = int(speed)
    print(('spd(int) = %d' % spd))
    if spd < 24:
        spd = 24
    motor.setSpeed(spd)

def setAngle(angle):
    try:
        angle = int(angle)
        car_dir.turn(angle)
    except:
        print(('Error: angle =', angle))

def forward_speed(speed):
    try:
        spd = int(speed)
        motor.forwardWithSpeed(spd)
    except:
        print(('Error speed =', speed))

def backward_speed(speed):
    try:
        spd = int(speed)
        motor.backwardWithSpeed(spd)
    except:
        print(('Error speed =', speed))


def set_cpu_value():
    print('read cpu temp...')
    #temp = cpu_temp.read()
    #tcpCliSock.send('[%s] %0.2f' % (ctime(), temp))


def move_car():
    while True:
        order, args = TO_MOTORS_Q.get()
        try:
            if None == args:
                ctrl_cmd[order]()
            else:
                ctrl_cmd[order](args)
        except Exception as e:
            print("Error motor order:")
            print(e)
