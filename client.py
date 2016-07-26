import bluetooth

def function send_packet(bdaddr, port, message):
	sock=bluetooth.BluetoothSocket( bluetooth.RFCOMM )
	sock.connect((bdaddr, port))

	sock.send(message)

	sock.close()
