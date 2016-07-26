import bluetooth

def send_packet(bdaddr, port, message):
	sock=bluetooth.BluetoothSocket( bluetooth.RFCOMM )
	sock.connect((bdaddr, port))

	sock.send(message)

	print "Sent[%s]" % message
	sock.close()

def listen_packets(port, answer = False):
	server_sock=bluetooth.BluetoothSocket( bluetooth.RFCOMM )
	server_sock.bind(("",port))
	server_sock.listen(1)

	client_sock,address = server_sock.accept()
	print "Accepted connection from ",address

	data = client_sock.recv(1024)
	print "received [%s]" % data

	if answer:
		send_packet(address[0], 3, "Silence by brother")
		return True

	client_sock.close()
	server_sock.close()