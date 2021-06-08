.. _how-to-create-a-normal-form-game:

Create a Normal Form Game
=========================

A game in :code:`Nashpy` is created by passing 1 or 2 matrices to the
:code:`nash.Game` class. Here is the zero sum game :ref:`matching-pennies`::

    >>> import nashpy as nash
    >>> import numpy as np
    >>> A = np.array([[1, -1], [-1, 1]])
    >>> matching_pennies = nash.Game(A)
    >>> matching_pennies
    Zero sum game with payoff matrices:
    <BLANKLINE>
    Row player:
    [[ 1 -1]
     [-1  1]]
    <BLANKLINE>
    Column player:
    [[-1  1]
     [ 1 -1]]

Here is the **non** zero sum game :ref:`prisoners-dilemma`::

    >>> import nashpy as nash
    >>> import numpy as np
    >>> A = np.array([[3, 0], [5, 1]])
    >>> B = np.array([[3, 5], [0, 1]])
    >>> prisoners_dilemma = nash.Game(A, B)
    >>> prisoners_dilemma
    Bi matrix game with payoff matrices:
    <BLANKLINE>
    Row player:
    [[3 0]
     [5 1]]
    <BLANKLINE>
    Column player:
    [[3 5]
     [0 1]]
