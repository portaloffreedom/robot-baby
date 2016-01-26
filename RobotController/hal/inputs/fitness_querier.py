import socket
import struct
import logging

class FitnessQuerier:

    def __init__(self, config_values):
        self._server_address = config_values['fitness_service_addr']
        self._server_port = config_values['fitness_service_port']
        self._query_type = config_values['fitness_type']
        self._fitness_weights = config_values['fitness_weights']
        self._id = config_values['robot_id']
        self._ipaddr = ''

    def start(self):
        try:
            s = self._create_socket()
            resp = self._send_message(s, 'start')
            s.close()
        except (socket.error, socket.gaierror):
            resp = -1

        return resp

    def get_fitness(self):
        fitness = {}
        for method, weight in zip(self._query_type, self._fitness_weights):
            try:
                s = self._create_socket()
                fitness[method] = weight * self._send_message(s, 'fitness', method)[0]
                s.close()
            except (socket.error, socket.gaierror):
                pass
        return sum([fitness[m] for m in self._query_type])

    def get_position(self):
        try:
            s = self._create_socket()
            position = self._send_message(s, 'position')
            s.close()
        except (socket.error, socket.gaierror):
            return ()

        return position

    def _create_socket(self):
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        except socket.error as err:
            logging.error("Failed to create socket: {0}".format(err))
            raise

        try:
            self._ipaddr = socket.gethostbyname(self._server_address)
            s.connect((self._ipaddr, self._server_port))
        except socket.gaierror:
            logging.error("Cannot connect to host: {}".format(self._server_address))
            raise
        return s

    def _send_message(self, sock, query_type, method=''):
        if query_type == 'start':
            qt = 1
            message = struct.pack('!ll', qt, self._id)
        elif query_type == 'fitness':
            if method == '':
                raise ValueError("Fitness evaluation method not specified")
            qt = 2
            if method == 'displacement':
                met = 1
            elif method == 'path':
                met = 2
            else:
                raise NameError("Unknown fitness evaluation method: {}".format(method))
            message = struct.pack('!lll', qt, self._id, met)
        elif query_type == 'position':
            qt = 3
            message = struct.pack('!ll', qt, self._id)
        else:
            raise NameError("Unknown query type: {}".format(query_type))

        try:
            sock.sendall(message)
        except socket.error:
            logging.error("Couldn't send query")

        if query_type == 'fitness':
            response = sock.recv(4)
            error = sock.recv(4)
            return struct.unpack('!f', response), struct.unpack('!l', error)
        elif query_type == 'start':
            error = sock.recv(4)
            return struct.unpack('!l', error)
        elif query_type == 'position':
            response1 = sock.recv(4)
            response2 = sock.recv(4)
            error = sock.recv(4)
            return struct.unpack('!f', response1), struct.unpack('!f', response2), struct.unpack('!l', error)
