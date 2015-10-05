from client import Client
from message import Message
from random import uniform
from server import Server


class Robot():
    """ Abstract class that implements a basic robot. Should be overriden. """
    def __init__(self, name=None):
        self.server = Server()  # Initialize a server
        self.client = Client()  # Initialize a client
        self.initialize_parameters()  # Custom function definitions go here
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

    # mate_probability defaults to 1, we may change this in the future
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
        """ Once the robots agree to mate, send their genomes to the mating
            server.
        """
        pass
