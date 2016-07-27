import bluetooth
import time
from funcs import *
from subprocess import call
from os import system

while True:
	print "Discovery started."
	target_name = None
	target_address = None

	peersArray = []
	index = -1

	nearby_devices = bluetooth.discover_devices(8, True, True)

	print nearby_devices

	for device in nearby_devices:
		peersArray.append([device[0], str(device[1]), 0])
		print "Check: " + device[0] + " - " + device[1]
		#call(["python send_discovery.py", device[0]])
		system("python send_discovery.py %s \"%s\" &" % (device[0], device[1]))
	   
	peers = open("peers.txt", "w")

	for peer in peersArray:
		if peer[2]:
			peers.write(peer[0] + "," + peer[1] + "\n")

	peers.close()
	print "Sleeping..."
	time.sleep(20)