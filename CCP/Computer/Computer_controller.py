import logging

from CCP import packets, connection_manager
from tkinter import *
from socket import *


class Computer_controller:
    def __init__(self):
        self.ui = Tk()
        self.sock = None

        self.start_server()

    def send(self, driving_order, args=None):
        message = packets.create_message("driving", driving_order, args)
        logging.debug('Computer sends:' + str(message))

        if message is not None:
            connection_manager.to_send(self.sock, message)


    def start_server(self):
        # Create the socket to connect to the car
        sock = socket(AF_INET, SOCK_STREAM)
        sock.bind(('', 3000))
        sock.listen(5)

        while True:
            logging.info("Waiting for new car...")
            self.sock, address = sock.accept()

            logging.info("Car {} connected".format(address))
            # We start the UI when the car is connected
            self.start_ui()
            logging.info("UI exited")

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
        self.Btn0.bind('<ButtonPress-1>', self.forward_fun)  # When button0 is pressed down, call the function forward_fun().
        self.Btn1.bind('<ButtonPress-1>', self.backward_fun)
        self.Btn2.bind('<ButtonPress-1>', self.left_fun)
        self.Btn3.bind('<ButtonPress-1>', self.right_fun)

        self.Btn0.bind('<ButtonRelease-1>', self.stop_fun)  # When button0 is released, call the function stop_fun().
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

        self.ui.bind('<KeyPress-q>', self.left_fun)
        self.ui.bind('<KeyPress-d>', self.right_fun)
        self.ui.bind('<KeyPress-s>', self.backward_fun)
        self.ui.bind('<KeyPress-z>', self.forward_fun)
        self.ui.bind('<KeyPress-h>', self.home_fun)

        self.ui.bind('<KeyRelease-z>', self.stop_fun)
        self.ui.bind('<KeyRelease-s>', self.stop_fun)
        self.ui.bind('<KeyRelease-q>', self.home_fun)
        self.ui.bind('<KeyRelease-d>', self.home_fun)

    def forward_fun(self, event):
        logging.info('forward')
        self.send("move_forward")

    def backward_fun(self, event):
        logging.info('backward')
        self.send("move_backward")

    def left_fun(self, event):
        logging.info('left')
        self.send("turn_left")
        #self.send("home")

    def right_fun(self, event):
        logging.info('right')
        self.send("turn_right")
        #self.send("home")

    def stop_fun(self, event):
        logging.info('stop')
        self.send("stop")

    def home_fun(self, event):
        logging.info('home')
        self.send("home")

    def x_increase(self, event):
        logging.info('x+')
        self.send("x+")

    def x_decrease(self, event):
        logging.info('x-')
        self.send("x-")

    def y_increase(self, event):
        logging.info('y+')
        self.send("y+")

    def y_decrease(self, event):
        logging.info('y-')
        self.send("y-")

    def xy_home(self, event):
        logging.info('xy_home')
        self.send("xy_home")

    # =============================================================================
    # Exit the GUI program and close the network connection between the client
    # and server.
    # =============================================================================
    def quit_fun(self, event):
        self.send('stop')
        self.sock.close()
        self.ui.quit()
        sys.exit(0)

    def changeSpeed(self, ev=None):
        self.spd = self.speed.get()
        logging.debug('set_speed: ' + str(self.spd))
        self.send("set_speed", self.spd)  # Send the speed data to the server(Raspberry Pi)
