.. _how-to-check-best-responses:

Check if a strategy is a best response
======================================

A game can be passed a pair of :ref:`strategies-discussion` to check if they are
best responses to each other.
Let us create a game to illustrate this::

    >>> import nashpy as nash
    >>> import numpy as np
    >>> A = np.array([[3, 0], [5, 1]])
    >>> B = np.array([[3, 5], [0, 1]])
    >>> prisoners_dilemma = nash.Game(A, B)

The :code:`is_best_response` method returns a pair of booleans. In this
instance, the row player strategy is a best response to the column player's but
not vice versa::

    >>> sigma_r = np.array([0, 1])
    >>> sigma_c = np.array([1, 0])
    >>> prisoners_dilemma.is_best_response(sigma_r, sigma_c)
    (True, False)
