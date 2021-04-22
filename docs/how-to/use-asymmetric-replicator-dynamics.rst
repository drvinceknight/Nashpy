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

    >>> game.asymmetric_replicator_dynamics()
    (array([[0.5       , 0.5       ],
            [0.49875501, 0.50124499],
            [0.49752257, 0.50247743],
            ...,
            [0.41421355, 0.58578645],
            [0.41421355, 0.58578645],
            [0.41421355, 0.58578645]]),
    array([[5.00000000e-01, 5.00000000e-01],
            [4.94995170e-01, 5.05004830e-01],
            [4.89991349e-01, 5.10008651e-01],
            ...,
            [2.28749299e-09, 9.99999998e-01],
            [2.24298132e-09, 9.99999998e-01],
            [2.19926532e-09, 9.99999998e-01]]))
    


It is also possible to pass :code:`x0` and :code:`y0` arguments to assign the 
initial strategy to be played. Otherwise the probability is divided equally 
amongst all possible actions for both :code:`x0` and :code:`y0`. Additionally, a
:code:`timepoints` argument may be passed that gives the algorithm a sequence of
timepoints over which to calculate the strategies.

    >>> x0 = np.array([0.4, 0.6])
    >>> y0 = np.array([0.9, 0.1])
    >>> timepoints = np.linspace(0, 10, 1000)
    >>> game.asymmetric_replicator_dynamics(x0=x0, y0=y0, timepoints=timepoints)
    (array([[0.4       , 0.6       ],
            [0.39784197, 0.60215803],
            [0.39569229, 0.60430771],
            ...,
            [0.17411242, 0.82588758],
            [0.17411242, 0.82588758],
            [0.17411242, 0.82588758]]),
    array([[9.00000000e-01, 1.00000000e-01],
            [8.98183704e-01, 1.01816296e-01],
            [8.96338222e-01, 1.03661778e-01],
            ...,
            [1.86696960e-08, 9.99999981e-01],
            [1.82868387e-08, 9.99999982e-01],
            [1.79139464e-08, 9.99999982e-01]]))



