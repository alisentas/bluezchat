import bluetooth

bd_addr = "38:59:F9:F5:48:EB"

port = 1

sock=bluetooth.BluetoothSocket( bluetooth.RFCOMM )
sock.connect((bd_addr, port))

sock.send("hello ali lai ali lali ali!!")

sock.close()
