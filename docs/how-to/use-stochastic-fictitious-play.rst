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

    >>> np.random.seed(0)
    >>> iterations = 500
    >>> play_counts_and_distributions = game.stochastic_fictitious_play(iterations=iterations)
    >>> for play_counts, distributions in play_counts_and_distributions:
    ...     row_play_counts, column_play_counts = play_counts
    ...     row_distributions, column_distributions = distributions
    ...     print(row_play_counts, column_play_counts, row_distributions, column_distributions)
    [0 0] [0 0] None None
    [1. 0.] [0. 1.] [9.99953841e-01 4.61594628e-05] [0.501447 0.498553]
    ...
    [498.   1.] [497.   2.] [1.00000000e+00 1.07557011e-13] [9.99999998e-01 2.32299935e-09]
    [499.   1.] [498.   2.] [1.00000000e+00 1.17304491e-13] [9.99999998e-01 2.18403537e-09]

Note that this process is stochastic::

    >>> np.random.seed(1)
    >>> play_counts_and_distributions = game.stochastic_fictitious_play(iterations=iterations)
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

    >>> np.random.seed(0)
    >>> play_counts = (np.array([0., 500.]), np.array([0., 500.]))
    >>> play_counts_and_distributions = game.stochastic_fictitious_play(iterations=iterations, play_counts=play_counts)
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

    >>> np.random.seed(0)
    >>> etha = 10**-2
    >>> epsilon_bar = 10**-3
    >>> play_counts_and_distributions = game.stochastic_fictitious_play(iterations=iterations, etha=etha, epsilon_bar=epsilon_bar)
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


Note that for some large valued input matrices a numerical error can occur::

    >>> A = np.array([[113, 65, 112], [141, 93, -56], [120, 73, -76]])
    >>> B = np.array([[-113, -65, -112], [-141, -93, 56], [-120, -73, 76]])
    >>> game = nash.Game(A, B)
    >>> iterations = 500
    >>> play_counts_and_distributions = tuple(game.stochastic_fictitious_play(iterations=iterations))
    Traceback (most recent call last):
    ...
    ValueError: The matrix with values ranging from -76 to 141...

This can usually addressed by an affine scaling of the matrices::

    >>> A = A / 10
    >>> B = B / 10
    >>> game = nash.Game(A, B)
    >>> play_counts_and_distributions = game.stochastic_fictitious_play(iterations=iterations, etha=etha, epsilon_bar=epsilon_bar)
