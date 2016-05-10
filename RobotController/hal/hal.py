from smbus import SMBus
from hal.outputs.servo import Servo
from hal.outputs.StatusLED import StatusLED
from hal.photocell import PCF8591P as photocell
import logging

__author__ = 'matteo'


class Hal:
    def __init__(self, config_options):
        self.led = StatusLED(config_options)
        self.sensor = photocell(SMBus(1), 0x48)
        self.sensor.enableDAC()
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
