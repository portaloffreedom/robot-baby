import zmq
import sys

# ZeroMQ Context
context = zmq.Context()

# Define the socket using the "Context"
sock = context.socket(zmq.REQ)
sock.connect("tcp://127.0.0.1:37373")

# Send a "message" using the socket
sock.send(" ".join(sys.argv[1:]))
print sock.recv()