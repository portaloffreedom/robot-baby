import json
from socket import socket, AF_INET, SOCK_STREAM

from mating.network import DEFAULT_PACKET_SIZE, TCP_IP, TCP_PORT


def run_mating_server():
    def handle_received_data(packet, mates):
        for data in packet:
            dhash = str(data['hash_code'])
            if mates[dhash]:
                mates[dhash].append(data['message'])
            else:
                mates[dhash] = [data['message']]

    s = socket(AF_INET, SOCK_STREAM)
    s.bind((TCP_IP, TCP_PORT))
    s.listen(1)

    conn, addr = s.accept()
    # Initialize an empty dictionary - mating pairs will be stored here
    mates = {}
    while True:
        packet = conn.recv(DEFAULT_PACKET_SIZE)
        handle_received_data(json.loads(packet), mates)
        for pair_id in mates:
            # If both robots have agreed to mate
            if len(mates[pair_id]) == 2:
                print mates[pair_id]
                pass  # TODO: Call the Cpp module that does the crossover

    conn.close()
