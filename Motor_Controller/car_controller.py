#!/usr/bin/env python
import RPi.GPIO as GPIO
import video_dir
import car_dir
import motor
import os
from socket import *
from time import ctime  # Import necessary modules

ctrl_cmd = {'0: (motor.forward,arg)', 'backward', 'left', 'right', 'stop', 'read cpu_temp', 'home', 'distance', 'x+', 'x-', 'y+', 'y-',
            'xy_home'}



video_dir.setup()
car_dir.setup()
motor.setup()  # Initialize the Raspberry Pi GPIO connected to the DC motor.
video_dir.home_x_y()
car_dir.home()


def move_car(receving_queue):
    while True:
        data = receving_queue.get()
        #log data

        if data == ctrl_cmd[0]:
            print('motor moving forward')
            motor.forward()
        elif data == ctrl_cmd[1]:
            print('recv backward cmd')
            motor.backward()
        elif data == ctrl_cmd[2]:
            print('recv left cmd')
            car_dir.turn_left()
        elif data == ctrl_cmd[3]:
            print('recv right cmd')
            car_dir.turn_right()
        elif data == ctrl_cmd[6]:
            print('recv home cmd')
            car_dir.home()
        elif data == ctrl_cmd[4]:
            print('recv stop cmd')
            motor.ctrl(0)
        elif data == ctrl_cmd[5]:
            print('read cpu temp...')
            #temp = cpu_temp.read()
            #sending_queue.put('[%s] %0.2f' % (ctime(), 0.0))
        elif data == ctrl_cmd[8]:
            print('recv x+ cmd')
            video_dir.move_increase_x()
        elif data == ctrl_cmd[9]:
            print('recv x- cmd')
            video_dir.move_decrease_x()
        elif data == ctrl_cmd[10]:
            print('recv y+ cmd')
            video_dir.move_increase_y()
        elif data == ctrl_cmd[11]:
            print('recv y- cmd')
            video_dir.move_decrease_y()
        elif data == ctrl_cmd[12]:
            print('home_x_y')
            video_dir.home_x_y()
        elif data[0:5] == 'speed':  # Change the speed
            print(data)
            numLen = len(data) - len('speed')
            if numLen == 1 or numLen == 2 or numLen == 3:
                tmp = data[-numLen:]
                print(('tmp(str) = %s' % tmp))
                spd = int(tmp)
                print(('spd(int) = %d' % spd))
                if spd < 24:
                    spd = 24
                motor.setSpeed(spd)
        elif data[0:5] == 'turn=':  # Turning Angle
            print(('data =', data))
            angle = data.split('=')[1]
            try:
                angle = int(angle)
                car_dir.turn(angle)
            except:
                print(('Error: angle =', angle))
        elif data[0:8] == 'forward=':
            print(('data =', data))
            spd = data[8:]
            try:
                spd = int(spd)
                motor.forwardWithSpeed(spd)
            except:
                print(('Error speed =', spd))
        elif data[0:9] == 'backward=':
            print(('data =', data))
            spd = data.split('=')[1]
            try:
                spd = int(spd)
                motor.backwardWithSpeed(spd)
            except:
                print(('ERROR, speed =', spd))

        else:
            print(('Command Error! Cannot recognize command: ' + data))
            break
