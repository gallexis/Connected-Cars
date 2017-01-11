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

reversed_message_type = {v: k for k, v in message_type.items()}
reversed_message_order = {v: k for k, v in message_order.items()}

print(message_type["alert"])
print(reversed_message_type[0])

print(message_type["alert"])
print(reversed_message_type[0])