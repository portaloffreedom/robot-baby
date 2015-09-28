from Locomotion.servo import Servo

__author__ = 'matteo'


class RobotController:
    """Class for controlling the whole life of the robot.
    Here you can find the main loop function
    """

    def __init__(self, controllers_file_path):
        # TODO load controllers from file
        # now there are just fake controllers:
        self._controllers = []
        self._controller_size = 8
        for i in range(self._controller_size):
            self._controllers = Servo(i)

    def live(self):
        pass
