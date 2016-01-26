import bisect
import json
import logging
import math
import numpy as np
import random
from learning.rlpower_controller import RLPowerController
from scipy.interpolate import splrep, splev
from hal.inputs.fitness_querier import FitnessQuerier

__author__ = 'matteo'


class RLPowerAlgorithm:
    epsilon = 10 ** -10

    def __init__(self, config_parameters):
        self.RANKING_SIZE = config_parameters['ranking_size']
        self.NUM_SERVOS = len(config_parameters['servo_pins'])
        # In the original algorithm they used variance and square-rooted it every time. We're using standard deviation
        # and decay parameter is also a square root of the parameter from original algorithm
        self._sigma = math.sqrt(config_parameters['variance'])
        self._sigma_decay = math.sqrt(config_parameters['sigma_decay_squared'])
        self._initial_spline_size = config_parameters['initial_spline_size']
        self._end_spline_size = config_parameters['end_spline_size']
        self._number_of_fitness_evaluations = config_parameters['number_of_fitness_evaluations']
        self._fitness_evaluation = config_parameters['fitness_evaluation_method']
        self._runtime_data_file = config_parameters['runtime_data_file']
        self._light_fitness_weight = config_parameters['light_fitness_weight']
        self._current_spline_size = self._initial_spline_size
        self._current_evaluation = 0

        # Create an instance of fitness querier
        if self._fitness_evaluation == 'auto':
            self._fitness_querier = FitnessQuerier(config_parameters)
            self._fitness_querier.start()

        # Recover evaluation data from tmp file
        self._runtime_data = self._load_runtime_data_from_file(self._runtime_data_file)
        if 'last_spline' in self._runtime_data:
            self.ranking = self._runtime_data['ranking']
            self._current_spline = self._runtime_data['last_spline']
            self._sigma = self._runtime_data['sigma']
            self._current_spline_size = len(self._current_spline[0])
            self._current_evaluation = self._runtime_data['evaluation']
        else:
            self.ranking = []
            # Spline initialisation
            self._current_spline = np.array(
                [[0.5 + random.normalvariate(0, self._sigma) for x in range(self._initial_spline_size)]
                    for y in range(self.NUM_SERVOS)])
        self.controller = RLPowerController(self._current_spline)

    def next_evaluation(self, light_sensor_value=0):
        logging.info("current spline size: {}".format(self._current_spline_size))
        movement_fitness = self.get_current_fitness()
        light_fitness = self._light_fitness_weight * light_sensor_value
        current_fitness = movement_fitness + light_fitness
        logging.info("Last evaluation fitness: {} (movement: {} + light: {})".format(current_fitness, movement_fitness, light_fitness))
        logging.info("Current position: {}".format(self._fitness_querier.get_position()))
        self.save_in_ranking(current_fitness, self._current_spline)
        self._current_evaluation += 1
        if math.floor((self._end_spline_size - self._initial_spline_size)/self._number_of_fitness_evaluations *
                              self._current_evaluation) + 3 > self._current_spline_size:
            self._current_spline_size += 1
            self._current_spline = self.recalculate_spline(self._current_spline, self._current_spline_size)
            for number, (fitness, rspline) in enumerate(self.ranking):
                self.ranking[number] = _RankingEntry((fitness, self.recalculate_spline(rspline, self._current_spline_size)))
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
        self._save_runtime_data_to_file(self._runtime_data_file)
        self._fitness_querier.start()

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
        elif self._fitness_evaluation == 'auto':
            # TODO: figure out how to handle multiple fitness values
            fitness = self._fitness_querier.get_fitness()
            #logging.info("fitness: {}".format(fitness))
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
        self._save_runtime_data_to_file(self._runtime_data_file)

    def _load_runtime_data_from_file(self, filename):
        try:
            with open(filename) as json_data:
                d = json.load(json_data)
                ranking_serialized = d['ranking']
                ranking = [_RankingEntry((elem['fitness'], np.array(elem['spline']))) for elem in ranking_serialized]
                d['ranking'] = ranking
                d['last_spline'] = np.array(d['last_spline'])
                return d
        except IOError:
            return {}

    def _save_runtime_data_to_file(self, filename):
        ranking_serialized = [{'fitness': f, 'spline': s.tolist()} for (f, s) in self.ranking]
        data = {'ranking': ranking_serialized,
                'last_spline': self._current_spline.tolist(),
                'sigma': self._sigma,
                'evaluation': self._current_evaluation
                }
        with open(filename, 'w') as outfile:
            json.dump(data, outfile)

class _RankingEntry(tuple):
    def __lt__(self, other):
        return other[0] > self[0]

    def __gt__(self, other):
        return not self.__lt__(other)
