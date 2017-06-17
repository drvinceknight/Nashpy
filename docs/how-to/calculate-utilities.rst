Calculate utilities
===================

A game can be passed a pair of mixed strategies (distributions over the set of
pure strategies) to return the utilities. Let us create a game to illustrate
this::

    >>> import nash
    >>> import numpy as np
    >>> A = np.array([[3, 0], [5, 1]])
    >>> B = np.array([[3, 5], [0, 1]])
    >>> prisoners_dilemma = nash.Game(A, B)

The utility for both players when they both play their first strategy::

    >>> sigma_r = np.array([1, 0])
    >>> sigma_c = np.array([1, 0])
    >>> prisoners_dilemma[sigma_r, sigma_c]
    array([3, 3])

The utility to both players when they play uniformly randomly across both their
strategies::

    >>> sigma_r = np.array([1 / 2, 1 / 2])
    >>> sigma_c = np.array([1 / 2, 1 / 2])
    >>> prisoners_dilemma[sigma_r, sigma_c]
    array([ 2.25,  2.25])
