import pigpio
import time


class Servo:
    """Class for controlling servos using PWM signals sent to GPIO pins

     Attributes:
        pin: Integer containing GPIO pin number in Broadcomm standard
        freq: Frequency of sending PWM signals in Hz. Default: 50
        range: Range of values for duty cycle. Default: 1000 (500 = 50% dc)
        inverse: Boolean. Allows for servo direction to be inverted. Default: False
    """
    POSITION_OFF = 0
    POSITION_BEGIN = 40
    POSITION_MIDDLE = 75
    POSITION_END = 110

    def __init__(self, pin, freq=50, ran=1000, inverse=False):
        """Create a Servo at GPIO nr *pin* with frequency *freq*."""
        self._port = pin
        self._pi = pigpio.pi()
        self._pi.set_PWM_frequency(self._port, freq)
        self._pi.set_PWM_range(self._port, ran)
        if inverse:
            self._maxPWM, self._minPWM = self.POSITION_BEGIN, self.POSITION_END
        else:
            self._maxPWM, self._minPWM = self.POSITION_END, self.POSITION_BEGIN

    def move_to_position(self, position):
        """Sends signal to the engine to move to a specified position.
        Position should be in range [-1, 1] with 0 being the middle."""
        if position < -1:
            position = -1
        elif position > 1:
            position = 1

        position = self._minPWM + (1 + position) * (self._maxPWM - self._minPWM) / 2

        self._pi.set_PWM_dutycycle(self._port, position)

    def center(self):
        """Set servo position to center"""
        self.move_to_position(0)

    def off(self):
        """Turn PWM signalling off"""
        self._pi.set_PWM_dutycycle(self._port, 0)
