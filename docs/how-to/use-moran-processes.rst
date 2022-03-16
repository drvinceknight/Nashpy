.. _how-to-use-moran_process:

Use Moran processes
===================

Moran processes are implemented in :code:`Nashpy` as a method on the
:code:`Game` class::

    >>> import nashpy as nash
    >>> import numpy as np
    >>> A = np.array([[3, 1], [1, 2]])
    >>> game = nash.Game(A)

The :code:`moran_process` method returns a generator of a given collection of
generations::

    >>> np.random.seed(0)
    >>> generations = game.moran_process(initial_population=(0, 0, 1))
    >>> for population in generations:
    ...     print(population)
    [0 0 1]
    [0 1 1]
    [0 1 1]
    ...
    [0 1 1]
    [1 1 1]

Note that this process is stochastic::

    >>> np.random.seed(2)
    >>> generations = game.moran_process(initial_population=(0, 0, 1))
    >>> for population in generations:
    ...     print(population)
    [0 0 1]
    [0 0 1]
    [0 0 0]

It is possible to pass a :code:`mutation_probability` to the process in
which case it will not terminate::

    >>> np.random.seed(2)
    >>> number_of_generations = 5
    >>> mutation_probability = 1
    >>> generations = game.moran_process(initial_population=(0, 0, 1), mutation_probability=mutation_probability)
    >>> for _ in range(number_of_generations):
    ...     print(next(generations))
    [0 0 1]
    [1 0 1]
    [1 1 1]
    [0 1 1]
    [0 1 0]

def test_update_population_with_mutation_probability_1_over_2_seed_2():
    population = np.array((0, 0, 0, 1, 1, 2, 2))
    scores = np.array((18, 18, 18, 15, 15, 23, 23))
    mutation_probability = 1 / 2
    expected_new_population = np.array((0, 0, 0, 1, 1, 1, 2))

    np.random.seed(2)
    new_population = update_population(
        population=population, scores=scores, mutation_probability=mutation_probability
    )
    new_population
    assert np.array_equal(expected_new_population, new_population)

def test_update_population_with_mutation_probability_1_over_2_seed_2():
    population = np.array((0, 0, 0, 1, 1, 2, 2))
    scores = np.array((18, 18, 18, 15, 15, 23, 23))
    mutation_probability = 1 / 2
    expected_new_population = np.array((0, 0, 0, 1, 1, 1, 2))

    np.random.seed(2)
    new_population = update_population(
        population=population, scores=scores, mutation_probability=mutation_probability
    )
    new_population
    assert np.array_equal(expected_new_population, new_population)

def test_update_population_with_mutation_probability_1_over_2_seed_2():
    population = np.array((0, 0, 0, 1, 1, 2, 2))
    scores = np.array((18, 18, 18, 15, 15, 23, 23))
    mutation_probability = 1 / 2
    expected_new_population = np.array((0, 0, 0, 1, 1, 1, 2))

    np.random.seed(2)
    new_population = update_population(
        population=population, scores=scores, mutation_probability=mutation_probability
    )
    new_population
    assert np.array_equal(expected_new_population, new_population)

Currently, only positive valued matrices are supported::

    >>> A = np.array([[3, 0], [1, 2]])
    >>> game = nash.Game(A)
    >>> generations = game.moran_process(initial_population=(0, 0, 1))
    >>> for population in generations:
    ...     print(population)
    Traceback (most recent call last):
     ...
    ValueError: Only positive valued payoff matrices are currently supported
