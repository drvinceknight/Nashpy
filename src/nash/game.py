"""A class for a normal form game"""
import numpy as np
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

    def obtain_equilibria(self):
        """
        Obtain the Nash equilibria using support enumeration.

        Algorithm implemented here is Algorithm 3.4 of [NN2007]_
        with an aspect of pruning from [SLB2008]_.

        1. For each k in 1...min(size of strategy sets)
        2. For each I,J supports of size k
        3. Solve indifference conditions
        4. Check that have Nash Equilibrium.
        """
        return ((s1, s2)
                for s1, s2, sup1, sup2 in self.indifference_strategies()
                if self.is_ne((s1, s2), (sup1, sup2)))

    @staticmethod
    def obey_support(strategy, support):
        """Test if a strategy obeys it's support"""
        if strategy is False:
            return False
        if not all((i in support and value > 0) or
                   (i not in support and value <= 0)
                   for i, value in enumerate(strategy)):
            return False
        return True

    def is_ne(self, strategy_pair, support_pair):
        """
        Test if a given strategy pair is a pair of best responses
        """
        # Payoff against opponents strategies:
        u = strategy_pair[1].reshape(strategy_pair[1].size, 1)
        row_payoffs = np.dot(self.payoff_matrices[0], u)

        v = strategy_pair[0].reshape(strategy_pair[0].size, 1)
        column_payoffs = np.dot(self.payoff_matrices[1].T, v)

        # Pure payoffs on current support:
        row_support_payoffs = row_payoffs[np.array(support_pair[0])]
        column_support_payoffs = column_payoffs[np.array(support_pair[1])]

        return (row_payoffs.max() == row_support_payoffs.max() and
                column_payoffs.max() == column_support_payoffs.max())

    def potential_support_pairs(self):
        """
        A generator for the potential support pairs
        """
        p1_num_strategies, p2_num_strategies = self.payoff_matrices[0].shape
        for support1 in (s for s in powerset(p1_num_strategies) if len(s) > 0):
            for support2 in (s for s in powerset(p2_num_strategies)
                             if len(s) == len(support1)):
                yield support1, support2

    def indifference_strategies(self):
        """
        A generator for the strategies corresponding to the potential supports
        """
        for pair in self.potential_support_pairs():
            s1 = self.solve_indifference(self.payoff_matrices[1].T, *(pair[::-1]))
            s2 = self.solve_indifference(self.payoff_matrices[0], *pair)

            if self.obey_support(s1, pair[0]) and \
               self.obey_support(s2, pair[1]):
                yield s1, s2, pair[0], pair[1]

    @staticmethod
    def solve_indifference(A, rows=None, columns=None):
        """
        Solve the indifference for a payoff matrix assuming support for the
        strategies given by columns

        Finds vector of probabilities that makes player indifferent between
        rows.  (So finds probability vector for corresponding column player)
        """
        # Ensure differences between pairs of pure strategies are the same
        M = (A[np.array(rows)] - np.roll(A[np.array(rows)], 1, axis=0))[:-1]

        # Ensure have probability vector
        M = np.append(M, [[1 for _ in M.T]], axis=0)

        # Columns that must be played with prob 0
        zero_columns = set(range(A.shape[1])) - set(columns)
        b = np.append(np.zeros(len(M) - 1), [1] + [0 for _ in zero_columns])

        if zero_columns != set():
            M = np.append(M, [[int(i == j) for i, col in enumerate(M.T)]
                              for j in zero_columns], axis=0)

        try:
            prob = np.linalg.solve(M, b)
            if all(prob >= 0):
                return prob
        except np.linalg.linalg.LinAlgError:
            return False
        return False
