import json
from socket import (socket, AF_INET, SOCK_DGRAM, SOL_SOCKET, SO_REUSEADDR,
                    SO_REUSEPORT)
from threading import Thread

from mating.message import Message
from mating.network import DEFAULT_PACKET_SIZE, UDP_PORT


class UDPServerThread(Thread):
    """ Receives data from the Wi-Fi, by convention encoded as JSON strings,
        and decides whether or not to respond.
    """
    def __init__(self, criterion=None, response=None):
        """ Should override criterion and response functions in offsping. """
        Thread.__init__(self)
        self.s = socket(AF_INET, SOCK_DGRAM)
        self.address = ('', UDP_PORT)
        self.s.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
        self.s.setsockopt(SOL_SOCKET, SO_REUSEPORT, 1)
        self.s.bind(self.address)
        # If criterion has not been set, use the default one
        self.criterion = criterion or default_criterion
        # If response has not been set, use the default one
        self.response = response or default_response

    def run(self):
        # Listen to the network
        while True:
            packet, addr = self.s.recvfrom(DEFAULT_PACKET_SIZE)
            # If packet received satisfies criteria
            rcv_data = json.loads(packet)
            if self.criterion(data=rcv_data):
                rsp_data = self.response(data=rcv_data)
                # Respond
                self.s.sendto(json.dumps(rsp_data.__dict__), self.address)


def default_response(**kwargs):
    """ Returns an empty message. """
    return Message()


def default_criterion(**kwargs):
    """ Always returns true. """
    return True
