import bluetooth
import time

while True:
	print "Discovery started."
	target_name = None
	target_address = None

	peersArray = []

	nearby_devices = bluetooth.discover_devices()

	for bdaddr in nearby_devices:
	    print bdaddr, bluetooth.lookup_name( bdaddr )
	    peersArray.append([bdaddr, str(bluetooth.lookup_name( bdaddr ))])
	   
	peers = open("peers.txt", "w")

	for peer in peersArray:
		peers.write(peer[0] + ", " + peer[1] + "\n")

	peers.close()
	print "Sleeping..."
	time.sleep(30)