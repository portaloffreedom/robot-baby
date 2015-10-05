import numpy as np
from scipy.interpolate import splev, splrep

__author__ = 'matteo'


class RLPowerController:
    def __init__(self, spline=None, interval_step=1, intermediate_values=50):
        self._spline = spline if spline is not None else np.array([])
        self._interval_step = interval_step
        self._intermediate_values = intermediate_values
        self._x = np.array([])
        self._x2 = np.linspace(0, self._interval_step, self._intermediate_values)

        self._interpolate()

    def _interpolate(self):
        y = np.append(self._spline, self._spline[0])

        if len(self._x) != len(self._spline):
            self._x = np.linspace(0, self._interval_step, len(y))

        # `per` stands for periodic
        tck = splrep(self._x, y, per=True)

        y2 = splev(self._x2, tck)

        self._interpolate_cache = y2
        return y2

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
        if isinstance(x, np.ndarray):
            # TODO this doens't work yet
            for i, e in x:
                x[i] = self._seek_value(e)
        else:
            x = self._seek_value(x)

        return np.interp(x, self._x2, self._interpolate_cache)
