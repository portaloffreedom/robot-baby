#!/bin/python3

import logging
import sys
import signal

from robot_brain import RobotBrain

__author__ = 'matteo'

LOG_FORMAT = "%(asctime)-15s:%(levelname)-8s:%(threadName)s:%(filename)s:%(funcName)s: %(message)s"
LOG_LEVEL = logging.DEBUG


def interrupt_handler(signum, frame):
    logging.info("changing evaluation")
    controller.stop_current_evaluation()


if __name__ == "__main__":
    logging.basicConfig(level=LOG_LEVEL, format=LOG_FORMAT, stream=sys.stdout)
    logging.info("starting application")

    # catch signal to interrupt current evaluation and call stop_current_evaluation
    signal.signal(signal.SIGINT, interrupt_handler)

    controller = RobotBrain("robot_1.cfg")
    controller.live()

    logging.info("ending application")
