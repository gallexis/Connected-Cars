import socket
import os

print("yooo")

if os.path.exists( "/tmp/connected-cars.sock" ):
    server = socket.socket( socket.AF_UNIX, socket.SOCK_STREAM )
    server.connect("/tmp/connected-cars.sock" )
    print("connected")
else:
    print("not connected")