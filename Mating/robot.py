from client import Client
from message import Message
from server import Server
from time import sleep


class Robot():

    def __init__(self, name=None):
        self.server = Server(service=self.server_data)
        self.client = Client(criterion=self.client_criterion,
                             response=self.client_data)
        self.name = name
        self.server.daemon = True
        self.client.daemon = True
        self.server.start()
        self.client.start()

    def server_data(self):
        return Message(hash(self), '')

    def client_criterion(self, data):
        return data['hash_code'] != hash(self)

    def client_data(self):
        return Message(hash(self), '')
