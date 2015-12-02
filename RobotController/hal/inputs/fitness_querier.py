import socket
import struct
import logging

class FitnessQuerier:

    def __init__(self, config_values):
        self._server_address = config_values['fitness_service_addr']
        self._server_port = config_values['fitness_service_port']
        self._query_type = config_values['fitness_type']
        self._id = config_values['robot_id']
        self._ipaddr = ''

    def start(self):
        # Create a TCP socket
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        except socket.error as err:
            logging.error("Failed to create socket: {0}".format(err))
            return

        # Connect to fitness service
        try:
            self._ipaddr = socket.gethostbyname(self._server_address)
            s.connect((self._ipaddr, self._server_port))
            self._send_message(s, 'start')
        except socket.gaierror:
            logging.error("Cannot connect to host: {}".format(self._server_address))

        s.close()

    def get_fitness(self):
        # Create a TCP socket
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        except socket.error as err:
            logging.error("Failed to create socket: {0}".format(err))
            return []

        fitness = {}
        # Connect to fitness service
        try:
            self._ipaddr = socket.gethostbyname(self._server_address)
            s.connect((self._ipaddr, self._server_port))
            for method in self._query_type:
                fitness['method'] = self._send_message(s, 'fitness', method)
        except socket.gaierror:
            logging.error("Cannot connect to host: {}".format(self._server_address))

        s.close()
        return [fitness[m] for m in self._query_type]

    def get_position(self):
        # Create a TCP socket
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        except socket.error as err:
            logging.error("Failed to create socket: {0}".format(err))
            return ()

        # Connect to fitness service
        try:
            self._ipaddr = socket.gethostbyname(self._server_address)
            s.connect((self._ipaddr, self._server_port))
            position = self._send_message(s, 'position')
        except socket.gaierror:
            logging.error("Cannot connect to host: {}".format(self._server_address))

        s.close()
        return position

    def _send_message(self, sock, query_type, method=''):
        message = bytearray()
        if query_type == 'start':
            message.append(1)
        elif query_type == 'fitness':
            if method == '':
                raise ValueError("Fitness evaluation method not specified")
            message.append(2)
        elif query_type == 'position':
            message.append(3)
        else:
            raise NameError("Unknown query type: {}".format(query_type))

        message.append(self._id)

        if query_type == 'fitness' and method != '':
            if method == 'displacement':
                message.append(1)
            elif method == 'distance':
                message.append(2)
            else:
                raise NameError("Unknown fitness evaluation method: {}".format(method))

        try:
            sock.sendall(message)
        except socket.error:
            logging.error("Couldn't send query")

        response = sock.recv(1024)

        if query_type == 'fitness':
            return struct.unpack('!f', response)
        elif query_type == 'position':
            return struct.unpack('!ff', response)
