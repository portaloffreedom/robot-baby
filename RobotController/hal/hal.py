from hal.outputs.servo import Servo

__author__ = 'matteo'


class Hal:
    def __init__(self, controller_config):
        # TODO load it from file "controller_config"
        self._servos = []
        self._n_servo = 8
        for i in range(self._n_servo):
            self._servos.append(Servo(i))

    def step(self):
        # TODO
        pass

    def off(self):
        for servo in self._servos:
            servo.off()
        pass
