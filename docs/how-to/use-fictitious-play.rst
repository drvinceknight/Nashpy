Use fictitious play
===================

One of the learning algorithms implemented in :code:`Nashpy` is called
:ref:`fictitious-play`, this is implemented as a method on the :code:`Game`
class::

    >>> import nashpy as nash
    >>> import numpy as np
    >>> A = np.array([[3, 1], [0, 2]])
    >>> B = np.array([[2, 0], [1, 3]])
    >>> game = nash.Game(A, B)

The :code:`fictitious_play` method returns a generator of a given collection of
learning steps::

    >>> np.random.seed(0)
    >>> iterations = 500
    >>> play_counts = game.fictitious_play(iterations=iterations)
    >>> for row_play_counts, column_play_counts in play_counts:
    ...     print(row_play_counts, column_play_counts)
    [0 0] [0 0]
    [1. 0.] [0. 1.]
    ...
    [498.   1.] [497.   2.]
    [499.   1.] [498.   2.]

Note that this process is stochastic::

    >>> np.random.seed(1)
    >>> play_counts = game.fictitious_play(iterations=iterations)
    >>> for row_play_counts, column_play_counts in play_counts:
    ...     print(row_play_counts, column_play_counts)
    [0 0] [0 0]
    [0. 1.] [0. 1.]
    ...
    [  0. 499.] [  0. 499.]
    [  0. 500.] [  0. 500.]

It is also possible to pass a :code:`play_counts` variable to give a starting
point for the algorithm::

    >>> np.random.seed(1)
    >>> play_counts = (np.array([0., 500.]), np.array([0., 500.]))
    >>> play_counts = game.fictitious_play(iterations=iterations, play_counts=play_counts)
    >>> for row_play_counts, column_play_counts in play_counts:
    ...     print(row_play_counts, column_play_counts)
    [  0. 500.] [  0. 500.]
    [  0. 501.] [  0. 501.]
    ...
    [  0. 999.] [  0. 999.]
    [   0. 1000.] [   0. 1000.]
