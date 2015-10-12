import bisect
import logging
import math
import numpy as np
import random
from learning.rlpower_controller import RLPowerController
from scipy.interpolate import splrep, splev

__author__ = 'matteo'


class RLPowerAlgorithm:
    epsilon = 10 ** -10

    def __init__(self, config_parameters):
        # TODO: get the following parameters from config file
        self.RANKING_SIZE = 10
        self.NUM_SERVOS = 8
        # In the original algorithm they used variance and square-rooted it every time. We're using standard deviation
        # and decay parameter is also a square root of the parameter from original algorithm
        self._sigma = math.sqrt(0.008)
        self._sigma_decay = math.sqrt(0.98)
        self._initial_spline_size = 3
        self._current_spline_size = self._initial_spline_size
        self._end_spline_size = 100
        self._number_of_fitness_evaluations = 500
        self._current_evaluation = 0
        self._fitness_evaluation = 'manual'

        self.ranking = []
        # Spline initialisation
        self._current_spline = np.array(
            [[0.5 + random.normalvariate(0, self._sigma) for x in range(self._initial_spline_size)]
             for y in range(self.NUM_SERVOS)])
        self.controller = RLPowerController(self._current_spline)

    def next_evaluation(self, controller):
        current_fitness = self.get_current_fitness()
        self.save_in_ranking(current_fitness, self._current_spline)
        self._current_evaluation += 1
        if math.floor((self._end_spline_size - self._initial_spline_size)/self._number_of_fitness_evaluations *
                              self._current_evaluation) + 3 > self._current_evaluation:
            self._current_spline_size += 1
            self._current_spline = self.recalculate_spline(self._current_spline, self._current_spline_size)
            for number, (fitness, rspline) in enumerate(self.ranking):
                self.ranking[number] = _RankingEntry(fitness, self.recalculate_spline(rspline, self._current_spline_size))
        # Add random noise to the spline
        uniform = np.array(
            [[random.normalvariate(0, self._sigma) for x in range(self._current_spline_size)]
             for y in range(self.NUM_SERVOS)])
        # Add a weighted average of the best splines seen so far
        total = self.epsilon  # something similar to 0, but not 0 ( division by 0 is evil )
        modifier = np.zeros(self._current_spline.shape)
        for (fitness, spline) in self.ranking:
            total += fitness
            modifier += (spline - self._current_spline) * fitness
        self._current_spline = self._current_spline + uniform + modifier / total
        self.controller.set_spline(self._current_spline)
        self._sigma *= self._sigma_decay

    def recalculate_spline(self, spline, spline_size):
        return np.apply_along_axis(self._interpolate, 1, spline, spline_size + 1)

    def _interpolate(self, spline, spline_size):
        spline = np.append(spline, spline[0])
        x = np.linspace(0, 1, len(spline))
        tck = splrep(x, spline, per=True)
        x2 = np.linspace(0, 1, spline_size)
        return splev(x2, tck)[:-1]

    def get_current_fitness(self):
        # Manual fitness evaluation
        if self._fitness_evaluation == 'manual':
            fitness = float(input("Enter fitness of current gait: "))
        # Random fitness (for testing purposes)
        elif self._fitness_evaluation == 'random':
            fitness = 5 + random.normalvariate(0, 2)
        # TODO: evaluate fitness automatically
        elif self._fitness_evaluation == 'auto':
            raise NotImplementedError("auto mode fitness evaluation not ready")
        else:
            logging.error("Unknown fitness evaluation method")
            raise NameError("Unknown fitness evaluation method")
        return fitness

    def save_in_ranking(self, current_fitness, current_spline):
        if len(self.ranking) < self.RANKING_SIZE:
            bisect.insort(self.ranking, _RankingEntry((current_fitness, current_spline)))
        elif current_fitness > self.ranking[0][0]:
            bisect.insort(self.ranking, _RankingEntry((current_fitness, current_spline)))
            self.ranking.pop(0)


class _RankingEntry(tuple):
    def __lt__(self, other):
        return other[0] > self[0]

    def __gt__(self, other):
        return not self.__lt__(other)