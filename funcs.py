import bluetooth
import sys, os

def send_packet(bdaddr, port, message):
	sock=bluetooth.BluetoothSocket( bluetooth.RFCOMM )

	try:
		sock.settimeout(5)
		sock.connect((bdaddr, port))
		sock.send(message)
	except Exception as exception:
		template = "An exception of type {0} occured. Arguments:{1!r}"
		mesg = template.format(type(exception).__name__, exception.args)
		print mesg
		sock.close()
		return False
	
	print "Sent[%s] to %s" % (message, bdaddr)
	sock.close()
	return True

def listen_packets(port, timeout, answer = False, transmit = False):
	server_sock=bluetooth.BluetoothSocket( bluetooth.RFCOMM )
	client_sock=bluetooth.BluetoothSocket( bluetooth.RFCOMM )
	
	try:
		server_sock.bind(("",port))
		server_sock.setsockopt(1,2,1);
		if timeout > 0:
			server_sock.settimeout(timeout)
		server_sock.listen(1)


		client_sock,address = server_sock.accept()
		print "Accepted connection from ",address

		data = client_sock.recv(1024)
		print "received [%s]" % data

		if answer:
			return send_packet(address[0], 3, "Silence my brother")
		if transmit:
			return False

	except KeyboardInterrupt:
		try:
			sys.exit(0)
		except SystemExit:
			os._exit(0)
	except Exception as exception:
		client_sock.close()
		server_sock.close()
		template = "An exception of type {0} occured. Arguments:{1!r}"
		mesg = template.format(type(exception).__name__, exception.args)
		print mesg
		return False

	client_sock.close()
	server_sock.close()
	return True

def sendall(port, message):
	closests = [line.rstrip('\n') for line in open("closest.txt", "r")]
	peers = [peer.split(",") for peer in closests]
	for peer in peers:
		send_packet(peer[0], 2, message)