import bluetooth

def send_packet(bdaddr, port, message):
	sock=bluetooth.BluetoothSocket( bluetooth.RFCOMM )

	try:
		sock.connect((bdaddr, port))
		sock.settimeout(3)
		sock.send(message)
	except:
		print "Something happened while connecting"
		sock.close()
		return
	
	print "Sent[%s]" % message
	sock.close()

def listen_packets(port, answer = False):
	server_sock=bluetooth.BluetoothSocket( bluetooth.RFCOMM )
	client_sock=bluetooth.BluetoothSocket( bluetooth.RFCOMM )
	
	try:
		server_sock.bind(("",port))
		server_sock.settimeout(3)
		server_sock.listen(1)


		client_sock,address = server_sock.accept()
		print "Accepted connection from ",address

		data = client_sock.recv(1024)
		print "received [%s]" % data

		if answer:
			send_packet(address[0], 3, "Silence by brother")
			return True
	except:
		client_sock.close()
		server_sock.close()
		print "Something happened while listening, probably timeout"

	client_sock.close()
	server_sock.close()