connection = ["connection_init",
              ]

driving = ["move_forward",
           "move_left",
           ]

alert = ["alert_stop",
         "alert_warning",
         ]

message_type = {
    "alert": alert,
    "driving": driving,
    "connection": connection
}

print(message_type)
