categories:
"driving":0
"alert":1

order:
init_connection:0
forward:0
stop:0
left:1
warning:1

args:
ex: [speed:5, angle:56]


call("driving","forward",5)

def get_move_forward(cat="driving", ):
    return {"categorie":"driving","order":'0',"args":[]}


