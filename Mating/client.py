import json
from message import Message
from network import UDP_IP, UDP_PORT
from socket import socket, AF_INET, SOCK_DGRAM, SOL_SOCKET, SO_REUSEADDR
from threading import Thread


class Client(Thread):
    """ Receives data from the Wi-Fi, by convention encoded as JSON strings,
        and decides whether or not to respond.
    """
    def __init__(self, criterion=None, response=None):
        """ Should override criterion and response functions in offsping. """
        Thread.__init__(self)
        self.s = socket(AF_INET, SOCK_DGRAM)
        self.s.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
        self.s.bind((UDP_IP, UDP_PORT))
        # If criterion has not been set, use the default one
        self.crt = criterion or should_respond
        # If response has not been set, use the default one
        self.rsp = response or default_response

    def run(self):
        while True:
            packet, addr = self.s.recvfrom(1024)
            if self.crt(json.loads(packet)):
                data = self.rsp()
                self.s.sendto(json.dumps(data.__dict__), (UDP_IP, UDP_PORT))


def default_response():
    """ Returns an empty message. """
    return Message()


def should_respond(data):
    """ Always returns true. """
    return True
