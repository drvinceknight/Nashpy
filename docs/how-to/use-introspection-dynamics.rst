.. _how-to-use-introspection-dynamics:

Use Introspection Dynamics
==========================

Introspection dynamics is implemented in :code:`Nashpy` as a method on the
:code:`Game` class::

    >>> import nashpy as nash
    >>> import numpy as np
    >>> A = np.array([[3, 1], [1, 2]])
    >>> B = np.array([[3, 6], [5, 2]])
    >>> game = nash.Game(A, B)

The :code:`introspection_dynamics` method returns a generator of a given collection of
generations::

    >>> np.random.seed(0)
    >>> steps = game.introspection_dynamics(number_of_iterations=50, beta=.2)
    >>> for actions in steps:
    ...     print(actions)
    [0 1]
    [0 1]
    [0 1]
    ...
    [1 1]
    [1 0]
    [1 1]

Note that this process is stochastic::

    >>> np.random.seed(2)
    >>> steps = game.introspection_dynamics(number_of_iterations=50, beta=.2)
    >>> for actions in steps:
    ...     print(actions)
    [0 1]
    [0 1]
    [0 1]
    ...
    [0 1]
    [0 1]
    [0 1]

Calculate the long-run state distribution
-----------------------------------------

To calculate the long-run probability of every action pair without simulating
a trajectory, use :code:`introspection_dynamics_state_distribution`::

    >>> distribution = game.introspection_dynamics_state_distribution(beta=.2)
    >>> np.round(distribution, 4)
    array([[0.2404, 0.283 ],
           [0.2528, 0.2238]])

The entry at :code:`distribution[i, j]` is the probability that the row player
chooses action :code:`i` and the column player chooses action :code:`j`. The
entries sum to one. Obtain each player's marginal action probabilities by
summing over the other player's actions::

    >>> np.round(distribution.sum(axis=1), 4)  # Row player's actions
    array([0.5234, 0.4766])
    >>> np.round(distribution.sum(axis=0), 4)  # Column player's actions
    array([0.4932, 0.5068])

With zero learning intensity, all action pairs are equally likely::

    >>> game.introspection_dynamics_state_distribution(beta=0)
    array([[0.25, 0.25],
           [0.25, 0.25]])

This is a joint stationary distribution of the learning process; its marginals
need not form a Nash equilibrium. The calculation requires finite payoff matrices,
at least two actions per player and a finite, non-negative :code:`beta`.
It stores a dense matrix with one row and column per action pair, so it is
intended for small games. Very large scaled payoff differences can cause
transition probabilities to underflow; in that case the method can raise
:code:`numpy.linalg.LinAlgError`.
