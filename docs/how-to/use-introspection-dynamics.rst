.. _how-to-use-introspection-dynamics:

Use Introspection Dynamics
==========================

Introspection dynamics is implemented in :code:`Nashpy` as a method on the
:code:`Game` class::

    >>> import nashpy as nash
    >>> import numpy as np
    >>> A = np.array([[3, 1], [1, 2]])
    >>> B = np.array([[3, 6], [5, 2]])
    >>> game = nash.Game(A, B)

The :code:`introspection_dynamics` method returns a generator of a given collection of
generations::

    >>> np.random.seed(0)
    >>> steps = game.moran_process(number_of_iterations=50)
    >>> for actions in steps:
    ...     print(actions)
    [0 0 1]
    [0 1 1]
    [0 1 1]
    ...
    [0 1 1]
    [1 1 1]

Note that this process is stochastic::

    >>> np.random.seed(2)
    >>> steps = game.moran_process(number_of_iterations=50)
    >>> for actions in steps:
    ...     print(actions)
    [0 0 1]
    [0 0 1]
    [0 0 0]
    ...
    [0 0 1]
    [0 0 0]
