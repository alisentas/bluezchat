import bluetooth

bd_addr = "3C:15:C2:D4:E4:D3"

port = 1

sock=bluetooth.BluetoothSocket( bluetooth.RFCOMM )
sock.connect((bd_addr, port))

sock.send("hello ali lai ali lali ali!!")

sock.close()