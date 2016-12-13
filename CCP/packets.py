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
    "connection_init":0,

    "move_forward":0,
    "move_left":1,

    "alert_stop":0,
    "alert_warning":1

}


def get_message(message):
    return pickle.loads(message)

def create_message(**kargs):
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