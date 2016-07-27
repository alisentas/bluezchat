from funcs import send_packet
import sys

bdaddr  = sys.argv[1]
port    = sys.argv[2]
message = sys.argv[3]

print bdaddr, port, "message", message, "troll";