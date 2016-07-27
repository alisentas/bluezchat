import time
from funcs import *
import subprocess

def send_discovery(bdaddr, lookup_name):

	print "Check: " + bdaddr + " - " + lookup_name

	res = send_packet(bdaddr, 2, "What is the music of life?")
	if res:
		isopen = listen_packets(3, 3)
		if isopen:
			peers = open("peers.txt", "a")
			peers.write("%s,%s\n" % (bdaddr, lookup_name))
			peers.close()

	else:
		print "Couldn't connect"

while True:
	print "Discovery started."
	target_name = None
	target_address = None

	peersArray = []
	index = -1

	processes = []

	nearby_devices = bluetooth.discover_devices(8, True, True)

	print nearby_devices

	peers = open("peers.txt", "w")
	peers.close()

	for device in nearby_devices:
		peersArray.append([device[0], str(device[1]), 0])
		send_discovery(device[0], device[1])

	print "Sleeping..."
	time.sleep(5)
