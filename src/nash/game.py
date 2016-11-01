"""A class for a normal form game"""
import numpy as np

class Game:
    """
    A class for a normal form game.

    Parameters
    ----------

        - A, B: 2 dimensional numpy array representing the payoff matrices for
          non zero sum games.
        - A: 2 dimensional numpy array representing the payoff matrix for a
          zero sum game.
    """
    def __init__(self, *args):
        if len(args) == 2:
            self.payoff_matrices = args
        if len(args) == 1:
            self.payoff_matrices = args[0], -args[0]
        self.zero_sum = np.array_equal(self.payoff_matrices[0],
                                       -self.payoff_matrices[1])


