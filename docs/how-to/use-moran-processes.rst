Use Moran processes
===================

Moran processes are implemented in :code:`Nashpy`
 as a method on the :code:`Game`
class::

    >>> import nashpy as nash
    >>> import numpy as np
    >>> A = np.array([[3, 1], [0, 2]])
    >>> game = nash.Game(A)

The :code:`moran_process` method returns a generator of a given collection of
generations::

    >>> np.random.seed(0)
    >>> generations = game.moran_process(initial_population=(1, 5))
    >>> for population in generations:
    ...     print(population)
    [0 0] [0 0]
    [1. 0.] [0. 1.]
    ...
    [498.   1.] [497.   2.]
    [499.   1.] [498.   2.]

Note that this process is stochastic::

    >>> np.random.seed(1)
    >>> generations = game.moran_process(initial_population=(1, 5))
    >>> for population in generations:
    ...     print(population)
    [0 0] [0 0]
    [1. 0.] [0. 1.]
    ...
    [498.   1.] [497.   2.]
    [499.   1.] [498.   2.]
