.. _how-to-obtain-a-repeated-game:

Obtain a repeated game
======================

Given a game in :code:`Nashpy` it is possible to create a new game by repeating
it as described in :ref:`repeated-games-discussion`::

    >>> import nashpy as nash
    >>> import nashpy.repeated_games
    >>> import numpy as np
    >>> A = np.array([[1, -1], [-1, 1]])
    >>> matching_pennies = nash.Game(A)
    >>> repeated_matching_pennies = nash.repeated_games.obtain_repeated_game(game=matching_pennies, repetitions=2)
    >>> repeated_matching_pennies
    Zero sum game with payoff matrices:
    <BLANKLINE>
    Row player:
    [[ 2.  2.  2. ...  0. -2. -2.]
     [ 2.  2.  2. ...  0. -2. -2.]
     [ 2.  2.  2. ...  0. -2. -2.]
     ...
     [ 0.  0.  0. ...  2.  0.  2.]
     [-2. -2. -2. ...  0.  2.  0.]
     [-2. -2. -2. ...  2.  0.  2.]]
    <BLANKLINE>
    Column player:
    [[-2. -2. -2. ...  0.  2.  2.]
     [-2. -2. -2. ...  0.  2.  2.]
     [-2. -2. -2. ...  0.  2.  2.]
     ...
     [ 0.  0.  0. ... -2.  0. -2.]
     [ 2.  2.  2. ...  0. -2.  0.]
     [ 2.  2.  2. ... -2.  0. -2.]]

Note, that these games can become large even for small values of
:code:`repetitions`. The above game has payoff matrices with size::

    >>> repeated_matching_pennies.payoff_matrices[0].shape
    (32, 32)

When studying these large games direct computation of equilibria is unlikely to
be computationally efficient. Instead learning algorithms should be used.

It is also to directly obtain a generator containing the strategies, :ref:`which
are mapping from histories of play to
actions<definition-of-strategies-in-repeated-games>`::

    >>> strategies = nash.repeated_games.obtain_strategy_space(A=A, repetitions=2)
    >>> next(strategies)
    {((), ()): (1.0, 0.0), ((0,), (0,)): (1.0, 0.0), ((0,), (1,)): (1.0, 0.0), ((1,), (0,)): (1.0, 0.0), ((1,), (1,)): (1.0, 0.0)}
