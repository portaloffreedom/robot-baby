#!/bin/python3

import logging
import sys
import signal

from robot_brain import RobotBrain

__author__ = 'matteo'

LOG_FORMAT = "%(asctime)-15s:%(levelname)-8s:%(threadName)s:%(filename)s:%(funcName)s: %(message)s"
LOG_LEVEL = logging.DEBUG

INTERRUPT_MESSAGE = "input 'q' if you want to exit, just enter (or any other character) to continue:"


def noop_interrupt_handler(signum, frame):
    print("\n" + INTERRUPT_MESSAGE)


def interrupt_handler(signum, frame):
    signal.signal(signal.SIGINT, noop_interrupt_handler)
    logging.info("changing evaluation")
    controller.stop_current_evaluation()
    command = input(INTERRUPT_MESSAGE + "\n")
    if command == 'q':
        controller.suicide()
        #sys.exit(0)
    signal.signal(signal.SIGINT, interrupt_handler)


if __name__ == "__main__":
    logging.basicConfig(level=LOG_LEVEL, format=LOG_FORMAT, stream=sys.stdout)
    logging.info("starting application")

    # catch signal to interrupt current evaluation and call stop_current_evaluation
    signal.signal(signal.SIGINT, interrupt_handler)

    controller = RobotBrain("robot_1.cfg")
    controller.live()

    logging.info("ending application")
