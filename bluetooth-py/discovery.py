import bluetooth
import time

while True:
	print "Discovery started."
	target_name = None
	target_address = None

	peers = open("peers.txt", "w")

	nearby_devices = bluetooth.discover_devices()

	for bdaddr in nearby_devices:
	    print bdaddr, bluetooth.lookup_name( bdaddr )
	    peers.write(bdaddr + "," + bluetooth.lookup_name( bdaddr ) + "\n")

	peers.close()
	print "Sleeping..."
	time.sleep(30)