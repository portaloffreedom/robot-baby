from client import Client
from message import Message
from random import uniform
from server import Server


class Robot():

    def __init__(self, name=None):
        self.server = Server()
        self.client = Client()
        self.initialize_parameters()
        self.name = name
        self.server.daemon = True
        self.client.daemon = True
        self.server.start()
        self.client.start()

    def initialize_parameters(self):
        self.server.service = self.server_data
        self.client.criterion = self.client_criterion
        self.client.response = self.client_data

    def server_data(self):
        return Message(hash(self), '')

    def client_criterion(self, data):
        return data['hash_code'] != hash(self)

    def client_data(self):
        return Message(hash(self), '')


class EvolutionaryRobot(Robot):

    def __init__(self, name, mate_probability=1):
        Robot.__init__(self, name)
        self.mate_probability = mate_probability

    def initialize_parameters(self):
        self.server.service = self.server_data
        self.client.criterion = self.client_criterion
        self.client.response = self.client_data

    def server_data(self):
        return Message(hash(self), 'Mate?')

    def client_criterion(self, data):
        return data['hash_code'] != hash(self)\
            and data['message'] == 'Mate?'\
            and uniform(0, 1) < self.mate_probability

    def client_data(self):
        return Message(hash(self), 'Sure!')

    def agree_to_mate(self):
        pass  # TODO
