.. _how-to-use-minimax:

Use the minimax theorem
=======================

One of the algorithms implemented in :code:`Nashpy` is based on :ref:`the
minimax theorem <the-minimax-theorem>`, this is implemented as a
method on the :code:`Game` class::

    >>> import nashpy as nash
    >>> import numpy as np
    >>> A = np.array([[1, -1], [-1, 1]])
    >>> matching_pennies = nash.Game(A)

This returns the Nash equilibria by solving the underlying :ref:`linear program
<formulation-of-linear-program>`::

    >>> matching_pennies.linear_program()
    (array([0.5, 0.5]), array([0.5, 0.5]))

Note that this is only defined for :ref:`Zero sum games <zero-sum-games>`::

    >>> A = np.array([[1, -1], [-1, 1]])
    >>> B = np.array([[2, -2], [-2, 2]])
    >>> game = nash.Game(A, B)
    >>> game.linear_program()
    Traceback (most recent call last):
    ...
    ValueError: The Linear Program corresponding to the minimax theorem is defined only for Zero Sum games.
