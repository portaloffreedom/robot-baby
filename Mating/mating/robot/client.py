import json
from socket import (socket, AF_INET, SOCK_DGRAM, SOL_SOCKET, SO_REUSEADDR,
                    SO_BROADCAST, SO_REUSEPORT, SOCK_STREAM)
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
        self.s.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
        self.s.setsockopt(SOL_SOCKET, SO_REUSEPORT, 1)
        self.s.setsockopt(SOL_SOCKET, SO_BROADCAST, 1)
        self.message = message or default_message

    def run(self):
        while True:
            data = self.message()
            if data:
                self.s.sendto(json.dumps(data.__dict__).encode(), self.address)


class TCPClient(Thread):
    def __init__(self, message=None):
        """ Should override message function in offsping. """
        Thread.__init__(self)
        self.s = socket(AF_INET, SOCK_STREAM)
        self.address = (TCP_IP, TCP_PORT)
        self.message = message or default_message

    def send(self):
        self.s.connect(self.address)
        data = self.message
        if data:
            self.s.send(json.dumps(data.__dict__).encode())
        self.s.close()


def default_message():
    """ Returns an empty message. """
    return Message()
