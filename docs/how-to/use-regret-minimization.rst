.. _how-to-use-regret-minimization:

Use Regret Minimization
=======================

Use :code:`Game.regret_minimization` to obtain average mixed strategies through
cumulative regret matching. Both players start uniformly and use expected
utilities, so no random seed is needed.

For example, create a rectangular bimatrix game::

    >>> import nashpy as nash
    >>> import numpy as np
    >>> A = np.array([[3, 0, 1], [1, 2, 4]])
    >>> B = np.array([[2, 5, 0], [3, 1, 4]])
    >>> game = nash.Game(A, B)

The method returns a generator yielding exactly one pair of NumPy arrays after
all rounds. Each array contains average action probabilities, with one entry
per strategy of that player::

    >>> results = list(game.regret_minimization(iterations=2))
    >>> len(results)
    1
    >>> row_strategy, column_strategy = results[0]
    >>> row_strategy
    array([0.25, 0.75])
    >>> np.round(column_strategy, 6)
    array([0.166667, 0.666667, 0.166667])
    >>> bool(np.isclose(row_strategy.sum(), 1))
    True
    >>> bool(np.isclose(column_strategy.sum(), 1))
    True

An iteration is a round played with the current strategies, followed by a
simultaneous regret update. The average includes the initial uniform profile
and excludes the unplayed update after the last round. Thus one round returns
the uniform profile. Zero rounds also returns the uniform profile by convention::

    >>> row_strategy, column_strategy = next(game.regret_minimization(iterations=0))
    >>> row_strategy
    array([0.5, 0.5])
    >>> np.allclose(column_strategy, [1 / 3] * 3)
    True

Approximating a zero-sum equilibrium
------------------------------------

For zero-sum games, increasing the number of rounds makes the average strategies
approach the set of Nash equilibria. A finite run is an approximation, and
general bimatrix games do not have the same guarantee.

Here the exact zero-sum equilibrium is :math:`(1/4, 3/4)` for both players.
The duality gap is the sum of the two players' possible payoff gains from
unilateral best responses. It measures how far the pair is from equilibrium::

    >>> A = np.array([[3, 0], [0, 1]])
    >>> game = nash.Game(A)
    >>> row_strategy, column_strategy = next(game.regret_minimization(iterations=5000))
    >>> gap = np.max(A @ column_strategy) - np.min(row_strategy @ A)
    >>> bool(gap < 0.05)
    True

See :ref:`regret-minimization` for the update equations and convergence details.

Migrating existing calls
------------------------

Earlier versions returned lists that put all probability on the most likely
final actions. The generator now yields NumPy arrays containing the average
probability of each action across the played rounds.

To migrate a call such as :code:`game.regret_minimization(0.1, 100)`, use
:code:`game.regret_minimization(iterations=100)`. The first positional slot
still accepts :code:`learning_rate` for compatibility. Any value other than
:code:`None` is ignored and emits :code:`DeprecationWarning` when the generator
is advanced. The default is 100 rounds.
