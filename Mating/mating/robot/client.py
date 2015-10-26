import json
from socket import socket, AF_INET, SOCK_DGRAM, SOCK_STREAM
from threading import Thread

from mating.message import Message
from mating.network import UDP_IP, UDP_PORT, TCP_IP, TCP_PORT


class UDPClientThread(Thread):
    """ Broadcasts data to the Wi-Fi, by convention encoded as JSON strings.
    """
    def __init__(self, message=None):
        """ Should override message function in offsping. """
        Thread.__init__(self)
        self.s = socket(AF_INET, SOCK_DGRAM)
        self.address = (UDP_IP, UDP_PORT)
        self.message = message or default_message

    def run(self):
        while True:
            data = self.message()
            self.s.sendto(json.dumps(data.__dict__), self.address)


class TCPClient():
    def __init__(self, message=None):
        """ Should override message function in offsping. """
        Thread.__init__(self)
        self.s = socket(AF_INET, SOCK_STREAM)
        self.address = (TCP_IP, TCP_PORT)
        self.message = message or default_message

    def send(self):
        self.s.connect(self.address)
        data = self.message()
        self.s.send(json.dumps(data.__dict__))
        self.s.close()


def default_message():
    """ Returns an empty message. """
    return Message()
