import json
from message import Message
from network import UDP_IP, UDP_PORT
from socket import socket, AF_INET, SOCK_DGRAM, SOL_SOCKET
from threading import Thread


class Client(Thread):
    """ Broadcasts data to the Wi-Fi, by convention encoded as JSON strings.
    """
    def __init__(self, message=None):
        """ Should override message function in offsping. """
        Thread.__init__(self)
        self.s = socket(AF_INET, SOCK_DGRAM)
        self.address = ('localhost', UDP_PORT)
        self.message = message or default_message

    def run(self):
        while True:
            data = self.message()
            self.s.sendto(json.dumps(data.__dict__), self.address)


def default_message():
    """ Returns an empty message. """
    return Message()
