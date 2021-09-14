.. _how-to-use-support-enumeration:

Solve with support enumeration
==============================

One of the algorithms implemented in :code:`Nashpy` is called
:code:`support-enumeration`, this is implemented as a method on the :code:`Game`
class::

    >>> import nashpy as nash
    >>> import numpy as np
    >>> A = np.array([[1, -1], [-1, 1]])
    >>> matching_pennies = nash.Game(A)

This :code:`support_enumeration` method returns a generator of all the
equilibria::

    >>> equilibria = matching_pennies.support_enumeration()
    >>> for eq in equilibria:
    ...     print(eq)
    (array([0.5, 0.5]), array([0.5, 0.5]))
