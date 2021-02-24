Use replicator dynamics
=======================

One of the learning algorithms implemented in :code:`Nashpy` is called
:ref:`replicator-dynamics`, this is implemented as a method on the :code:`Game` 
class::

    >>> import nashpy as nash
    >>> import numpy as np
    >>> A = np.array([[3, 2], [4, 2]])
    >>> game = nash.Game(A)

The :code:`replicator_dynamics` method returns the strategies of the row player 
over time::

    >>> game.replicator_dynamics()
    array([[0.5       , 0.5       ],
           [0.49875032, 0.50124968],
           [0.49750377, 0.50249623],
    ...
           [0.10199196, 0.89800804],
           [0.10189853, 0.89810147],
           [0.10180527, 0.89819473]])



It is also possible to pass a :code:`y0` variable in order to assign a starting 
strategy. Otherwise the probability is divided equally amongst all possible 
actions. Passing a :code:`timepoints` variable gives the algorithm a sequence of 
timepoints over which to calculate the strategies::

    >>> y0 = np.array([0.9, 0.1])
    >>> timepoints = np.linspace(0, 10, 1000)
    >>> game.replicator_dynamics(y0=y0, timepoints=timepoints)
    array([[0.9       , 0.1       ],
           [0.89918663, 0.10081337],
           [0.89836814, 0.10163186],
    ...
           [0.14109126, 0.85890874],
           [0.1409203 , 0.8590797 ],
           [0.14074972, 0.85925028]])