Create a game
=============

A game in :code:`Nashpy` is created by passing 1 or 2 matrices to the
:code:`nash.Game` class. Here is the zero sum game `matching pennies
<https://en.wikipedia.org/wiki/Matching_pennies>`_::

    >>> import nash
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

Here is the **non** zero sum game `prisoners
dilemma <https://en.wikipedia.org/wiki/Prisoner%27s_dilemma>`_::

    >>> import nash
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
