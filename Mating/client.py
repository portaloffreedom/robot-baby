import json
from message import Message
from network import UDP_IP, UDP_PORT
from socket import socket, AF_INET, SOCK_DGRAM, SOL_SOCKET, SO_REUSEADDR
from threading import Thread


class Client(Thread):

    def __init__(self, criterion=None, response=None):
        Thread.__init__(self)
        self.s = socket(AF_INET, SOCK_DGRAM)
        self.s.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
        self.s.bind((UDP_IP, UDP_PORT))
        self.crt = criterion or should_respond
        self.rsp = response or default_response

    def run(self, cond='True'):
        while eval(cond):
            packet, addr = self.s.recvfrom(1024)
            if self.crt(json.loads(packet)):
                data = self.rsp()
                self.s.sendto(json.dumps(data.__dict__), (UDP_IP, UDP_PORT))


def default_response():
    return Message()


def should_respond(data):
    return True
