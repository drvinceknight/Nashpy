.. _how-to-use-discrete-replicator-dynamics:

Use discrete replicator dynamics
=====================================

One of the algorithms implemented in :code:`Nashpy` is called :ref:`discrete-replicator-dynamics`, this is implemented as a
method on the :code:`Game` class::

    >>> import nashpy as nash
    >>> import numpy as np
    >>> A = np.array([[3, 2], [4, 1]])
    >>> game = nash.Game(A)

The :code:`discrete_replicator-dynamics` produces the stratergy distribution for a given number of discrete time steps::
    >>> initial_distribution=np.array([0.2,0.8])
    >>> stratergy_over_time = game.discrete_replicator_dynamics(initial_distribution, steps=100, quantize=False)
    >>> stratergy_over_time
    array([[0.25581395, 0.74418605],
           [0.30494427, 0.69505573],
           [0.34559999, 0.65440001],
    ...
           [0.5       , 0.5       ],
           [0.5       , 0.5       ],
           [0.5       , 0.5       ]])

Quantization can be toggled to model a finite intager population::
    >>> initial_distribution=np.array([20,80])
    >>> stratergy_over_time = game.discrete_replicator_dynamics(initial_distribution, steps=100, quantize=True)
    >>> stratergy_over_time
    array([[26., 74.],
           [31., 69.],
           [35., 65.],
    ...
           [48., 52.],
           [48., 52.],
           [48., 52.]])