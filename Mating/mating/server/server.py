import json
import os
import uuid
from socket import socket, AF_INET, SOCK_STREAM

from mating.logging import l
from mating.network import DEFAULT_PACKET_SIZE, TCP_IP, TCP_PORT


MATING_CMD = ('./RobotCrossover parent/{}.txt parent/{}.txt '
              'confs/evolConf-full.txt -{}.genome.txt')


def run_mating_server():
    def handle_received_data(packet, mates):
        dhash = str(packet['hash_code'])
        l('Mating server received {}'.format(dhash))
        if mates.get(dhash):
            mates[dhash].append(packet['message'])
        else:
            mates[dhash] = [packet['message']]

    s = socket(AF_INET, SOCK_STREAM)
    s.bind((TCP_IP, TCP_PORT))
    s.listen(1)

    # Initialize an empty dictionary - mating pairs will be stored here
    mates = {}
    while True:
        conn, addr = s.accept()
        packet = conn.recv(DEFAULT_PACKET_SIZE)
        if packet:
            handle_received_data(json.loads(packet.decode()), mates)
        for pair_id in mates:
            # If both robots have agreed to mate
            if len(mates[pair_id]) == 2:
                l('Mating server formed a pair {}'.format(mates[pair_id]))
                command = MATING_CMD.format(mates[pair_id][0],
                                            mates[pair_id][1],
                                            str(uuid.uuid4()))
                l('Running command {}'.format(command))
                # Call the Cpp module that does the crossover
                os.system(command)
        conn.close()
