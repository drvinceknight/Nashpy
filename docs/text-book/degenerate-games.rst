.. _degenerate-games-discussion:

Degenerate games
================

A two player game is called nondegenerate if no mixed strategy of support size
:math:`k` has more than :math:`k` pure best responses.

For example, the zero sum game defined by the following matrix is degenerate:

.. math::

   A =
   \begin{pmatrix}
        0 & -1 &  1\\
       -1 &  0 &  1\\
       -1 &  1 &  0
   \end{pmatrix}

The third column has two pure best responses.

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

The :ref:`support-enumeration-discussion` algorithm can be run with two optional
arguments:

- :code:`non_degenerate=True` (:code:`False` is the default) will only consider
  supports of equal size. If you know your game is non degenerate this will make
  support enumeration make less checks.
- :code:`tol=0` (:code:`10 ** -16` is the default), when considering the
  underlying linear system :code:`tol` is considered to be a lower bound for
  difference between two real numbers. Using :code:`tol=0` ensures a strict
  run of the algorithm.

Here is an example::

    >>> A = np.array([[4, 9, 9], [9, 1, 6], [9, 2, 3]])
    >>> B = np.array([[2, 2, 5], [7, 4, 4], [1, 6, 4]])
    >>> game = nash.Game(A, B)
    >>> for eq in game.support_enumeration():
    ...     print(np.round(eq[0], 2), np.round(eq[1], 2))
    [1. 0. 0.] [0. 0. 1.]
    [0. 1. 0.] [1. 0. 0.]
    [0.5 0.5 0. ] [0.38 0.   0.62]
    [0.2 0.5 0.3] [0.57 0.32 0.11]
    >>> for eq in game.support_enumeration(non_degenerate=True):
    ...     print(np.round(eq[0], 2), np.round(eq[1], 2))
    [1. 0. 0.] [0. 0. 1.]
    [0. 1. 0.] [1. 0. 0.]
    [0.2 0.5 0.3] [0.57 0.32 0.11]
    >>> for eq in game.support_enumeration(non_degenerate=False, tol=0):
    ...     print(np.round(eq[0], 2), np.round(eq[1], 2))
    [1. 0. 0.] [0. 0. 1.]
    [0. 1. 0.] [1. 0. 0.]
    [0.2 0.5 0.3] [0.57 0.32 0.11]
