.. _degenerate-games-discussion:

Handle Degenerate games
=======================

When dealing with *degenerate* games unexpected results can occur::

    >>> import nashpy as nash
    >>> import numpy as np
    >>> A = np.array([[0, -1, 1], [-1, 0, 1], [-1, 0, 1]])
    >>> game = nash.Game(A)

Here is the output when using :ref:`support-enumeration-discussion`::

    >>> for eq in game.support_enumeration():
    ...     print(np.round(eq[0], 2), np.round(eq[1], 2))
    [0.5 0.5 0. ] [0.5 0.5 0. ]
    [0.5 0.  0.5] [0.5 0.5 0. ]

Here is the output when using :ref:`vertex-enumeration`::

    >>> for eq in game.vertex_enumeration(): # doctest: +SKIP
    ...     print(np.round(eq[0], 2), np.round(eq[1], 2))
    [0.5 0.  0.5] [ 0.5  0.5 -0. ]
    [ 0.5  0.5 -0. ] [ 0.5  0.5 -0. ]


Here is the output when using the :ref:`lemke-howson`::

    >>> for eq in game.lemke_howson_enumeration():  # doctest: +SKIP
    ...     print(np.round(eq[0], 2), np.round(eq[1], 2))
    [0.33... 0.33... 0.33...] [nan]


We see that the `lemke-howson` algorithm fails but also that the
:ref:`support-enumeration-discussion` and :ref:`vertex-enumeration` fail to find some
equilibria: there is in fact a range of strategies the row player can play
against :code:`[ 0.5 0.5 0]` that is still a best response.

When the indifference system for a support pair is singular, support
enumeration also returns the extreme points of that Nash component. For
example the degenerate game from
https://github.com/drvinceknight/Nashpy/issues/222 has equilibria
:math:`([p, 1-p], [1, 0])` for all :math:`p \in [0, 2/7]`. The algorithm
returns both endpoints::

    >>> A = np.array([[-3, 3], [-3, 5]])
    >>> B = np.array([[2, 7], [4, 2]])
    >>> game = nash.Game(A, B)
    >>> for eq in game.support_enumeration():  # doctest: +ELLIPSIS
    ...     print(np.round(eq[0], 2), np.round(eq[1], 2))
    [0. 1.] [1. 0.]
    [0.29 0.71] [1. 0.]

The :ref:`support-enumeration-discussion` algorithm can be run with two optional
arguments:

- :code:`non_degenerate=True` (:code:`False` is the default) will only consider
  supports of equal size. If you know your game is non degenerate this will make
  support enumeration make less checks.
- :code:`tol=0` (:code:`10 ** -16` is the default), when considering the
  underlying linear system :code:`tol` is considered to be a lower bound for
  difference between two real numbers. Using :code:`tol=0` ensures a strict
  run of the algorithm.
