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


def solve_indifference(A, rows=None, columns=None):
    """
    Solve the indifference for a payoff matrix assuming support for the
    strategies given by columns

    Finds vector of probabilities that makes player indifferent between
    rows.  (So finds probability vector for corresponding column player)

    Parameters
    ----------

        A: a 2 dimensional numpy array (A payoff matrix for the row player)
        rows: the support played by the row player
        columns: the support player by the column player

    Returns
    -------

        A numpy array:
        A probability vector for the column player that makes the row
        player indifferent. Will return False if all entries are not >= 0.
    """
    # Ensure differences between pairs of pure strategies are the same
    M = (A[np.array(rows)] - np.roll(A[np.array(rows)], 1, axis=0))[:-1]

    # Columns that must be played with prob 0
    zero_columns = set(range(A.shape[1])) - set(columns)

    if zero_columns != set():
        M = np.append(M, [[int(i == j) for i, col in enumerate(M.T)]
                          for j in zero_columns], axis=0)

    # Ensure have probability vector
    M = np.append(M, np.ones((1, M.shape[1])), axis=0)
    b = np.append(np.zeros(len(M) - 1), [1])

    try:
        prob = np.linalg.solve(M, b)
        if all(prob >= 0):
            return prob
        return False
    except np.linalg.linalg.LinAlgError:
        return False

def potential_support_pairs(A, B):
    """
    A generator for the potential support pairs

    Returns
    -------

        A generator of all potential support pairs
    """
    p1_num_strategies, p2_num_strategies = A.shape
    for support1 in (s for s in powerset(p1_num_strategies) if len(s) > 0):
        for support2 in (s for s in powerset(p2_num_strategies)
                         if len(s) == len(support1)):
            yield support1, support2

def indifference_strategies(A, B):
    """
    A generator for the strategies corresponding to the potential supports

    Returns
    -------

        A generator of all potential strategies that are indifferent on each
        potential support. Return False if they are not valid (not a
        probability vector OR not fully on the given support).
    """
    for pair in potential_support_pairs(A, B):
        s1 = solve_indifference(B.T, *(pair[::-1]))
        s2 = solve_indifference(A, *pair)

        if obey_support(s1, pair[0]) and obey_support(s2, pair[1]):
            yield s1, s2, pair[0], pair[1]

def obey_support(strategy, support):
    """
    Test if a strategy obeys its support

    Parameters
    ----------

        strategy: a numpy array
            A given strategy vector
        support: a numpy array
            A strategy support

    Returns
    -------

        A boolean: whether or not that strategy does indeed have the given
        support
    """
    if strategy is False:
        return False
    if not all((i in support and value > 0) or
               (i not in support and value <= 0)
               for i, value in enumerate(strategy)):
        return False
    return True

def is_ne(strategy_pair, support_pair, payoff_matrices):
    """
    Test if a given strategy pair is a pair of best responses

    Parameters
    ----------

        strategy_pair: a 2-tuple of numpy arrays
        support_pair: a 2-tuple of numpy arrays
    """
    A, B = payoff_matrices
    # Payoff against opponents strategies:
    u = strategy_pair[1].reshape(strategy_pair[1].size, 1)
    row_payoffs = np.dot(A, u)

    v = strategy_pair[0].reshape(strategy_pair[0].size, 1)
    column_payoffs = np.dot(B.T, v)

    # Pure payoffs on current support:
    row_support_payoffs = row_payoffs[np.array(support_pair[0])]
    column_support_payoffs = column_payoffs[np.array(support_pair[1])]

    return (row_payoffs.max() == row_support_payoffs.max() and
            column_payoffs.max() == column_support_payoffs.max())

def support_enumeration(A, B):
    """
    Obtain the Nash equilibria using support enumeration.

    Algorithm implemented here is Algorithm 3.4 of [Nisan2007]_

    1. For each k in 1...min(size of strategy sets)
    2. For each I,J supports of size k
    3. Solve indifference conditions
    4. Check that have Nash Equilibrium.

    Returns
    -------

        equilibria: A generator.
    """
    return ((s1, s2)
            for s1, s2, sup1, sup2 in indifference_strategies(A, B)
            if is_ne((s1, s2), (sup1, sup2), (A, B)))
