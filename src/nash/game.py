"""A class for a normal form game"""
import numpy as np
from .algorithms.vertex_enumeration import vertex_enumeration
from .algorithms.support_enumeration import support_enumeration
from itertools import chain, combinations


def powerset(n):
    """
    A power set of range(n)

    Based on recipe from python itertools documentation:

    https://docs.python.org/2/library/itertools.html#recipes
    """
    return chain.from_iterable(combinations(range(n), r) for r in range(n + 1))


class Game:
    """
    A class for a normal form game.

    Parameters
    ----------

        - A, B: 2 dimensional list/arrays representing the payoff matrices for
          non zero sum games.
        - A: 2 dimensional list/array representing the payoff matrix for a
          zero sum game.
    """
    def __init__(self, *args):
        if len(args) == 2:
            self.payoff_matrices = tuple([np.asarray(m) for m in args])
        if len(args) == 1:
            self.payoff_matrices = np.asarray(args[0]), -np.asarray(args[0])
        self.zero_sum = np.array_equal(self.payoff_matrices[0],
                                       -self.payoff_matrices[1])

    def __repr__(self):
        if self.zero_sum:
            tpe = "Zero sum"
        else:
            tpe = "Bi matrix"
        return """{} game with payoff matrices:

Row player:
{}

Column player:
{}""".format(tpe, *self.payoff_matrices)

    def __getitem__(self, key):
        row_strategy, column_strategy = key
        return np.array([np.dot(row_strategy, np.dot(m, column_strategy))
                         for m in self.payoff_matrices])

    def vertex_enumeration(self):
        return vertex_enumeration(*self.payoff_matrices)

    def support_enumeration(self):
        return support_enumeration(*self.payoff_matrices)
