.. _stochastic-fictitious-play:

Stochastic fictitious play
==========================

The stochastic fictitious play algorithm implemented in :code:`Nashpy` is based on the
one given in [Hofbauer2002]_.

As explained in [Fudenberg1998]_ stochastic fictitious play "avoids the discontinuity inherent
in standard fictitious play, where a small change in the data can lead to an abrupt change in
behaviour."

The algorithm is designed to converge in cases where fictitious play does not
converge. Note that in some cases this will require a thoughtful choice of the :code:`etha`
and :code:`epsilon_bar` parameters.

For a game :math:`(A, B)\in\mathbb{R}^{m\times n}` define
:math:`\kappa_t^{i}:S^{-1}\to\mathbb{N}` to be a function that in a given time
interval :math:`t` for a player :math:`i` maps a strategy :math:`s` from the
opponent's strategy space :math:`S^{-1}` to a number of total times the opponent
has played :math:`s`.

As per standard :ref:`fictitious-play`, each player assumes their opponent is playing a mixed strategy
based on :math:`\kappa_{t-1}`. If no play has taken place, then the probability of playing each
action is assumed to be equal. The assumed mixed strategies of a player's opponent are multplied
by the player's own payoff matrices to calculate the expected payoff of each action.

A stochastic pertubation :math:`\epsilon_i` is added to each expected payoff :math:`\pi_i` to give a
pertubated payoff.  Each :math:`\epsilon_i` is independent of each :math:`\pi_i` and is a random number
between 0 and :code:`epsilon_bar`.

A logit choice function is used to map the pertubated payoff to a non-negative probability distribution,
corresponding to the probability with which each strategy is chosen by the player. The logit choice function
can be seen below:

.. math::

    L_i( \pi ) = \frac{\exp (\eta ^{-1} \pi_i )}{\sum_{j}\exp (\eta ^{-1} \pi_j)}

Discussion
----------

Using the same game from the fictitious play discussion section, we can visualise a lack of convergence when
using the default value of :code:`epsilon_bar`::

    >>> import numpy as np
    >>> import nashpy as nash
    >>> A = np.array([[0, 1, 0], [0, 0, 1], [1, 0, 0]])
    >>> B = np.array([[0, 0, 1], [1, 0, 0], [0, 1, 0]])
    >>> game = nash.Game(A, B)
    >>> iterations = 10000
    >>> np.random.seed(0)
    >>> play_counts_and_distribuions = tuple(game.stochastic_fictitious_play(iterations=iterations))
    >>> play_counts, distributions = play_counts_and_distribuions[-1]
    >>> print(play_counts)
    [array([3937., 1907., 4156.]), array([2823., 5458., 1719.])]

    >>> import matplotlib.pyplot as plt
    >>> plt.figure() # doctest: +SKIP
    >>> probabilities = [
    ...     row_play_counts / np.sum(row_play_counts)
    ...     if np.sum(row_play_counts) != 0
    ...     else row_play_counts + 1 / len(row_play_counts)
    ...     for (row_play_counts, col_play_counts), _ in play_counts_and_distribuions]
    >>> for number, strategy in enumerate(zip(*probabilities)):
    ...     plt.plot(strategy, label=f"$s_{number}$") # doctest: +SKIP
    >>> plt.xlabel("Iteration") # doctest: +SKIP
    >>> plt.ylabel("Probability") # doctest: +SKIP
    >>> plt.title("Actions taken by row player") # doctest: +SKIP
    >>> plt.legend() # doctest: +SKIP

.. image:: /_static/learning/stochastic_fictitious_play/divergent_example/main.svg

Observe below that the game converges when passing values for :code:`etha` and :code:`epsilon_bar`::

    >>> A = np.array([[1 / 2, 1, 0], [0, 1 / 2, 1], [1, 0, 1 / 2]])
    >>> B = np.array([[1 / 2, 0, 1], [1, 1 / 2, 0], [0, 1, 1 / 2]])
    >>> game = nash.Game(A, B)
    >>> iterations = 10000
    >>> etha = 0.1
    >>> epsilon_bar = 10**-1
    >>> np.random.seed(0)
    >>> play_counts_and_distribuions = tuple(game.stochastic_fictitious_play(iterations=iterations, etha=etha, epsilon_bar=epsilon_bar))
    >>> play_counts_and_distribuions[-1]
    ([array([3300., 3293., 3407.]), array([3320., 3372., 3308.])], [array([0.33502382, 0.41533594, 0.24964024]), array([0.18890743, 0.42793694, 0.38315563])])
    >>> import matplotlib.pyplot as plt
    >>> plt.figure() # doctest: +SKIP
    >>> probabilities = [
    ...     row_play_counts / np.sum(row_play_counts)
    ...     if np.sum(row_play_counts) != 0
    ...     else row_play_counts + 1 / len(row_play_counts)
    ...     for (row_play_counts, col_play_counts), _ in play_counts_and_distribuions]
    >>> for number, strategy in enumerate(zip(*probabilities)):
    ...     plt.plot(strategy, label=f"$s_{number}$") # doctest: +SKIP
    >>> plt.xlabel("Iteration") # doctest: +SKIP
    >>> plt.ylabel("Probability") # doctest: +SKIP
    >>> plt.title("Actions taken by row player") # doctest: +SKIP
    >>> plt.legend() # doctest: +SKIP

.. image:: /_static/learning/stochastic_fictitious_play/convergent_example/main.svg




