import socket

def parse_server_message(message):
    if b"forward" == message:
        return "forward"
    elif b"exit" == message:
        return "exit"
    else:
        return None


def send_to_slave(queue):
    hote = "localhost"
    port = 15555

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((hote, port))
    print("Connection on {}".format(port))

    sock.send(b"init")

    while True:
        response = sock.recv(255)

        parsed_message = parse_server_message(response)

        if not parsed_message == None:
            queue.put(parsed_message)
        elif parsed_message == "exit":
            break

    sock.close()


def send_to_master(queue):
    hote = "localhost"
    port = 15555

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((hote, port))
    print("Connection on {}".format(port))

    sock.send(b"init")

    while True:
        response = sock.recv(255)

        parsed_message = parse_server_message(response)

        if not parsed_message == None:
            queue.put(parsed_message)
        elif parsed_message == "exit":
            break

    sock.close()


def receive_from_slave(queue):
    hote = "localhost"
    port = 15555

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((hote, port))
    print("Connection on {}".format(port))

    sock.send(b"init")

    while True:
        response = sock.recv(255)

        parsed_message = parse_server_message(response)

        if not parsed_message == None:
            queue.put(parsed_message)
        elif parsed_message == "exit":
            break

    sock.close()


def receive_from_master(queue):
    hote = "localhost"
    port = 15555

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((hote, port))
    print("Connection on {}".format(port))

    sock.send(b"init")

    while True:
        response = sock.recv(255)

        parsed_message = parse_server_message(response)

        if not parsed_message == None:
            queue.put(parsed_message)
        elif parsed_message == "exit":
            break

    sock.close()