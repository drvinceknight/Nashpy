.. _how-to-use-moran_process_in_replacement_graph:

Use Moran processes on replacement graph
========================================

The Moran process method on the :code:`Game` class can take an
:code:`replacement_stochastic_matrix` which defines the replacement graph
as described in [Ohtsuki2007]_::

    >>> import nashpy as nash
    >>> import numpy as np
    >>> A = np.array([[3, 1], [1, 2]])
    >>> game = nash.Game(A)

In this case, the :code:`moran_process` method returns a generator of a given
collection of generations where individuals replace individuals as with
probability proportional to the weighted directed replacement graph (in the
example below, there are actually two disconnected components)::

    >>> np.random.seed(0)
    >>> replacement_stochastic_matrix = np.array(((1 / 2, 1 / 2, 0, 0), (1 / 2, 1 / 2, 0, 0), (0, 0, 1 / 2, 1 / 2), (0, 0, 1 / 2, 1 / 2)))
    >>> generations = game.moran_process(initial_population=(0, 1, 1, 0), replacement_stochastic_matrix=replacement_stochastic_matrix)
    >>> for population in generations:
    ...     print(population)
    [0 1 1 1]
    [0 1 1 1]
    [0 1 1 1]
    [0 1 1 1]
    [0 1 1 1]
    [0 1 1 1]
    [0 1 1 1]
    [0 1 1 1]
    [0 0 1 1]
