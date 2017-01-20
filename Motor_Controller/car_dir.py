import Motor_Controller.PCA9685 as servo
import time  # Import necessary modules
import os

def Map(x, in_min, in_max, out_min, out_max):
    return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min


def setup():
    global leftPWM, rightPWM, homePWM, pwm
    ROOT_DIR = os.path.dirname(os.path.abspath(__file__))

    leftPWM = 400
    homePWM = 450
    rightPWM = 500
    offset = 0
    try:
        for line in open(ROOT_DIR + '/config'):
            s = line.split("=")
            s0 = s[0].strip()
            s1 = s[1].strip()

            if s0 == 'offset':
                offset = int(s1)
    except Exception as e:
        print('config error')
        print(e)
    leftPWM += offset
    homePWM += offset
    rightPWM += offset
    pwm = servo.PWM()  # Initialize the servo controller.
    pwm.set_frequency(60)


# ==========================================================================================
# Control the servo connected to channel 0 of the servo control board, so as to make the
# car turn left.
# ==========================================================================================
def turn_left():
    global leftPWM
    pwm.set_value(0, 0, leftPWM)  # CH0


# ==========================================================================================
# Make the car turn right.
# ==========================================================================================
def turn_right():
    global rightPWM
    pwm.set_value(0, 0, rightPWM)


# ==========================================================================================
# Control the servo connected to channel 0 of the servo control board, so as to make the
# car turn left.
# ==========================================================================================
def fine_turn_left():
    global leftPWM
    pwm.set_value(0, 0, 450 - 1)


# ==========================================================================================
# Make the car turn right.
# ==========================================================================================
def fine_turn_right():
    pwm.set_value(0, 0, 450 + 1)


# ==========================================================================================
# Make the car turn back.
# ==========================================================================================

def turn(angle):
    angle = Map(angle, 0, 255, leftPWM, rightPWM)
    pwm.set_value(0, 0, angle)


def home():
    global homePWM
    pwm.set_value(0, 0, homePWM)


def calibrate(x):
    pwm.set_value(0, 0, 450 + x)


def test():
    while True:
        turn_left()
        time.sleep(1)
        home()
        time.sleep(1)
        turn_right()
        time.sleep(1)
        home()


if __name__ == '__main__':
    setup()
    home()
