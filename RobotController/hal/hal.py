from hal.outputs.servo import Servo
import logging

__author__ = 'matteo'


class Hal:
    def __init__(self, config_options):
        self._servos = []
        self._n_servo = len(config_options['servo_pins'])
        for x in config_options['servo_pins']:
            logging.info("creating servo {}".format(x))
            self._servos.append(Servo(x))
            pass

    def step(self, outputs):
        for index, servo in enumerate(self._servos):
            servo.move_to_position(outputs[index])

    def off(self):
        for servo in self._servos:
            servo.off()
        pass
