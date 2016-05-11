#!/usr/bin/python
import logging
import RPi.GPIO as GPIO

# Needed for main() test harnesses
import json

# Common Cathode RGB-LEDs (Cathode=Active Low)
RGB_ENABLE = 0
RGB_DISABLE = 1

# LED CONFIG - Set GPIO Ports
RGB_RED = 15
RGB_GREEN = 14
RGB_BLUE = 4
RGB_CYAN = [RGB_GREEN, RGB_BLUE]
RGB_MAGENTA = [RGB_RED, RGB_BLUE]
RGB_YELLOW = [RGB_RED, RGB_GREEN]
RGB_WHITE = [RGB_RED, RGB_GREEN, RGB_BLUE]


class RGBLED:
    """
    Class for controlling RGB LED indicator using discrete signals sent to GPIO pins

    Attributes:
        config_options: Array containing GPIO pin numbers in Broadcomm standard
    """

    def __init__(self, config_options=None):
        self._red = config_options['red_pin'] if config_options is not None else RGB_RED
        self._green = config_options['green_pin'] if config_options is not None else RGB_GREEN
        self._blue = config_options['blue_pin'] if config_options is not None else RGB_BLUE
        self._cyan = [self._green, self._blue]
        self._magenta = [self._red, self._blue]
        self._yellow = [self._red, self._green]
        self._white = [self._red, self._green, self._blue]
        self._led_setup()

    def _led_setup(self):
        # Set up the wiring
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BCM)
        # Setup Ports
        for val in self._white:
            GPIO.setup(val, GPIO.OUT)
        self.led_clear()

    def set_color(self, color):
        self.led_clear()
        if isinstance(color, int):
            GPIO.output(color, RGB_ENABLE)
        else:
            for c in color:
                GPIO.output(c, RGB_ENABLE)

    def led_clear(self):
        for val in self._white:
            GPIO.output(val, RGB_DISABLE)

    def led_cleanup(self):
        self.led_clear()
        GPIO.cleanup(self._white)


# Test harnesses
if __name__ == '__main__':
    try:
        with open('../../robot_1.cfg') as config_file:
            config_option = json.load(config_file)
    except IOError:
        logging.error("Configuration file could not be read: {}".format('../../robot_1.cfg'))
        raise SystemExit

    rgbled = RGBLED(config_option)
    rgbled.set_color(rgbled._cyan)
# End
