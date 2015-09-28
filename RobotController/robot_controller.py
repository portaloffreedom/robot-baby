from locomotion.fake_controller import FakeController
from movement.rlpower_algorithm import RLPowerAlgorithm
import time
import logging

__author__ = 'matteo'


class RobotController:
    """Class for controlling the whole life of the robot.
    Here you can find the main loop function, called live
    """

    TIME_CHECK_TIMEOUT = 30  # in seconds

    def __init__(self, controllers_file_path):
        # TODO load controllers from file
        self.controller = FakeController()
        self.algorithm = RLPowerAlgorithm()

        self._next_check = time.time() + RobotController.TIME_CHECK_TIMEOUT

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
        self.controller.step()

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
            self._next_check = current_check + RobotController.TIME_CHECK_TIMEOUT

    def stop_current_evaluation(self):
        """
        Stop the current evaluation, mark it as bad and starts a new one

        intended to do an emergency stop for a bad controller that could "kill" the robot
        """
        self.controller.off()
        # TODO discard current evaluation
        self._check_next_evaluation(force=True)
