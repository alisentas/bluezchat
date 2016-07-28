import os, sys, time, gtk, gobject, gtk.glade, bluetooth

class Chat:
	def __init__(self):
		self.peers = {}
		self.sources = {}
		self.addresses = {}
		self.server_sock = None

	def scan(self):
		print "Discovery started"

		nearby_devices = bluetooth.discover_devices(8, True, True)

		for device in nearby_devices:
			print device
			addr = device[0]
			lookup_name = device[1]
			sock = bluetooth.BluetoothSocket(bluetooth.L2CAP)
			try:
				sock.settimeout(5)
				sock.connect((addr, 0x1001))
				sock.send("What is the music of life?")
			except Exception as exception:
				template = "An exception of type {0} occured. Arguments:{1!r}"
				mesg = template.format(type(exception).__name__, exception.args)
				print mesg, lookup_name
				sock.close()
				continue

	def data_ready(self, sock, condition):
		address = self.addresses[sock]
		data = sock.recv(1024)

		if len(data) == 0:
			print "No msg"
			#gobject.source_remove(self.sources[address])
			#del self.sources[address]
			#del self.peers[address]
			#del self.addresses[sock]
			#sock.close()
		else:
			print("\n%s - %s" % (address, str(data)))
		return True

	def incoming_connection(self, source, condition):
		sock, info = self.server_sock.accept()
		address, psm = info

		print address

		# add new connection to list of peers
		self.peers[address] = sock
		self.addresses[sock] = address

		source = gobject.io_add_watch (sock, gobject.IO_IN, self.data_ready)
		self.sources[address] = source
		return True

	def start_server(self):
		print "Server started"
		self.server_sock = bluetooth.BluetoothSocket (bluetooth.L2CAP)
		self.server_sock.bind(("",0x1001))
		self.server_sock.listen(1)
		gobject.io_add_watch(self.server_sock, gobject.IO_IN, self.incoming_connection)

	def run(self):
		print "Running"
		self.start_server()
		gtk.main()


if __name__ == "__main__":
	chat = Chat()
	chat.run()