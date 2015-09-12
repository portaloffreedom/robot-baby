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
        self.server.start()
        self.client.start()

    def server_data(self):
        sleep(1)
        print '{}: Hello!'.format(self.name)
        return Message(hash(self), 'Hello!')

    def client_criterion(self, data):
        return data['hash_code'] != hash(self)

    def client_data(self):
        print '{}: Hello to you as well, sir!'.format(self.name)
        return Message(hash(self), 'Hello to you as well, sir!')
