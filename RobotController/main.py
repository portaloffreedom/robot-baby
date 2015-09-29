#!/bin/python2

import logging
import sys

from robot_brain import RobotBrain

LOG_FORMAT = "%(asctime)-15s:%(levelname)-8s:%(threadName)s:%(filename)s:%(funcName)s: %(message)s"
LOG_LEVEL = logging.DEBUG

__author__ = 'matteo'

if __name__ == "__main__":
    logging.basicConfig(level=LOG_LEVEL, format=LOG_FORMAT, stream=sys.stdout)
    logging.info("starting application")

    # TODO catch signal to interrupt current evaluation and call stop_current_evaluation

    controller = RobotBrain("robot_1.cfg")
    controller.live()

    logging.info("ending application")
