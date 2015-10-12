from client import Client
from message import PersonalMessage
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
        self.server.criterion = self.server_criterion
        self.server.response = self.server_response
        self.client.message = self.client_message

    def server_criterion(self, data):
        return data['hash_code'] != hash(self)

    def server_response(self):
        return PersonalMessage(hash(self), '')

    def client_message(self):
        return PersonalMessage(hash(self), '')


class EvolutionaryRobot(Robot):

    # mate_probability defaults to 1, we may change this in the future
    def __init__(self, name, mate_probability=1):
        Robot.__init__(self, name)
        self.mate_probability = mate_probability

    def initialize_parameters(self):
        self.server.criterion = self.server_criterion
        self.server.response = self.server_response
        self.client.message = self.client_message

    def server_criterion(self, data):
        return data['hash_code'] != hash(self)\
            and data['message'] == 'Mate?'\
            and uniform(0, 1) < self.mate_probability

    def server_response(self):
        return PersonalMessage(hash(self), 'Sure!')

    def client_message(self):
        return PersonalMessage(hash(self), 'Mate?')

    def agree_to_mate(self):
        """ Once the robots agree to mate, send their genomes to the mating
            server.
        """
        pass  # TODO: Implement
