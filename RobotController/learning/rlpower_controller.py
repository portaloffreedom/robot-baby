import random
import numpy as np
from scipy.interpolate import splev, splrep

__author__ = 'matteo'


class RLPowerController:
    def __init__(self, spline, interval_step=1, intermediate_values=50):
        self._spline = spline

        self._interval_step = interval_step
        self._intermediate_values = intermediate_values
        self._x = np.array([])
        self._x2 = np.linspace(0, self._interval_step, self._intermediate_values)

        self._interpolate()

    def _interpolate(self):
        self._interpolate_cache = []

        for spline_row in self._spline:
            y = np.append(spline_row, spline_row[0])

            if len(self._x) != len(y):
                self._x = np.linspace(0, self._interval_step, len(y))

            # `per` stands for periodic
            tck = splrep(self._x, y, per=True)

            y2 = splev(self._x2, tck)

            self._interpolate_cache.append(y2)

        return self._interpolate_cache

    def set_spline(self, spline):
        self._spline = spline
        self._interpolate()

    def get_spline(self):
        return self._spline

    def _seek_value(self, x):
        while x > self._interval_step:
            x -= self._interval_step
        return x

    def get_value(self, x):
        """
        Gets interpolated values using X as position vector
        :param x: an iterable object with a value for every row in the spline
        :return: interpolated values in a numpy.array object
        """
        if (type(x) is float) or (type(x) is int):
            x = [_x for _x in range(len(self._interpolate_cache))]
        elif (type(x) is list) or (type(x) is np.ndarray):
            pass
        else:
            raise ValueError("input is not a number nor an interable object")

        assert len(x) == len(self._interpolate_cache)

        result = []
        for index, e in x:
            e = self._seek_value(e)
            result.append(np.interp(e, self._x2, self._interpolate_cache[index]))

        return np.array(result)
