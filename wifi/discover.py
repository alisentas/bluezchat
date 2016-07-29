#!/usr/bin/python 


import socket  

import threading
import time

# Define a function for the thread

thread_list = []

def start_thread():
	ip_ = 1
	while ip_ < 254:
		ip_ = ip_ + 1
		IP = "172.16.5.%d", ip_;
		# Create two threads as follows
		try:
			t = threading.Thread(discover,IP)
			# Sticks the thread in a list so that it remains accessible
			thread_list.append(t)
		except:
			print "Error: unable to start thread"

	for thread in thread_list:
		thread.start()

	for thread in thread_list:
		thread.join()

	print "Done"


def discover(IP):
	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	socket.settimeout(5.0)
	host = socket.gethostname() # Get local machine name
	port = 12345                # Reserve a port for your service.

	server_address = ('IP', 12345)

	try:
		sock.connect(server_address)
	except:
		print " Error to discovering"


