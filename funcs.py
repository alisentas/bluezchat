import bluetooth
import sys, os

def send_packet(bdaddr, port, message):
	sock=bluetooth.BluetoothSocket( bluetooth.RFCOMM )

	try:
		sock.connect((bdaddr, port))
		sock.settimeout(3)
		sock.send(message)
	except:
		print "Something happened while connecting", bdaddr
		sock.close()
		return False
	
	print "Sent[%s] to %s" % (message, bdaddr)
	sock.close()
	return True

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
			return send_packet(address[0], 3, "Silence by brother")
	except KeyboardInterrupt:
		try:
			sys.exit(0)
		except SystemExit:
			os._exit(0)
	finally:
		client_sock.close()
		server_sock.close()
		print "Something happened while listening, probably timeout"
		return False

	client_sock.close()
	server_sock.close()
	return True

def sendall(port, message):
	closests = [line.rstrip('\n') for line in open("closest.txt", "r")]
	peers = [peer.split(",") for peer in closests]
	for peer in peers:
		send_packet(peer[0], 2, message)