import random
import math


def sigmoid(x):
    return 1 / (1 + math.exp(-x))

def relu(x):
    return max(0,x)


class NeuroOptions:
    def __init__(self, options):
        self.options = {
            # Logistic activation function
            'activation': sigmoid,
            # Returns a random value between -1 and 1.
            'randomClamped': lambda: random.random(), # * 2 -1,
            # Perceptron network structure (1 hidden)
            'network': [1, [1], 1],
            # Population by generation.
            'population': 50,
            # Best networks kepts unchanged for the next generation (rate).
            'elitism': 0.2,
            # New random networks for the next generation (rate).
            'randomBehaviour': 0.2,
            # Mutation rate on the weights of synapses.
            'mutationRate': 0.1,
            # Interval of the mutation changes on the synapse weight.
            'mutationRange': 0.5,
            # Latest generations saved.
            'historic': 0,
            # Only save score (not the network).
            'lowHistoric': False,
            # Sort order (-1 = desc, 1 = asc).
            'scoreSort': -1,
            # Number of children by breeding.
            'nbChild': 1
        }
        self.set(options)

    def set(self, options):
        for items in options.items():
            self.options[items[0]] = items[1]
