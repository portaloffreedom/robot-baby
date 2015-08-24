__author__ = 'bweel'

import socket
import sys

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

server_address = ('', 373737)

sock.bind(server_address)

while True:
    data, address = sock.recvfrom(4096)

    print >> sys.stderr, 'received %s bytes from %s' % (len(data), address)
    print >> sys.stderr, data

    if data == "ipcheck":
        reply = "ip:" + address[0]
        sock.sendto(reply,address)