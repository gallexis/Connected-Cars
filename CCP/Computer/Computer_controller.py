import gevent
from tkinter import *
from socket import *

# =============================================================================
# The function is to send the command forward to the server, so as to make the
# car move forward.
# =============================================================================

# ctrl_cmd = ['forward', 'backward', 'left', 'right', 'stop', 'read cpu_temp', 'home', 'distance', 'x+', 'x-', 'y+', 'y-', 'xy_home']
"""
ctrl_cmd = {
    '0':  motor.ctrl(0), #Stop
    '1':  motor.forward(),
    '2':  motor.backward(),
    '3':  car_dir.turn_left(),
    '4':  car_dir.turn_right(),
    '5':  lambda args: forward_speed(args),
    '6':  lambda args: backward_speed(args),
    '7':  lambda args: setAngle(args),
    '8':  video_dir.move_increase_x(),# X+
    '9':  video_dir.move_decrease_x(), # X-
    '10': video_dir.move_increase_y(), # Y+
    '11': video_dir.move_decrease_y(), # Y-
    '12': video_dir.home_x_y(),# home X_Y
    '13': lambda args: setSpeed(args),
    '14': car_dir.home(),
    '15': lambda : set_cpu_value()
}
"""


class Computer_controller:
    def __init__(self):
        self.ui = Tk()
        self.sock = None

        gevent.joinall([
            gevent.spawn(self.start_server()),
        ])

    def start_server(self):
        # Create the socket to connect to the car
        self.sock = socket(AF_INET, SOCK_STREAM)
        self.sock.bind(('', 15555))
        self.sock.listen(5)

        while True:
            print("waiting for car...")
            car_sock, address = self.sock.accept()

            print("car {} connected".format(address))
            # We start the UI when the car is connected
            self.start_ui()

    def start_ui(self):
        self.spd = 50

        self.label = Label(self.ui, text='Speed:', fg='red')  # Create a label
        self.label.grid(row=6, column=0)  # Label layout

        self.speed = Scale(self.ui, from_=0, to=100, orient=HORIZONTAL, command=self.changeSpeed)  # Create a scale
        self.speed.set(50)
        self.speed.grid(row=6, column=1)

        self.init_buttons()
        self.set_layout_buttons()
        self.bind_buttons()

        self.ui.mainloop()

    # =============================================================================
    # Create buttons
    # =============================================================================
    def init_buttons(self):
        self.Btn0 = Button(self.ui, width=5, text='Forward')
        self.Btn1 = Button(self.ui, width=5, text='Backward')
        self.Btn2 = Button(self.ui, width=5, text='Left')
        self.Btn3 = Button(self.ui, width=5, text='Right')
        self.Btn4 = Button(self.ui, width=5, text='Quit')
        self.Btn5 = Button(self.ui, width=5, height=2, text='Home')

        self.Btn07 = Button(self.ui, width=5, text='X+', bg='red')
        self.Btn08 = Button(self.ui, width=5, text='X-', bg='red')
        self.Btn09 = Button(self.ui, width=5, text='Y-', bg='red')
        self.Btn10 = Button(self.ui, width=5, text='Y+', bg='red')
        self.Btn11 = Button(self.ui, width=5, height=2, text='HOME', bg='red')

    # =============================================================================
    # Buttons layout
    # =============================================================================
    def set_layout_buttons(self):
        self.Btn0.grid(row=0, column=1)
        self.Btn1.grid(row=2, column=1)
        self.Btn2.grid(row=1, column=0)
        self.Btn3.grid(row=1, column=2)
        self.Btn4.grid(row=3, column=2)
        self.Btn5.grid(row=1, column=1)

        self.Btn07.grid(row=1, column=5)
        self.Btn08.grid(row=1, column=3)
        self.Btn09.grid(row=2, column=4)
        self.Btn10.grid(row=0, column=4)
        self.Btn11.grid(row=1, column=4)

    # =============================================================================
    # Bind the buttons with the corresponding callback function.
    # =============================================================================
    def bind_buttons(self):
        self.Btn0.bind('<ButtonPress-1>',
                       self.forward_fun)  # When button0 is pressed down, call the function forward_fun().
        self.Btn1.bind('<ButtonPress-1>', self.backward_fun)
        self.Btn2.bind('<ButtonPress-1>', self.left_fun)
        self.Btn3.bind('<ButtonPress-1>', self.right_fun)
        self.Btn0.bind('<ButtonRelease-1>',
                       self.stop_fun)  # When button0 is released, call the function stop_fun().
        self.Btn1.bind('<ButtonRelease-1>', self.stop_fun)
        self.Btn2.bind('<ButtonRelease-1>', self.stop_fun)
        self.Btn3.bind('<ButtonRelease-1>', self.stop_fun)
        self.Btn4.bind('<ButtonRelease-1>', self.quit_fun)
        self.Btn5.bind('<ButtonRelease-1>', self.home_fun)

        self.Btn07.bind('<ButtonPress-1>', self.x_increase)
        self.Btn08.bind('<ButtonPress-1>', self.x_decrease)
        self.Btn09.bind('<ButtonPress-1>', self.y_decrease)
        self.Btn10.bind('<ButtonPress-1>', self.y_increase)
        self.Btn11.bind('<ButtonPress-1>', self.xy_home)
        # Btn07.bind('<ButtonRelease-1>', home_fun)
        # Btn08.bind('<ButtonRelease-1>', home_fun)
        # Btn09.bind('<ButtonRelease-1>', home_fun)
        # Btn10.bind('<ButtonRelease-1>', home_fun)
        # Btn11.bind('<ButtonRelease-1>', home_fun)

        self.ui.bind('<KeyPress-a>',
                     self.left_fun)  # Press down key 'A' on the keyboard and the car will turn left.
        self.ui.bind('<KeyPress-d>', self.right_fun)
        self.ui.bind('<KeyPress-s>', self.backward_fun)
        self.ui.bind('<KeyPress-w>', self.forward_fun)
        self.ui.bind('<KeyPress-h>', self.home_fun)
        self.ui.bind('<KeyRelease-a>', self.home_fun)  # Release key 'A' and the car will turn back.
        self.ui.bind('<KeyRelease-d>', self.home_fun)
        self.ui.bind('<KeyRelease-s>', self.stop_fun)
        self.ui.bind('<KeyRelease-w>', self.stop_fun)

    def forward_fun(self, event):
        print('forward')
        self.sock.send('1')

    def backward_fun(self, event):
        print('backward')
        self.sock.send('2')

    def left_fun(self, event):
        print('left')
        self.sock.send('3')

    def right_fun(self, event):
        print('right')
        self.sock.send('4')

    def stop_fun(self, event):
        print('stop')
        self.sock.send('0')

    def home_fun(self, event):
        print('home')
        self.sock.send('14')

    def x_increase(self, event):
        print('x+')
        self.sock.send('8')

    def x_decrease(self, event):
        print('x-')
        self.sock.send('9')

    def y_increase(self, event):
        print('y+')
        self.sock.send('10')

    def y_decrease(self, event):
        print('y-')
        self.sock.send('11')

    def xy_home(self, event):
        print('xy_home')
        self.sock.send('12')

    # =============================================================================
    # Exit the GUI program and close the network connection between the client
    # and server.
    # =============================================================================
    def quit_fun(self, event):
        self.ui.quit()
        self.sock.send('stop')
        self.sock.close()

    def changeSpeed(self, ev=None):
        self.spd = self.speed.get()
        data = 'speed ' + str(self.spd)  # Change the integers into strings and combine them with the string 'speed'.
        print('sendData = %s' % data)
        self.sock.send(data)  # Send the speed data to the server(Raspberry Pi)
