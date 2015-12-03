from random import uniform
from time import sleep
from uuid import uuid4

from mating.logging import l
from mating.message import PersonalMessage, GenomeMessage, MESSAGE_INTERVAL_SEC
from mating.robot.client import TCPClient, UDPClientThread
from mating.robot.server import UDPServerThread


MATING_MESSAGE = 'MATE'

MATING_AGREE_RESPONSE = 'YES'
MATING_DISAGREE_RESPONSE = 'NO'


class Robot():
    """ Abstract class that implements a basic robot. Should be subclassed. """

    def __init__(self, name=None):
        self.server = UDPServerThread()  # Initialize a server
        self.client = UDPClientThread()  # Initialize a client
        self.initialize_parameters()  # Custom function definitions go here
        self.name = name
        self.hash = str(uuid4())
        self.server.daemon = True
        self.client.daemon = True
        self.server.start()
        self.client.start()

    def initialize_parameters(self):
        self.server.criterion = self.server_criterion
        self.server.response = self.server_response
        self.client.message = self.client_message

    def server_criterion(self, data):
        return data['hash_code'] != self.hash

    def server_response(self):
        return PersonalMessage(self.hash, '')

    def client_message(self):
        return PersonalMessage(self.hash, '')


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
        sleep(MESSAGE_INTERVAL_SEC)
        if self.availability and data['hash_code'] != self.hash:
            if data['message'] == MATING_MESSAGE:
                l('{} received a mating message from {}'
                  .format(self.hash, data['hash_code']))
                return uniform(0, 1) < self.mate_probability
            elif data['message'] == MATING_AGREE_RESPONSE:
                l('{} agreed to mate with {}'.format(self.hash,
                                                     data['hash_code']))
                return hasattr(self, 'mate_hash')\
                    and data['hash_code'] == self.mate_hash

        return False

    def server_response(self, data):
        sleep(MESSAGE_INTERVAL_SEC)
        if data['message'] == MATING_MESSAGE:
            self.mate_hash = data['hash_code']
            l('Registered {} as potential mate'.format(self.mate_hash))
            return PersonalMessage(self.hash, MATING_AGREE_RESPONSE)
        elif data['message'] == MATING_AGREE_RESPONSE:
            self.availability = False
            l('Agreed to mate with {}'.format(self.mate_hash))
            self.agree_to_mate()
            return PersonalMessage(self.hash, MATING_AGREE_RESPONSE)

        return PersonalMessage(self.hash, MATING_DISAGREE_RESPONSE)

    def client_message(self):
        sleep(MESSAGE_INTERVAL_SEC)
        l('{} sending mating message'.format(self.hash))
        return PersonalMessage(self.hash, MATING_MESSAGE)

    def agree_to_mate(self):
        """ Once the robots agree to mate, send their genomes to the mating
            server.
        """
        cli = TCPClient(message=GenomeMessage(
            sorted([self.hash, self.mate_hash]), self.genome_file
        ))
        l('{} sending genome to the mating server'.format(self.hash))
        cli.send()  # TODO: Add fallback to connection errors/failures
