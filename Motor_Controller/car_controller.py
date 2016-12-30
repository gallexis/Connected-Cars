import RPi.GPIO as GPIO
import video_dir
import car_dir
import motor
import os
from socket import *
from time import ctime  # Import necessary modules

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
    '15': set_cpu_value,
}


#data = recv()
#{order:'2', arg:'toto'}

# if 0 < data 20

#    ctrl_cmd[data](arg)

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


def move_car(receving_queue):
    while True:
        data = receving_queue.get()
        data_split= data.split(' ')
        if len(data_split) > 1:
            ctrl_cmd[data_split[0]](data_split[1])
        else:
            ctrl_cmd[data_split[0]]()
