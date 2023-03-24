"""Code for implementation of a Moran process"""
import numpy as np
import numpy.typing as npt
import networkx as nx  # TODO Remove this as a dependency

from typing import Generator


def score_all_individuals(
    A: npt.NDArray,
    population: npt.NDArray,
    interaction_probability: array = None,  # Modify this to be the probability
                                            # Point out it corresponds to
                                            # adjacency matrix of...
                                            # Highlight need not be a stochastic
                                            # matrix
) -> npt.NDArray:
    """
    Return the scores of all individuals when they play against all other
    individuals in the population.

    Parameters
    ----------
    A : array
        a payoff matrix
    population : array
        the population
    interaction_graph : graph
        the interaction graph G: individuals of type i interact with individuals
        of type j count towards fitness iff G_{ij} = 1.
        Default is None: if so a complete graph is used -- this corresponds to
        all individuals interacting with each other.

    Returns
    -------
    array
        the scores of every player in the population

    Raises
    ------
    ValueError
        If the payoff matrix A has a negative value. Currently only
        non negative valued matrices are supported.

    """
    if np.min(A) < 0:
        raise ValueError(
            "Only non negative valued payoff matrices are currently supported"
        )

    if interaction_graph is None:
        population_size = len(population)
        interaction_graph = nx.complete_graph(population_size)

    scores = []

    for i, player in enumerate(population):
        total = 0
        for j, opponent in enumerate(population):
            if (i, j) in interaction_graph.edges:
                total += A[player, opponent]
        scores.append(total)

    return np.array(scores)


def update_population(
    population: npt.NDArray,
    scores: npt.NDArray,
    original_set_of_strategies: set,
    mutation_probability: float = 0,
    reproduction_graph: nx.Digraph = None,  # TODO Modify this to be an
                                            # stochastic matrix.
                                            # Note that it corresponds to
                                            # adjacency matrix of graph defined
                                            # in Nowak's Nature paper.
) -> npt.NDArray:
    """
    Return the new population of all individuals given the scores of every
    individual.

    Birth is selected proportionally to scores.
    Death is uniformly random.

    Parameters
    ----------
    population : array
        the population
    scores : array
        the scores
    original_set_of_strategies: set
        the set of the strategies present in the initial population
    mutation_probability : float
        the probability of an individual selected to be copied mutates to
        another individual from the original set of strategies (even if they are
        no longer present in the population).
    reproduction_stochastic_matrix : array
        

    Returns
    -------
    array
        the next population
    """
    N = len(population)
    next_population = np.array(population)
    probabilities = scores / np.sum(scores)

    try:
        birth_index = np.random.choice(range(N), p=probabilities)
    except ValueError:
        birth_index = np.random.choice(range(N))
    death_index = np.random.randint(N)  # TODO Modify this to use birth graph

    if (mutation_probability > 0) and (np.random.random() < mutation_probability):
        birth_strategy = np.random.choice(
            [n for n in original_set_of_strategies if n != birth_index]
        )
        next_population[death_index] = birth_strategy
    else:
        next_population[death_index] = next_population[birth_index]

    return next_population


def moran_process(
    A: npt.NDArray,
    initial_population: npt.NDArray,
    mutation_probability: float = 0,
) -> Generator[npt.NDArray, None, None]:
    """
    Return a generator of population across the Moran process. The last
    population is when only a single type of individual is present in the
    population.

    If an already fixed initial population is given then the generator will
    return that same initial population.

    Parameters
    ----------
    A : array
        a payoff matrix
    initial_population : array
        the initial population
    mutation_probability : float
        the probability of an individual selected to be copied mutates to
        another individual from the original set of strategies (even if they are
        no longer present in the population).


    Yields
    -------
    Generator
        The generations.
    """
    population = initial_population
    if len(set(population)) > 1:
        while (len(set(population)) != 1) or (mutation_probability > 0):
            scores = score_all_individuals(A=A, population=population)

            population = update_population(
                population=population,
                scores=scores,
                mutation_probability=mutation_probability,
                original_set_of_strategies=set(initial_population),
            )

            yield population
    else:
        yield population


def fixation_probabilities(
    A: npt.NDArray,
    initial_population: npt.NDArray,
    repetitions: int,
) -> npt.NDArray:
    """
    Return the fixation probabilities for all types of individuals.

    The returned array will have the same dimension as the number of rows or
    columns as the payoff matrix A. The ith element of the returned array
    corresponds to the probability that the ith strategy becomes fixed given the
    initial population.

    This is a stochastic algorithm and the probabilities are estimated over a
    number of repetitions.

    Parameters
    ----------
    A : array
        a payoff matrix
    initial_population : array
        the initial population
    repetitions : int
        The number of repetitions of the algorithm.


    Returns
    -------
    array
        The fixation probability of each type.
    """
    number_of_strategies = A.shape[0]
    fixation_counts = np.array([0 for _ in range(number_of_strategies)])
    for repetition in range(repetitions):
        generations = tuple(moran_process(A=A, initial_population=initial_population))
        last_population = generations[-1]

        assert len(set(last_population)) == 1
        fixed_strategy = last_population[0]

        fixation_counts[fixed_strategy] += 1

    return fixation_counts / repetitions
