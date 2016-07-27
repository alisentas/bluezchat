import time
from funcs import *
import subprocess

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
		processes.append(subprocess.Popen(["python", "send_discovery.py", device[0], device[1]]))

	for process in processes:
		print "waiting"
		process.wait()

	print "Sleeping..."
	time.sleep(5)