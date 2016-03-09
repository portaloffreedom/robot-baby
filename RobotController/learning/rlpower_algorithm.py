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
    EPSILON = 10 ** -10

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
        self.aging_parameter = config_parameters['fitness_evaluation_aging_parameter']
        fitness_weights = config_parameters['fitness_weights']
        self._average_norm_factor = 2 / \
            (fitness_weights[0] + fitness_weights[1] + self._light_fitness_weight + self.EPSILON)

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

    def _total_ranking_fitness(self):
        total = 0.0
        for rank in self.ranking:
            total += rank.fitness
        return total

    def _average_ranking_fitness(self):
        return self._total_ranking_fitness() / len(self.ranking)

    def _generate_spline(self):
        # Add a weighted average of the best splines seen so far
        total = self.EPSILON  # something similar to 0, but not 0 ( division by 0 is evil )
        modifier = np.zeros(self._current_spline.shape)
        for rank_entry in self.ranking:
            total += rank_entry.fitness
            modifier += (rank_entry.spline - self._current_spline) * rank_entry.fitness

        # random noise for the spline
        randomness_factor = self._sigma
        # the lower the overall fitness, the higher the randomness factor
        randomness_factor /= (self._average_ranking_fitness() / self._average_norm_factor) + self.EPSILON
        randomness_factor = max(randomness_factor, self._sigma)

        noise = np.array(
            [[random.normalvariate(0, randomness_factor) for x in range(self._current_spline_size)]
             for y in range(self.NUM_SERVOS)])

        return self._current_spline + noise + modifier / total

    def skip_evaluation(self):
        logging.info("Skipping evaluation, starting new one")
        self._current_spline = self._generate_spline()
        self.controller.set_spline(self._current_spline)
        self._fitness_querier.start()

    def next_evaluation(self, light_sensor_value=0):
        self._current_evaluation += 1
        logging.info("current spline size: {}".format(self._current_spline_size))

        # generate fitness
        movement_fitness = self.get_current_fitness()
        light_fitness = self._light_fitness_weight * light_sensor_value
        current_fitness = movement_fitness + light_fitness
        logging.info("Last evaluation fitness: {} (movement: {} + light: {})".format(current_fitness, movement_fitness, light_fitness))
        logging.info("Current position: {}".format(self._fitness_querier.get_position()))

        # save old evaluation
        self._age_old_ranking()
        self.save_in_ranking(current_fitness, self._current_spline)

        # check if is time to increase the number of evaluations
        if math.floor((self._end_spline_size - self._initial_spline_size)/self._number_of_fitness_evaluations *
                              self._current_evaluation) + 3 > self._current_spline_size:
            self._current_spline_size += 1
            self._current_spline = self.recalculate_spline(self._current_spline, self._current_spline_size)
            for number, rank_entry in enumerate(self.ranking):
                self.ranking[number] = _RankingEntry(rank_entry.fitness, self.recalculate_spline(rank_entry.spline, self._current_spline_size))

        # update values
        self._current_spline = self._generate_spline()
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

    def _age_old_ranking(self):
        for rank in self.ranking:
            rank.fitness *= self.aging_parameter

    def get_current_fitness(self):
        # Manual fitness evaluation
        if self._fitness_evaluation == 'manual':
            fitness = float(input("Enter fitness of current gait: "))
        # Random fitness (for testing purposes)
        elif self._fitness_evaluation == 'random':
            fitness = 5 + random.normalvariate(0, 2)
        elif self._fitness_evaluation == 'auto':
            fitness = self._fitness_querier.get_fitness()
            #logging.info("fitness: {}".format(fitness))
        else:
            logging.error("Unknown fitness evaluation method")
            raise NameError("Unknown fitness evaluation method")
        return fitness

    def save_in_ranking(self, current_fitness, current_spline):
        if len(self.ranking) < self.RANKING_SIZE:
            bisect.insort(self.ranking, _RankingEntry(current_fitness, current_spline))
        elif current_fitness > self.ranking[0].fitness:
            bisect.insort(self.ranking, _RankingEntry(current_fitness, current_spline))
            self.ranking.pop(0)
        self._save_runtime_data_to_file(self._runtime_data_file)

    @staticmethod
    def _load_runtime_data_from_file(filename):
        try:
            with open(filename) as json_data:
                d = json.load(json_data)
                ranking_serialized = d['ranking']
                ranking = [_RankingEntry(elem['fitness'], np.array(elem['spline'])) for elem in ranking_serialized]
                d['ranking'] = ranking
                d['last_spline'] = np.array(d['last_spline'])
                return d
        except IOError:
            return {}

    def _save_runtime_data_to_file(self, filename):
        ranking_serialized = [{'fitness': rank_entry.fitness, 'spline': rank_entry.spline.tolist()} for rank_entry in self.ranking]
        data = {'ranking': ranking_serialized,
                'last_spline': self._current_spline.tolist(),
                'sigma': self._sigma,
                'evaluation': self._current_evaluation
                }
        with open(filename, 'w') as outfile:
            json.dump(data, outfile)


class _RankingEntry:
    def __init__(self, fitness, spline):
        self.fitness = fitness
        self.spline = spline

    def __lt__(self, other):
        return other.fitness > self.fitness

    def __gt__(self, other):
        return not self.__lt__(other)
