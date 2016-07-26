import bluetooth
import time
from funcs import *

while True:
	print "Discovery started."
	target_name = None
	target_address = None

	peersArray = []
	index = -1

	nearby_devices = bluetooth.discover_devices(8, False, True)

	print nearby_devices

	for device in nearby_devices:
		peersArray.append([device[0], str(device[1]), 0])
		print "Check: " + device[0] + " - " + device[1]
		res = send_packet(device[0], 2, "What is the music of life?")
		print "Res:[%s]" % res
		if res:
			isopen = listen_packets(3)
			if isopen:
				peersArray[index][2] = 1
		else:
			print "Couldn't connect"
	   
	peers = open("peers.txt", "w")

	for peer in peersArray:
		if peer[2]:
			peers.write(peer[0] + ", " + peer[1] + "\n")

	peers.close()
	print "Sleeping..."
	time.sleep(5)