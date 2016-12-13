import socket
import os
import gevent


class Controller:
    def __init__(self,queue_ccp_receive,queue_ccp_send,queue_images,queue_motor):
        self.queue_ccp_receive = queue_ccp_receive
        self.queue_ccp_send = queue_ccp_send

        self.queue_images = queue_images
        self.queue_motor =  queue_motor

        gevent.joinall([
            gevent.spawn(self.manager_ccp()),
            gevent.spawn(self.manager_images())
        ])

    def controller(self):
        pass


    def manager_images(self):
        while True:
            data=self.queue_images.get()
            if interprete_image(data) == obstacle:
                self.queue_motor.put(stop)
                self.queue_ccp_send.put(obstacle)

    def manager_ccp_receive(self):
        while True:
            data = self.queue_ccp_receive.get()

            if data == motor
                self.queue_motor.put(data)


    def manager_ccp_send(self):
        while True:
            data = self.queue_ccp_send.get()

            if data == (image: obstacle):
            self.queue_motor.put(stop)
            self.queue_ccp_send.put(stop)
