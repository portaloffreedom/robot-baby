from time import sleep
from uuid import uuid4

from mating.logging import l
from mating.message import PersonalMessage, GenomeMessage, MESSAGE_INTERVAL_SEC
from mating.robot.client import TCPClient, UDPClientThread
from mating.robot.server import UDPServerThread


AVAILABLE = 1


class Robot(object):
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

    def server_response(self, data):
        if data:
            return PersonalMessage(self.hash, '')

    def client_message(self):
        return PersonalMessage(self.hash, '')


class EvolutionaryRobot(Robot):

    def __init__(self, name):
        Robot.__init__(self, name)
        self.genome_file = '{}.genome'.format(name)
        self.mate_hash = None
        self.availability = True

    def initialize_parameters(self):
        self.server.criterion = self.server_criterion
        self.server.response = self.server_response
        self.client.message = self.client_message

    def server_criterion(self, data):
        return data['hash_code'] != self.hash

    def server_response(self, data):
        message = None
        if data['message'] == AVAILABLE:
            if not self.mate_hash:
                message = data['hash_code']
        if data['message'] == self.hash:
            if (self.mate_hash
                    and data['hash_code'] == self.mate_hash
                    and self.availability):
                self.agree_to_mate()
                self.availability = False
            else:
                self.mate_hash = data['hash_code']
            message = data['hash_code']
        return PersonalMessage(self.hash, message)

    def client_message(self):
        sleep(MESSAGE_INTERVAL_SEC)
        message = None
        if not self.mate_hash:
            l('SENT: {}, mating call'.format(self.hash))
            message = AVAILABLE
        else:
            l('SENT: {}, {}'.format(self.hash, self.mate_hash))
            message = self.mate_hash
        return PersonalMessage(self.hash, message)

    def agree_to_mate(self):
        """ Once the robots agree to mate, send their genomes to the mating
            server.
        """
        cli = TCPClient(message=GenomeMessage(
            sorted([self.hash, self.mate_hash]), self.genome_file
        ))
        l('{} sending genome to the mating server'.format(self.hash))
        cli.send()  # TODO: Add fallback to connection errors/failures
