.. _how-to-use-moran_process_on_interaction_graph:

Use Moran processes on interaction graph
========================================

The Moran process method on the :code:`Game` class can take an
:code:`interaction_graph_adjacency_matrix` which defines the interaction graph
as described in [Ohtsuki2007]_::

    >>> import nashpy as nash
    >>> import numpy as np
    >>> A = np.array([[3, 1], [1, 2]])
    >>> game = nash.Game(A)

In this case, the :code:`moran_process` method returns a generator of a given
collection of generations where individuals interact if and only if they are
adjacent on the interaction graph (in the example below, the individuals are
placed on a cycle and only interact with the successive individuals except for
the last individual who interacts with everyone including themself)::

    >>> np.random.seed(0)
    >>> interaction_graph_adjacency_matrix = np.array(((0, 1, 0), (0, 0, 1), (1, 1, 1)))
    >>> generations = game.moran_process(initial_population=(0, 0, 1), interaction_graph_adjacency_matrix=interaction_graph_adjacency_matrix)
    >>> for population in generations:
    ...     print(population)
    [0 1 1]
    [0 1 1]
    [0 1 1]
    ...
    [0 1 1]
    [1 1 1]
