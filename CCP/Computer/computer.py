import socket
import gevent

def handle_car(car_sock, address):
    global number_of_cars,cars

    while True:
        response = car_sock.recv(255)

        if response == "" or response == "exit":
            car_sock.close()
            break

        if b"init" == response:
            print("new car")

        print(response)


def server(sendingQueue):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(('', 15555))
    s.listen(5)

    while True:
        car_sock, address = s.accept()
        print("{} connected".format(address))
        gevent.spawn(handle_car,car_sock, address)



    #s.close()
