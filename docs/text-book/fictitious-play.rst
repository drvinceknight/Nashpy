.. _fictitious-play:

Fictitious play
================

The fictitious play algorithm implemented in :code:`Nashpy` is based on the
one described in [Fudenberg1998]_.

The algorithm is as follows:

For a game :math:`(A, B)\in\mathbb{R}^{m\times n}` define
:math:`\kappa_t^{i}:S^{-1}\to\mathbb{N}` to be a function that in a given time
interval :math:`t` for a player :math:`i` maps a strategy :math:`s` from the
opponent's strategy space :math:`S^{-1}` to a number of total times the opponent
has played :math:`s`.

Thus:

.. math::

   \kappa_t^{i}(s^{-i}) = \kappa_{t-1}(s^{-i}) + \begin{cases}
                                        1,& \text{ if }s^{-i}_{t-1}=s^{-i}\\
                                        0,& \text{ otherwise}
                                        \end{cases}

In practice:

.. math::

   \kappa_t^{1} \in \mathbb{Z}^{n}\qquad \kappa_t^{2} \in \mathbb{Z} ^ {m}


At stage :math:`t`, each player assumes their opponent is playing a mixed strategy
based on :math:`\kappa_{t-1}`:

.. math::

   \frac{\kappa_{t-1}}{\sum\kappa_{t-1}}

They calculate the expected value of each strategy, which is equivalent to:

.. math::

   s_{t}^{1}\in\text{argmax}_{s\in S_1}A\kappa_{t-1}^{2}\qquad s_{t}^{2}\in\text{argmax}_{s\in S_2}B^T\kappa_{t-1}^{1}

In the case of multiple best responses, a random choice is made.

Discussion
----------

Note that this algorithm will not always converge and sometimes it depends on
the form of the game.

For example::

    >>> import numpy as np
    >>> import nashpy as nash
    >>> A = np.array([[0, 1, 0], [0, 0, 1], [1, 0, 0]])
    >>> B = np.array([[0, 0, 1], [1, 0, 0], [0, 1, 0]])
    >>> game = nash.Game(A, B)
    >>> iterations = 10000
    >>> np.random.seed(0)
    >>> play_counts = tuple(game.fictitious_play(iterations=iterations))
    >>> play_counts[-1]
    [array([5464., 1436., 3100.]), array([2111., 4550., 3339.])]

We can visualise the lack of convergence::

    >>> import matplotlib.pyplot as plt
    >>> plt.figure() # doctest: +SKIP
    >>> probabilities = [row_play_counts / np.sum(row_play_counts) for row_play_counts, col_play_counts in play_counts]
    >>> for number, strategy in enumerate(zip(*probabilities)):
    ...     plt.plot(strategy, label=f"$s_{number}$")  # doctest: +SKIP
    >>> plt.xlabel("Iteration")  # doctest: +SKIP
    >>> plt.ylabel("Probability")  # doctest: +SKIP
    >>> plt.title("Actions taken by row player")  # doctest: +SKIP
    >>> plt.legend()  # doctest: +SKIP

.. image:: /_static/learning/fictitious_play/divergent_example/main.svg

If we modify the game slightly we obtain a different outcome::

    >>> A = np.array([[1 / 2, 1, 0], [0, 1 / 2, 1], [1, 0, 1 / 2]])
    >>> B = np.array([[1 / 2, 0, 1], [1, 1 / 2, 0], [0, 1, 1 / 2]])
    >>> game = nash.Game(A, B)
    >>> np.random.seed(0)
    >>> play_counts = tuple(game.fictitious_play(iterations=iterations))
    >>> play_counts[-1]
    [array([3290., 3320., 3390.]), array([3356., 3361., 3283.])]

With a clear convergence now visible::

    >>> import matplotlib.pyplot as plt
    >>> plt.figure() # doctest: +SKIP
    >>> probabilities = [row_play_counts / np.sum(row_play_counts) for row_play_counts, col_play_counts in play_counts]
    >>> for number, strategy in enumerate(zip(*probabilities)):
    ...     plt.plot(strategy, label=f"$s_{number}$")  # doctest: +SKIP
    >>> plt.xlabel("Iteration")  # doctest: +SKIP
    >>> plt.ylabel("Probability")  # doctest: +SKIP
    >>> plt.title("Actions taken by row player")  # doctest: +SKIP
    >>> plt.legend()  # doctest: +SKIP

.. image:: /_static/learning/fictitious_play/convergent_example/main.svg
