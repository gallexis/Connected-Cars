try:
    import cPickle as pickle
except:
    import pickle

connection = ["connection_init",
              ]

driving = ['stop',
           'move_forward',
           'move_forward',
           'turn_left',
           'turn_right',
           'forward_speed',
           'backward_speed',
           'set_angle',
           'x+',
           'x-',
           'y+',
           'y-',
           'xy_home',
           'set_speed',
           'home',
           'get_cpu_value',
           ]

alert = ["alert_stop",
         "alert_warning",
         ]

message_type={
    "alert": alert,
    "driving": driving,
    "connection": connection
}


def get_message(binary_data):
    loaded_message = pickle.loads(binary_data)
    keys = list(message_type.keys())

    if "message_type" in keys and "message_order" in keys and "args" in keys:
        return loaded_message
    else:
        return None


def create_message(type, order, args):
    try:
        if type in list(message_type.keys()) and order in message_type[type]:
            return pickle.dumps(
                {
                    "message_type": type,
                    "message_order": order,
                    "args": args
                }
            )
        else:
            raise ("Type is not in message_type, or order is not in message_type's array")

    except Exception as e:
        print(e)
        return None
