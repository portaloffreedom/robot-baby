import bisect
import logging
import numpy as np
import random
from learning.rlpower_controller import RLPowerController

__author__ = 'matteo'


class RLPowerAlgorithm:
    epsilon = 10 ** -10

    def __init__(self, config_parameters):
        # TODO: get the following parameters from config file
        self.RANKING_SIZE = 10
        self.NUM_SERVOS = 8
        self.SIGMA = 0.2
        self._spline_size = 3
        self._fitness_evaluation = 'manual'

        self.ranking = []
        # Spline initialisation
        self._current_spline = np.array(
            [[0.5 + random.normalvariate(0, self.SIGMA) for x in range(self._spline_size)]
             for y in range(self.NUM_SERVOS)])
        self.controller = RLPowerController(self._current_spline)

    def next_evaluation(self, controller):
        current_fitness = self.get_current_fitness()
        self.save_in_ranking(current_fitness, self._current_spline)
        # Add random noise to the spline
        uniform = np.array(
            [[random.normalvariate(0, self.SIGMA) for x in range(self._spline_size)] for y in range(self.NUM_SERVOS)])
        # Add a weighted average of the best splines seen so far
        total = self.epsilon  # something similar to 0, but not 0 ( division by 0 is evil )
        modifier = np.zeros(self._current_spline.shape)
        for (fitness, spline) in self.ranking:
            total += fitness
            modifier += (spline - self._current_spline) * fitness
        self._current_spline = self._current_spline + uniform + modifier / total
        self.controller.set_spline(self._current_spline)

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
            bisect.insort(self.ranking, (current_fitness, current_spline))
        elif current_fitness > self.ranking[0][0]:
            bisect.insort(self.ranking, (current_fitness, current_spline))
            self.ranking.pop(0)
