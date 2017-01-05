import RPi.GPIO as GPIO
import video_dir
import car_dir
import motor
import sys
from socket import *
from time import ctime

HOST = '192.168.43.202'  # Server(Raspberry Pi) IP address
PORT = 21567
BUFSIZ = 1024  # buffer size
ADDR = (HOST, PORT)

tcpSerSock = socket(AF_INET, SOCK_STREAM)  # Create a socket

try:
    tcpSerSock.connect(ADDR)  # Connect with the server
except Exception as e:
    print("Error connection to server: ", e)
    sys.exit(1)

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
            if line[0:8] == 'offset_x':
                offset_x = int(line[11:-1])
                print(('offset_x ='), offset_x)
            if line[0:8] == 'offset_y':
                offset_y = int(line[11:-1])
                print(('offset_y ='), offset_y)
            if line[0:8] == 'offset =':
                offset = int(line[9:-1])
                print('offset =', offset)
            if line[0:8] == "forward0":
                forward0 = line[11:-1]
                print('turning0 =', forward0)
            if line[0:8] == "forward1":
                forward1 = line[11:-1]
                print('turning1 =', forward1)
    except:
        print('no config file, set config to original')

    video_dir.setup()
    car_dir.setup()
    motor.setup()
    video_dir.calibrate(offset_x, offset_y)
    car_dir.calibrate(offset)


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
            data = tcpSerSock.recv(BUFSIZ)  # Receive data sent from the client.
            # Analyze the command received and control the car accordingly.
            if not data:
                break
            # --------Motor calibration----------
            if data == 'motor_run':
                print('motor moving forward')
                motor.setSpeed(50)
                motor.motor0(forward0)
                motor.motor1(forward1)
            elif data[0:9] == 'leftmotor':
                forward0 = data[9:]
                motor.motor0(forward0)
            elif data[0:10] == 'rightmotor':
                forward1 = data[10:]
                motor.motor1(forward1)

            # -------------Added--------------
            elif data == 'leftreverse':
                if forward0 == "True":
                    forward0 = "False"
                else:
                    forward0 = "True"
                print("left motor reversed to", forward0)
                motor.motor0(forward0)
            elif data == 'rightreverse':
                if forward1 == "True":
                    forward1 = "False"
                else:
                    forward1 = "True"
                print("right motor reversed to", forward1)
                motor.motor1(forward1)
            elif data == 'motor_stop':
                print('motor stop')
                motor.stop()
            # ---------------------------------

            # -------Turing calibration------
            elif data[0:7] == 'offset=':
                offset = int(data[7:])
                car_dir.calibrate(offset)
            # --------------------------------

            # ----------Mount calibration---------
            elif data[0:8] == 'offsetx=':
                offset_x = int(data[8:])
                print('Mount offset x', offset_x)
                video_dir.calibrate(offset_x, offset_y)
            elif data[0:8] == 'offsety=':
                offset_y = int(data[8:])
                print('Mount offset y', offset_y)
                video_dir.calibrate(offset_x, offset_y)
            # ----------------------------------------

            # -------Turing calibration 2------
            elif data[0:7] == 'offset+':
                offset = offset + int(data[7:])
                print('Turning offset', offset)
                car_dir.calibrate(offset)
            elif data[0:7] == 'offset-':
                offset = offset - int(data[7:])
                print('Turning offset', offset)
                car_dir.calibrate(offset)
            # --------------------------------

            # ----------Mount calibration 2---------
            elif data[0:8] == 'offsetx+':
                offset_x = offset_x + int(data[8:])
                print('Mount offset x', offset_x)
                video_dir.calibrate(offset_x, offset_y)
            elif data[0:8] == 'offsetx-':
                offset_x = offset_x - int(data[8:])
                print('Mount offset x', offset_x)
                video_dir.calibrate(offset_x, offset_y)
            elif data[0:8] == 'offsety+':
                offset_y = offset_y + int(data[8:])
                print('Mount offset y', offset_y)
                video_dir.calibrate(offset_x, offset_y)
            elif data[0:8] == 'offsety-':
                offset_y = offset_y - int(data[8:])
                print('Mount offset y', offset_y)
                video_dir.calibrate(offset_x, offset_y)
            # ----------------------------------------

            # ----------Confirm--------------------
            elif data == 'confirm':
                config = 'offset_x = %s\noffset_y = %s\noffset = %s\nforward0 = %s\nforward1 = %s\n ' % (
                    offset_x, offset_y, offset, forward0, forward1)
                print('')
                print('*********************************')
                print(' You are setting config file to:')
                print('*********************************')
                print(config)
                print('*********************************')
                print('')
                fd = open('config', 'w')
                fd.write(config)
                fd.close()

                motor.stop()
                tcpSerSock.close()
                quit()
            else:
                print('Command Error! Cannot recognize command: ' + data)


if __name__ == "__main__":
    try:
        setup()
        loop()
    except KeyboardInterrupt:
        tcpSerSock.close()
