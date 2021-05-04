Use asymmetric replicator dynamics
==================================

This algorithm that is implemented in :code:`Nashpy` is called 
:ref:`asymmetric-replicator-dynamics` and is implemented as a method on the 
:code:`Game` class::

    >>> import nashpy as nash
    >>> import numpy as np
    >>> A = np.array([[3, 2], [4, 2]])
    >>> B = np.array([[1, 3], [2, 4]])
    >>> game = nash.Game(A, B)

The :code:`asymmetric_replicator_dynamics` method returns the strategies of both
the row player and the column player over time::

    >>> xs, ys = game.asymmetric_replicator_dynamics()
    >>> xs
    array([[0.5       , 0.5       ],
           [0.49875..., 0.50124...],
           [0.49752..., 0.50247...],
           ...,
           [0.41421..., 0.58578...],
           [0.41421..., 0.58578...],
           [0.41421..., 0.58578...]])
    >>> ys
    array([[5.00000...e-01, 5.00000...e-01],
           [4.94995...e-01, 5.05004...e-01],
           [4.89991...e-01, 5.10008...e-01],
           ...,
           [2.28749...e-09, 9.99999...e-01],
           [2.24298...e-09, 9.99999...e-01],
           [2.19926...e-09, 9.99999...e-01]])


It is also possible to pass :code:`x0` and :code:`y0` arguments to assign the 
initial strategy to be played. Otherwise the probability is divided equally 
amongst all possible actions for both :code:`x0` and :code:`y0`. Additionally, a
:code:`timepoints` argument may be passed that gives the algorithm a sequence of
timepoints over which to calculate the strategies.

    >>> x0 = np.array([0.4, 0.6])
    >>> y0 = np.array([0.9, 0.1])
    >>> timepoints = np.linspace(0, 10, 1000)
    >>> xs, ys = game.asymmetric_replicator_dynamics(x0=x0, y0=y0, timepoints=timepoints)
    >>> xs
    array([[0.4       , 0.6       ],
           [0.39784..., 0.60215...],
           [0.39569..., 0.60430...],
           ...,
           [0.17411..., 0.82588...],
           [0.17411..., 0.82588...],
           [0.17411..., 0.82588...]])
    >>> ys
    array([[9.00000...e-01, 1.00000...e-01],
           [8.98183...e-01, 1.01816...e-01],
           [8.96338...e-01, 1.03661...e-01],
           ...,
           [1.86696...e-08, 9.99999...e-01],
           [1.82868...e-08, 9.99999...e-01],
           [1.79139...e-08, 9.99999...e-01]])



