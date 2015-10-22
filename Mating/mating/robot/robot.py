from client import TCPClient, UDPClientThread
from message import PersonalMessage, GenomeMessage
from random import uniform
from server import UDPServerThread


MATING_MESSAGE = 'MATE'

MATING_AGREE_RESPONSE = 'YES'
MATING_DISAGREE_RESPONSE = 'NO'


class Robot():
    """ Abstract class that implements a basic robot. Should be overriden. """
    def __init__(self, name=None):
        self.server = UDPServerThread()  # Initialize a server
        self.client = UDPClientThread()  # Initialize a client
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
        self.genome_file = '{}.genome'.format(name)
        self.availability = True  # Availability to mate
        self.mate_probability = mate_probability

    def initialize_parameters(self):
        self.server.criterion = self.server_criterion
        self.server.response = self.server_response
        self.client.message = self.client_message

    def server_criterion(self, data):
        if self.availability and data['hash_code'] != hash(self):
            if data['message'] == MATING_MESSAGE:
                return uniform(0, 1) < self.mate_probability
            elif data['message'] == MATING_AGREE_RESPONSE:
                return hasattr(self, 'mate_hash')\
                    and data['hash_code'] == self.mate_hash

        return False

    def server_response(self, data):
        if data['message'] == MATING_MESSAGE:
            self.mate_hash = data['hash_code']
            return PersonalMessage(hash(self), MATING_AGREE_RESPONSE)
        elif data['message'] == MATING_AGREE_RESPONSE:
            self.availability = False
            self.agree_to_mate()
            return PersonalMessage(hash(self), MATING_AGREE_RESPONSE)

        return PersonalMessage(hash(self), MATING_DISAGREE_RESPONSE)

    def client_message(self):
        return PersonalMessage(hash(self), MATING_MESSAGE)

    def agree_to_mate(self):
        """ Once the robots agree to mate, send their genomes to the mating
            server.
        """
        cli = TCPClient(message=GenomeMessage(
            sorted([hash(self), self.mate_hash]), self.genome_file
        ))
        cli.send()  # TODO: Add fallback to connection errors/failures
