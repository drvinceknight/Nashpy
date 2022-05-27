.. _how-to-use-replicator-dynamics-with-mutation:

Use replicator dynamics with mutation
=====================================

Given a matrix :math:`Q` such that :math:`Q_{ij}` gives the probability that an
individual of type `i` mutates to an individual of type `j`, the replicator
dynamics equation with mutation can be solved using the following::

    >>> import nashpy as nash
    >>> import numpy as np
    >>> A = np.array([[3, 2], [4, 2]])
    >>> Q = np.array([[9 / 10,  1 / 10], [1 / 5, 4 / 5]])
    >>> game = nash.Game(A)
    >>> game.replicator_dynamics(mutation_matrix=Q)
    array([[0.5       , 0.5       ],
           [0.50049813, 0.49950187],
           [0.50099155, 0.49900845],
           ...,
           [0.55278206, 0.44721794],
           [0.5527821 , 0.4472179 ],
           [0.55278214, 0.44721786]])
