.. _how-to-obtain-fixation-probabilities:

Obtain fixation probabilities
=============================

Using the implemented `Moran process <how-to-use-moran_process>` the fixation
probabilities can be approximated using a method on the :code:`Game` class::

    >>> import nashpy as nash
    >>> import numpy as np
    >>> A = np.array([[3, 1], [1, 2]])
    >>> game = nash.Game(A)

The :code:`fixation` method returns a dictionary mapping the final states to the probabilities::

    >>> np.random.seed(0)
    >>> probabilities = game.fixation_probabilities(initial_population=(0, 1, 1, 1), repetitions=200)
    >>> probabilities
    {(1, 1, 1, 1): 0.765, (0, 0, 0, 0): 0.235}

This above shows that approximately (estimated over 200 iterations) 23.5 % of
the time the first strategy will take over a population with a total of 4
individuals (when the initial population begins with 3 individuals of the other
type).
