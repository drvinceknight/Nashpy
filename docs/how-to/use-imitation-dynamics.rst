.. _how-to-use-imitation-dynamics:

Use Imitation Dynamics
======================

Imitation dynamics is implemented as a method on the :code:`Game` class. For
example, consider a rectangular game in which the row player has two strategies
and the column player has three::

    >>> import nashpy as nash
    >>> import numpy as np
    >>> A = np.array([[3, 0, 1], [1, 2, 4]])
    >>> B = np.array([[2, 5, 0], [3, 1, 4]])
    >>> game = nash.Game(A, B)

The :code:`imitation_dynamics` method returns a generator containing one pair
of final thresholded population profiles::

    >>> profiles = game.imitation_dynamics(
    ...     population_size=5,
    ...     iterations=2,
    ...     threshold=.4,
    ...     seed=0,
    ... )
    >>> row_profile, column_profile = next(profiles)
    >>> row_profile
    array([0., 1.])
    >>> column_profile
    array([0., 1., 1.])

Passing a :code:`seed` makes the random initialization reproducible without
changing NumPy's global random state::

    >>> first = next(game.imitation_dynamics(population_size=5, seed=0))
    >>> second = next(game.imitation_dynamics(population_size=5, seed=0))
    >>> all(np.array_equal(x, y) for x, y in zip(first, second))
    True

The older :code:`random_seed` parameter remains available as an alias for
:code:`seed`. Supplying both parameters raises a :code:`ValueError`.

The returned binary profiles describe the thresholded final populations. They
are not necessarily probability distributions or Nash equilibria.
