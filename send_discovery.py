from funcs import send_packet, listen_packets
import sys

bdaddr  = sys.argv[1]
lookup_name = sys.argv[2]

print "Check: " + bdaddr + " - " + lookup_name

res = send_packet(bdaddr, 2, "What is the music of life?")
if res:
    isopen = listen_packets(3, 3)
    if isopen:
        peers = open("peers.txt", "a")
        peers.write("%s,%s\n" % (bdaddr, lookup_name))
        peers.close()
        
else:
    print "Couldn't connect"
