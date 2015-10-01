import json
from message import Message
from network import UDP_IP, UDP_PORT
from socket import socket, AF_INET, SOCK_DGRAM
from threading import Thread


class Server(Thread):
    """ Broadcasts data to the Wi-Fi, by convention encoded as JSON strings.
    """
    def __init__(self, service=None):
        Thread.__init__(self)
        self.s = socket(AF_INET, SOCK_DGRAM)
        self.srv = service or default_service

    def run(self):
        while True:
            data = self.srv()
            self.s.sendto(json.dumps(data.__dict__), (UDP_IP, UDP_PORT))


def default_service():
    """ Returns an empty message. """
    return Message()
