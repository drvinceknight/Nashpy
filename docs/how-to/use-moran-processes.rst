.. _how-to-use-moran_process:

Use Moran processes
===================

Moran processes are implemented in :code:`Nashpy` as a method on the
:code:`Game` class::

    >>> import nashpy as nash
    >>> import numpy as np
    >>> A = np.array([[3, 1], [1, 2]])
    >>> game = nash.Game(A)

The :code:`moran_process` method returns a generator of a given collection of
generations::

    >>> np.random.seed(0)
    >>> generations = game.moran_process(initial_population=(0, 0, 1))
    >>> for population in generations:
    ...     print(population)
    [0 0 1]
    [0 1 1]
    [0 1 1]
    ...
    [0 1 1]
    [1 1 1]

Note that this process is stochastic::

    >>> np.random.seed(2)
    >>> generations = game.moran_process(initial_population=(0, 0, 1))
    >>> for population in generations:
    ...     print(population)
    [0 0 1]
    [0 0 1]
    [0 0 0]

Currently, only positive valued matrices are supported::

    >>> A = np.array([[3, 0], [1, 2]])
    >>> game = nash.Game(A)
    >>> generations = game.moran_process(initial_population=(0, 0, 1))
    >>> for population in generations:
    ...     print(population)
    Traceback (most recent call last):
     ...
    ValueError: Only positive valued payoff matrices are currently supported
