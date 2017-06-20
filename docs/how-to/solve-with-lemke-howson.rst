Solve with Lemke Howson
=======================

One of the algorithms implemented in :code:`Nashpy` is the *Lemke Howson*
algorithm. This algorithm does not return **all** equilibria and takes an input
argument::

    >>> import nash
    >>> import numpy as np
    >>> A = np.array([[1, -1], [-1, 1]])
    >>> matching_pennies = nash.Game(A)
    >>> matching_pennies.lemke_howson(initial_dropped_label=0)
    (array([ 0.5,  0.5]), array([ 0.5,  0.5]))
