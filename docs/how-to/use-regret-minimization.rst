.. _how-to-use-regret-minimization:

Use with Regret Minimization
============================

One of the algorithms implemented in :code:`Nashpy` is called
:code:`regret_minimization()`, this is implemented as a method on the :code:`Game`
class::

    >>> import nashpy as nash
    >>> import numpy as np
    >>> A = np.array([[3, -1], [-1, 3]])
    >>> B = np.array([[-3, 1], [1, -3]])
    >>> rps = nash.Game(A,B)

This :code:`regret_minimization` method returns a generator of the outcomes 
of the regret minimization algorithm::

    >>> ne_regret_mini = rps.regret_minimization()
    >>> print(list(ne_regret_mini))
    [([0.5, 0.5], [0.5, 0.5])]

:code:`regret_minimization` takes the following parameters :code:`learning_rate` and :code:`iterations`.

    >>> A = np.array([[3, -1,3], [-1, 3,6], [-1, 1,2]])
    >>> B = np.array([[-3, 1,4], [1, -3,3], [-1, 3,4]])
    >>> rps = nash.Game(A,B)
    >>> learning_rate = 0.2
    >>> iterations = 1000
    >>> ne_regret_mini = rps.regret_minimization(learning_rate=learning_rate,
    iterations=iterations)
    >>> print(list(ne_regret_mini))
    [([0.0, 1.0, 0.0], [0.0, 0.0, 1.0])]
