.. _how-to-use-imitation-dynamics:

Use Imitation Dynamics
======================

One of the algorithms implemented in :code:`Nashpy` is called
:code:`imitation_dynamics()`, this is implemented as a method on the :code:`Game`
class::

    >>> import nashpy as nash
    >>> import numpy as np
    >>> A = np.array([[3, -1], [-1, 3]])
    >>> B = np.array([[-3, 1], [1, -3]])
    >>> rps = nash.Game(A,B)

This :code:`imitation_dynamics` method returns a generator of the outcomes 
of the imitation dynamics algorithm::

    >>> ne_imitation_dynamics = rps.imitation_dynamics()
    >>> print(list(ne_imitation_dynamics))
    [(array([0., 1.]), array([1., 0.]))]

:code:`imitation_dynamics` takes the following parameters  :code:`iterations`, :code:`population_size`, :code:`random_seed` and :code:`threshold` within the function :code:`imitation_dynamics`.

    >>> import nashpy as nash
    >>> import numpy as np
    >>> A = np.array([[3, -1,3], [-1, 3,6], [-1, 1,2]])
    >>> B = np.array([[-3, 1,4], [1, -3,3], [-1, 3,4]])
    >>> rps = nash.Game(A,B)
    >>> population_size=200
    >>> iterations=100
    >>> random_seed=30
    >>> threshold=0.3
    >>> ne_imitation_dynamics = rps.imitation_dynamics(population_size=population_size,iterations=iterations,random_seed=random_seed,threshold=threshold)
    >>> list(ne_imitation_dynamics)
    [(array([0., 1., 0.]), array([1., 0., 1.]))]
