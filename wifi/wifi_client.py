#!/usr/bin/python           # This is client.py file

import socket               # Import socket module

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host = socket.gethostname() # Get local machine name
port = 12345                # Reserve a port for your service.

server_address = ('172.16.5.105', 12345)

sock.connect(server_address)
sock.send("Merhaba")
sock.close()                     # Close the socket when done
