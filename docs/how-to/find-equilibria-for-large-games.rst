Find equilibria for large games
===============================

:code:`Nashpy` is not optimised for performance, if you would like to solve
large games you should take a look at
`gambit <https://github.com/gambitproject/gambit>`_. *However*, as each
algorithm implemented is a generator it is possible to find **a** Nash
equilibrium for large games at a low computational run time.

To illustrate this, let us create a 15 by 15 game::

    >>> import nash
    >>> import numpy as np
    >>> np.random.seed(0)
    >>> A = np.random.randint(-5, 5, (15, 15))
    >>> B = np.random.randint(-5, 5, (15, 15))
    >>> large_game = nash.Game(A, B)

Let us get the first equilibria found by :code:`Nashpy` when using
:ref:`support-enumeration`::

    >>> eq = next(large_game.support_enumeration())
    >>> eq
    (array([ 0.,  0.,  0.,  0.,  0.,  0.,  0.,  1.,  0.,  0.,  0.,  0.,  0.,
            0.,  0.]), array([ 0.,  0.,  0.,  0.,  0.,  0.,  1.,  0.,  0.,  0.,  0.,  0.,  0.,
            0.,  0.]))
