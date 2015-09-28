#!/bin/python2

import logging
import sys

from robot_controller import RobotController

LOG_FORMAT = "%(asctime)-15s:%(levelname)-8s:%(threadName)s:%(filename)s:%(funcName)s: %(message)s"
LOG_LEVEL = logging.DEBUG

__author__ = 'matteo'

if __name__ == "__main__":
    logging.basicConfig(level=LOG_LEVEL, format=LOG_FORMAT, stream=sys.stdout)
    logging.info("starting application")

    controller = RobotController("robot_1.cfg")
    controller.live()

    logging.info("ending application")
