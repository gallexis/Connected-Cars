try:
    import cPickle as pickle
except:
    import pickle

message_type={
    "alert": 0,
    "driving": 1,
    "connection": 2
}

message_order={
    # ALERT
    "connection_init":0,

    # DRIVING
    "move_forward":0,
    "move_left":1,

    #CONNECTION
    "alert_stop":0,
    "alert_warning":1
}

"""
    message_type is used to encode a message
    reversed_message_type i used to decode a message

    i.e:
        print(message_type["alert"])     == 0
        print(reversed_message_type[0])  == "alert"
"""
reversed_message_type = {v: k for k, v in message_type.items()}
reversed_message_order = {v: k for k, v in message_order.items()}


def get_message(message):
    loaded_message = pickle.loads(pickle.dumps(message))

    # loaded_message["message_type"] = reversed_message_type[loaded_message["message_type"]]
    # loaded_message["message_order"] = reversed_message_order[loaded_message["message_order"]]
    print(loaded_message)

    return bytearray(loaded_message)


def create_message(**kargs):
    assert (len(kargs) >= 2)

    type =   kargs["message_type"]
    order=   kargs["message_order"]
    args=    kargs["args"]

    return pickle.dumps(
        {
            "message_type": message_type[type],
            "message_order": message_order[order],
            "args": args
        }
    )