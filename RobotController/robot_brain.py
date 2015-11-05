# from hal.fake_hal import FakeHal
from hal.hal import Hal
from learning.rlpower_algorithm import RLPowerAlgorithm
import time
import json
import logging
from hal.outputs.servo import Servo

__author__ = 'matteo'


class RobotBrain:
    """Class for controlling the whole life of the robot.
    Here you can find the main loop function, called live
    """

    TIME_CHECK_TIMEOUT = 30  # in seconds

    def __init__(self, config_file_path):
        try:
            with open(config_file_path) as config_file:
                config_options = json.load(config_file)
        except IOError:
            logging.error("Configuration file could not be read: {}".format(config_file_path))
            raise SystemExit

        self.servos = []
        for x in config_options['servo_pins']:
            logging.info("creating servo {}".format(x))
            self.servos.append(Servo(x))

#        config_options = []
        self.HAL = Hal(config_options)
        self.algorithm = RLPowerAlgorithm(config_options)

        self._next_check = time.time() + RobotBrain.TIME_CHECK_TIMEOUT
        self._start_time = time.time()

    def live(self):
        """
        life big cycle
        """
        while True:
            self.life_step()

    def life_step(self):
        """
        A life step, composed of several operations
        """
        self.HAL.step()
        _input = (time.time() - self._start_time) / 4
        _outputs = self.algorithm.controller.get_value(_input)
#        logging.info("output: {}".format(_outputs))

        for index, servo in enumerate(self.servos):
            servo.move_to_position(_outputs[index])

        # if 30 seconds passed from last check:
        self._check_next_evaluation()

    def _check_next_evaluation(self, force=False):
        """
        Check if is a moment for a new evaluation and starts a new one
        :param force: forces the new evaluation to start
        """
        current_check = time.time()
        if force or current_check > self._next_check:
            logging.info("next movement values current {}, next {}".format(current_check, self._next_check))
            self.algorithm.next_evaluation(self)
            self._next_check = current_check + RobotBrain.TIME_CHECK_TIMEOUT

    def stop_current_evaluation(self):
        """
        Stop the current evaluation, mark it as bad and starts a new one

        intended to do an emergency stop for a bad controller that could "kill" the robot
        """
        self.HAL.off()
        # TODO discard current evaluation
        self._check_next_evaluation(force=True)
