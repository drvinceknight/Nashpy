Solve with vertex enumeration
=============================

One of the algorithms implemented in :code:`Nashpy` is called
:ref:`vertex-enumeration`, this is implemented as a method on the :code:`Game`
class::

    >>> import nashpy as nash
    >>> import numpy as np
    >>> A = np.array([[1, -1], [-1, 1]])
    >>> matching_pennies = nash.Game(A)

This :code:`vertex_enumeration` method returns a generator of all the
equilibria::

    >>> equilibria = matching_pennies.vertex_enumeration()
    >>> for eq in equilibria:
    ...     print(eq)
    (array([0.5, 0.5]), array([0.5, 0.5]))
