import socket  

import threading
import time

# Define a function for the thread

thread_list = []

def start_thread():
	ip_ = 1
	while ip_ < 254:
		ip_ = ip_ + 1
		IP = "172.16.5.%d" % ip_
		# Create two threads as follows
		try:
			t = threading.Thread(target=discover, args=(IP,))
			# Sticks the thread in a list so that it remains accessible
			thread_list.append(t)
		except Exception as e:
			template = "An exception of type {0} occured. Arguments:{1!r}"
			mesg = template.format(type(e).__name__, e.args)
			print mesg

	for thread in thread_list:
		thread.start()

	for thread in thread_list:
		thread.join()

	print "Done"


def discover(IP):
	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	sock.settimeout(3.0)
	host = socket.gethostname() # Get local machine name
	port = 12345                # Reserve a port for your service.

	server_address = ('IP', 12345)

	try:
		sock.connect(server_address)
	except:
		print " Error to discovering"


if __name__ == "__main__":
	start_thread()