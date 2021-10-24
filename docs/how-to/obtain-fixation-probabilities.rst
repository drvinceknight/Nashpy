Obtain fixation probabilities
=============================

Using the implemented `Moran process <how-to-use-moran_process>` the fixation
probabilities can be approximated using a method on the :code:`Game` class::

    >>> import nashpy as nash
    >>> import numpy as np
    >>> A = np.array([[3, 1], [1, 2]])
    >>> game = nash.Game(A)

The :code:`fixation` method returns an array with the fixation probabilities of
each strategy given the initial population::

    >>> np.random.seed(0)
    >>> probabilities = game.fixation_probabilities(initial_population=(0, 1, 1, 1), iterations=200)
    >>> probabilities
    array([0.235, 0.765])

This above shows that approximately (estimated over 200 iterations) 23.5 % of
the time the first strategy will take over a population with a total of 4
individuals (when the initial population begins with 3 individuals of the other
type).
