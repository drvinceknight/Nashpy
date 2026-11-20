Use stochastic fictitious play
==============================

One of the learning algorithms implemented in :code:`Nashpy` is called
:ref:`stochastic-fictitious-play`, this is implemented as a method on the :code:`Game`
class::

    >>> import nashpy as nash
    >>> import numpy as np
    >>> A = np.array([[3, 1], [0, 2]])
    >>> B = np.array([[2, 0], [1, 3]])
    >>> game = nash.Game(A, B)

The :code:`stochastic_fictitious_play` method returns a generator of a given collection of
learning steps, comprising of the play counts and the mixed strategy of each player::

    >>> iterations = 500
    >>> play_counts_and_distributions = game.stochastic_fictitious_play(iterations=iterations, seed=0)
    >>> for play_counts, distributions in play_counts_and_distributions:
    ...     row_play_counts, column_play_counts = play_counts
    ...     row_distributions, column_distributions = distributions
    ...     print(row_play_counts, column_play_counts, row_distributions, column_distributions)
    [0 0] [0 0] None None
    [1. 0.] [0. 1.] [9.99956239e-01 4.37612752e-05] [0.50061115 0.49938885]
    ...
    [498.   1.] [497.   2.] [1.00000000e+00 1.09702646e-13] [9.99999998e-01 2.18218160e-09]
    [499.   1.] [498.   2.] [1.0000000e+00 1.0116217e-13] [9.99999998e-01 2.07111668e-09]

Note that this process is stochastic::

    >>> play_counts_and_distributions = game.stochastic_fictitious_play(iterations=iterations, seed=1)
    >>> for play_counts, distributions in play_counts_and_distributions:
    ...     row_play_counts, column_play_counts = play_counts
    ...     row_distributions, column_distributions = distributions
    ...     print(row_play_counts, column_play_counts)
    [0 0] [0 0]
    [1. 0.] [1. 0.]
    ...
    [499.   0.] [499.   0.]
    [500.   0.] [500.   0.]

It is also possible to pass a :code:`play_counts` variable to give a starting
point for the algorithm::

    >>> play_counts = (np.array([0., 500.]), np.array([0., 500.]))
    >>> play_counts_and_distributions = game.stochastic_fictitious_play(iterations=iterations, seed=0, play_counts=play_counts)
    >>> for play_counts, distributions in play_counts_and_distributions:
    ...     row_play_counts, column_play_counts = play_counts
    ...     row_distributions, column_distributions = distributions
    ...     print(row_play_counts, column_play_counts)
    ...
    [  0. 500.] [  0. 500.]
    [  0. 501.] [  0. 501.]
    ...
    [  0. 999.] [  0. 999.]
    [   0. 1000.] [   0. 1000.]

A value of :code:`etha` and :code:`epsilon_bar` can be passed.
See the :ref:`stochastic-fictitious-play` reference section for more information. The default values for etha and epsilon bar are
:math:`10^-1` and :math:`10^-2` respectively::

    >>> etha = 10**-2
    >>> epsilon_bar = 10**-3
    >>> play_counts_and_distributions = game.stochastic_fictitious_play(iterations=iterations, seed=0, etha=etha, epsilon_bar=epsilon_bar)
    >>> for play_counts, distributions in play_counts_and_distributions:
    ...     row_play_counts, column_play_counts = play_counts
    ...     row_distributions, column_distributions = distributions
    ...     print(row_play_counts, column_play_counts)
    ...
    [0 0] [0 0]
    [1. 0.] [0. 1.]
    ...
    [498.   1.] [497.   2.]
    [499.   1.] [498.   2.]


Logit probabilities are evaluated using a common shift of the scaled utilities,
so large payoffs do not overflow their exponentials::

    >>> A = np.array([[113, 65, 112], [141, 93, -56], [120, 73, -76]])
    >>> B = np.array([[-113, -65, -112], [-141, -93, 56], [-120, -73, 76]])
    >>> game = nash.Game(A, B)
    >>> iterations = 500
    >>> play_counts_and_distributions = tuple(game.stochastic_fictitious_play(iterations=iterations, seed=0))
    >>> len(play_counts_and_distributions)
    501
    >>> all(np.all(np.isfinite(distribution)) for _, distributions in play_counts_and_distributions[1:] for distribution in distributions)
    True

The common shift leaves the probabilities unchanged. Rescaling the payoff
matrices instead changes the strength of the logit response when :code:`etha`
is held fixed, so it is not needed as a workaround for exponential overflow.
