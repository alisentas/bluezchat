from funcs import send_packet, listen_packets
import sys
import sqlite

bdaddr  = sys.argv[1]
lookup_name = sys.argv[2]

res = send_packet(bdaddr, 2, "What is the music of life?")
if res:
    isopen = listen_packets(3)
    if isopen:
        conn = sqlite.connect("peers.db")
        c = conn.cursor()
        c.execute("INSERT INTO peers VALUES (%s, %s)", bdaddr, lookup_name)
else:
    print "Couldn't connect"