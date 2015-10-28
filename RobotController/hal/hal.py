from hal.outputs.servo import Servo

__author__ = 'matteo'


class Hal:
    def __init__(self, config_options):
        self._servos = []
        self._n_servo = len(config_options['servo_pins'])
        for i in range(self._n_servo):
            #self._servos.append(Servo(i))
            pass

    def step(self):
        # TODO
        pass

    def off(self):
        for servo in self._servos:
            servo.off()
        pass
