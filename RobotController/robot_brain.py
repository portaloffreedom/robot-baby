# from hal.fake_hal import FakeHal
from hal.hal import Hal
from learning.rlpower_algorithm import RLPowerAlgorithm
from mating.robot.robot import EvolutionaryRobot
import time
import json
import logging

__author__ = 'matteo'

MATE_STEPS_THRESHOLD = 10

class RobotBrain:
    """Class for controlling the whole life of the robot.
    Here you can find the main loop function, called live
    """

    def __init__(self, config_file_path):
        try:
            with open(config_file_path) as config_file:
                config_options = json.load(config_file)
        except IOError:
            logging.error("Configuration file could not be read: {}"
                          .format(config_file_path))
            raise SystemExit

        self.HAL = Hal(config_options)
        self.algorithm = RLPowerAlgorithm(config_options)
        self.HAL.led.setColor(self.HAL.led._green)

        self.robot_name = config_options['robot_name']
        self.TIME_CHECK_TIMEOUT = config_options['evaluation_time']
        self.LIGHT_THRESHOLD = config_options['light_mating_threshold']
        self._offline = config_options['disable_learning']

        self._next_check = time.time() + self.TIME_CHECK_TIMEOUT
        self._start_time = time.time()

        self.mating_client = None
        self._stop = False

        self.evaluations_after_mating = 0

    def live(self):
        """
        life big cycle
        """
        while not self._stop:
            self.life_step()
        self._die()

    def life_step(self):
        """
        A life step, composed of several operations
        """
        _input = (time.time() - self._start_time) / 4
        _outputs = self.algorithm.controller.get_value(_input)
        self.HAL.step(_outputs)
#        logging.info("output: {}".format(_outputs))

        # check if new evaluation is needed and if so, change it
        if not self._offline:
            self._check_next_evaluation()

        # check mating conditions
        self._check_mating_conditions()

    def _check_next_evaluation(self, force=False):
        """
        Check if is a moment for a new evaluation and starts a new one
        :param force: forces the new evaluation to start
        """

        current_check = time.time()
        if force or current_check > self._next_check:
            self.HAL.led.setColor(self.HAL.led._magenta)
            logging.info("Next movement values current {}, next {}"
                         .format(current_check, self._next_check))
            if force:
                self.algorithm.skip_evaluation()
            else:
                # TODO make HAL smarter in light readings
                self.algorithm.next_evaluation(
                    1 + (self.HAL.sensor.readADC(0) / -255))  # 255-0 to 0-1
            self._next_check = current_check + self.TIME_CHECK_TIMEOUT

    def _check_mating_conditions(self):
        if self.mating_client and self.mating_client.availability:
            self.mating_client.server.join()
            self.mating_client.client.join()
            self.mating_client = None

        light_level = 1 + (self.HAL.sensor.readADC(0) / -255)
        if light_level < self.LIGHT_THRESHOLD:
            self.HAL.led.setColor(self.HAL.led._green)
        else:
            self.HAL.led.setColor(self.HAL.led._red)
            if not self.mating_client and\
                    self.evaluations_after_mating < MATE_STEPS_THRESHOLD:
                self.evaluations_after_mating = 0
                self.mating_client = EvolutionaryRobot(self.robot_name)
            else:
                self.evaluations_after_mating += 1

    def stop_current_evaluation(self):
        """
        Stop the current evaluation, mark it as bad and starts a new one

        intended to do an emergency stop for a bad controller that could "kill" the robot
        """
        # self.HAL.off()
        self._check_next_evaluation(force=True)

    def _die(self):
        self.HAL.off()

    def suicide(self):
        self._stop = True
