import bluetooth
import time
from funcs import *

while True:
	print "Discovery started."
	target_name = None
	target_address = None

	peersArray = []
	index = -1

	nearby_devices = bluetooth.discover_devices()

	for bdaddr in nearby_devices:
		index += 1
		print bdaddr, bluetooth.lookup_name( bdaddr )
		peersArray.append([bdaddr, str(bluetooth.lookup_name( bdaddr )), 0])
		if(peersArray[index][1] == "parrot"):
			print "Check: " + bdaddr
			send_packet(bdaddr, 2, "What is the music of life?")
			isopen = listen_packets(3)
			if isopen:
				peersArray[index][2] = 1
	   
	peers = open("peers.txt", "w")

	for peer in peersArray:
		if peer[2]:
			peers.write(peer[0] + ", " + peer[1] + "\n")

	peers.close()
	print "Sleeping..."
	time.sleep(30)