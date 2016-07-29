#!/usr/bin/python           # This is server.py file

import socket               # Import socket module

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host = '172.16.5.116' # Get local machine name
port = 12345                # Reserve a port for your service.
s.bind((host, port))        # Bind to the port

s.listen(5)                 # Now wait for client connection.
while True:
   c, addr = s.accept()     # Establish connection with client.
   print 'Got connection from', addr,host
   a = c.recv(1024)
   print "Message", a
   c.close()                # Close the connection
