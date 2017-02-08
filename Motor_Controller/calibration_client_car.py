import RPi.GPIO as GPIO
import Motor_Controller.video_dir
import Motor_Controller.car_dir
import Motor_Controller.motor
import os,sys
from socket import *
from time import ctime

IP = ""  # Server(Raspberry Pi) IP address
PORT = 21567
BUFSIZ = 1024

tcpSerSock = socket(AF_INET, SOCK_STREAM)




# connections are full, others will be rejected.
def setup():
    global offset_x, offset_y, offset, forward0, forward1
    offset_x = 0
    offset_y = 0
    offset = 0
    forward0 = 'True'
    forward1 = 'False'
    try:
        for line in open('config'):
            s = line.split("=")
            s0 = s[0].split()
            s1 = s[1].split()

            if s0 == 'offset_x':
                offset_x = int(s1)
                print('offset_x =', offset_x)
            elif s0 == 'offset_y':
                offset_y = int(s1)
                print('offset_y =', offset_y)
            elif s0 == 'offset':
                offset = int(s1)
                print('offset =', offset)
            elif s0 == "forward0":
                forward0 = s1
                print('turning0 =', forward0)
            elif s0 == "forward1":
                forward1 = s1
                print('turning1 =', forward1)
    except:
        print('no config file, set config to original')

    Motor_Controller.video_dir.setup()
    Motor_Controller.car_dir.setup()
    Motor_Controller.motor.setup()

    Motor_Controller.video_dir.calibrate(offset_x, offset_y)
    Motor_Controller.car_dir.calibrate(offset)


def REVERSE(x):
    if x == 'True':
        return 'False'
    elif x == 'False':
        return 'True'


def loop():
    global offset_x, offset_y, offset, forward0, forward1
    while True:
        print('Waiting for connection...')

        while True:
            try:
                data = tcpSerSock.recv(BUFSIZ)
                if len(data) <= 0:
                    print("Server disconnected.")
                    return

                data = data.decode("utf-8")


            except Exception as e:
                print("Error received data from server: ", e)
                return

            # --------Motor calibration----------
            if data == 'motor_run':
                print('motor moving forward')
                Motor_Controller.motor.setSpeed(50)
                Motor_Controller.motor.motor0(forward0)
                Motor_Controller.motor.motor1(forward1)
            elif data[0:9] == 'leftmotor':
                forward0 = data[9:]
                Motor_Controller.motor.motor0(forward0)
            elif data[0:10] == 'rightmotor':
                forward1 = data[10:]
                Motor_Controller.motor.motor1(forward1)

            # -------------Added--------------
            elif data == 'leftreverse':
                if forward0 == "True":
                    forward0 = "False"
                else:
                    forward0 = "True"
                print("left motor reversed to", forward0)
                Motor_Controller.motor.motor0(forward0)
            elif data == 'rightreverse':
                if forward1 == "True":
                    forward1 = "False"
                else:
                    forward1 = "True"
                print("right motor reversed to", forward1)
                Motor_Controller.motor.motor1(forward1)
            elif data == 'motor_stop':
                print('motor stop')
                Motor_Controller.motor.stop()
            # ---------------------------------

            # -------Turing calibration------
            elif data[0:7] == 'offset=':
                offset = int(data[7:])
                Motor_Controller.car_dir.calibrate(offset)
            # --------------------------------

            # ----------Mount calibration---------
            elif data[0:8] == 'offsetx=':
                offset_x = int(data[8:])
                print('Mount offset x', offset_x)
                Motor_Controller.video_dir.calibrate(offset_x, offset_y)
            elif data[0:8] == 'offsety=':
                offset_y = int(data[8:])
                print('Mount offset y', offset_y)
                Motor_Controller.video_dir.calibrate(offset_x, offset_y)
            # ----------------------------------------

            # -------Turing calibration 2------
            elif data[0:7] == 'offset+':
                offset = offset + int(data[7:])
                print('Turning offset', offset)
                Motor_Controller.car_dir.calibrate(offset)
            elif data[0:7] == 'offset-':
                offset = offset - int(data[7:])
                print('Turning offset', offset)
                Motor_Controller.car_dir.calibrate(offset)
            # --------------------------------

            # ----------Mount calibration 2---------
            elif data[0:8] == 'offsetx+':
                offset_x = offset_x + int(data[8:])
                print('Mount offset x', offset_x)
                Motor_Controller.video_dir.calibrate(offset_x, offset_y)
            elif data[0:8] == 'offsetx-':
                offset_x = offset_x - int(data[8:])
                print('Mount offset x', offset_x)
                Motor_Controller.video_dir.calibrate(offset_x, offset_y)
            elif data[0:8] == 'offsety+':
                offset_y = offset_y + int(data[8:])
                print('Mount offset y', offset_y)
                Motor_Controller.video_dir.calibrate(offset_x, offset_y)
            elif data[0:8] == 'offsety-':
                offset_y = offset_y - int(data[8:])
                print('Mount offset y', offset_y)
                Motor_Controller.video_dir.calibrate(offset_x, offset_y)
            # ----------------------------------------

            # ----------Confirm--------------------
            elif data == 'confirm':
                ROOT_DIR = os.path.dirname(os.path.abspath(__file__))

                config = 'offset_x = %s\noffset_y = %s\noffset = %s\nforward0 = %s\nforward1 = %s' % (
                    offset_x, offset_y, offset, forward0, forward1)
                print('')
                print('*********************************')
                print(' You are setting config file to:')
                print('*********************************')
                print(config)
                print('*********************************')
                print('')
                fd = open(ROOT_DIR+'/config', 'w')
                fd.write(config)
                fd.close()

                Motor_Controller.motor.stop()
                tcpSerSock.close()
                quit()
            else:
                print('Command Error! Cannot recognize command: ', data)


def main(master_address):

    IP = master_address
    try:
        tcpSerSock.connect((IP, PORT))
    except Exception as e:
        print(" Error connection to server: ", e)
        sys.exit(1)

    try:
        setup()
        loop()
    except KeyboardInterrupt:
        tcpSerSock.close()
