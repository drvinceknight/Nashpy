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

The :code:`initial_dropped_label` is an integer between :code:`0` and
:code:`sum(A.shape) - 1`. To iterate over all possible labels use the
:code:`enumerate_lemke_howson` which returns a generator::

    >>> equilibria = matching_pennies.enumerate_lemke_howson()
    >>> for eq in equilibria:
    ...     print(eq)
    (array([ 0.5,  0.5]), array([ 0.5,  0.5]))
    (array([ 0.5,  0.5]), array([ 0.5,  0.5]))
    (array([ 0.5,  0.5]), array([ 0.5,  0.5]))
    (array([ 0.5,  0.5]), array([ 0.5,  0.5]))

Note that this algorithm is not guaranteed to find **all** equilibria but is
an efficient way of finding an equilibrium.
