"""Code for implementation of a Moran process"""

import numpy as np
import numpy.typing as npt
import networkx as nx

from typing import Optional, Generator, Dict, Tuple


def get_complete_graph_adjacency_matrix(population: npt.NDArray) -> npt.NDArray:
    """
    Return the adjacency matrix for the complete graph on a population.

    Parameters
    ----------
    population : npt.NDArray
        The number of nodes

    Returns
    -------
    array
        the adjacency matrix for the complete graph on N nodes.
    """
    population_size = len(population)
    interaction_graph_adjacency_matrix = (np.eye(population_size) + 1) % 2
    return interaction_graph_adjacency_matrix


def score_all_individuals(
    A: npt.NDArray,
    population: npt.NDArray,
    interaction_graph_adjacency_matrix: Optional[npt.NDArray] = None,
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
    interaction_graph_adjacency_matrix : array
        the adjacency matrix for the interaction graph G: individuals of type i
        interact with individuals of type j count towards fitness iff G_{ij} =
        1.  Default is None: if so a complete graph is used -- this corresponds
        to all individuals interacting with each other (with no self
        interactions)

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

    if interaction_graph_adjacency_matrix is None:
        interaction_graph_adjacency_matrix = get_complete_graph_adjacency_matrix(
            population=population
        )

    scores = []

    for i, player in enumerate(population):
        total = 0
        for j, opponent in enumerate(population):
            if interaction_graph_adjacency_matrix[i, j] == 1:
                total += A[player, opponent]
        scores.append(total)

    return np.array(scores)


def update_population(
    population: npt.NDArray,
    scores: npt.NDArray,
    original_set_of_strategies: set,
    mutation_probability: float = 0,
    replacement_stochastic_matrix: Optional[npt.NDArray] = None,
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
    replacement_stochastic_matrix: array
        Individual i chosen for replacement will replace individual j with
        probability P_{ij}.
        Default is None: this is equivalent to P_{ij} = 1 / N for all i, j.

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

    if replacement_stochastic_matrix is None:
        death_index = np.random.randint(N)
    else:
        death_index = np.random.choice(
            range(N),
            p=replacement_stochastic_matrix[birth_index],
        )

    if (mutation_probability > 0) and (np.random.random() < mutation_probability):
        birth_strategy = np.random.choice(
            [n for n in original_set_of_strategies if n != birth_index]
        )
        next_population[death_index] = birth_strategy
    else:
        next_population[death_index] = next_population[birth_index]

    return next_population


def is_population_not_fixed(
    population: npt.NDArray,
    population_components: Tuple,
) -> bool:
    """
    Given a population vector and a set of population connected components this
    returns a boolean indicating if all individuals in each component are of the
    same type.
    This is used to check for fixation when using a replacement graph that may
    be disconnected.

    Parameters
    ----------
    population : array
        the population
    population_components : Tuple
        a tuple of sets containing node indices. Each set corresponds to a set
        of connected components.

    Returns
    -------
    bool
        True if the population is not yet fixed. True if the population is
        fixed (all individuals in all connected components have the same type).
    """
    return any(
        len(set(population[node] for node in component)) != 1
        for component in population_components
    )


def moran_process(
    A: npt.NDArray,
    initial_population: npt.NDArray,
    mutation_probability: float = 0,
    replacement_stochastic_matrix: Optional[npt.NDArray] = None,
    interaction_graph_adjacency_matrix: Optional[npt.NDArray] = None,
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
    replacement_stochastic_matrix: array
        Individual i chosen for replacement will replace individual j with
        probability P_{ij}.
        Default is None: this is equivalent to P_{ij} = 1 / N for all i, j.
    interaction_graph_adjacency_matrix : array
        the adjacency matrix for the interaction graph G: individuals of type i
        interact with individuals of type j count towards fitness iff G_{ij} =
        1.  Default is None: if so a complete graph is used -- this corresponds
        to all individuals interacting with each other (with no self
        interactions)




    Yields
    -------
    Generator
        The generations.
    """
    population = initial_population
    original_set_of_strategies = set(population)

    if interaction_graph_adjacency_matrix is None:
        interaction_graph_adjacency_matrix = get_complete_graph_adjacency_matrix(
            population=population
        )

    if replacement_stochastic_matrix is not None:
        G = nx.Graph(replacement_stochastic_matrix)
        population_components = tuple(nx.connected_components(G))
    else:
        population_components = (set(range(len(population))),)

    if is_population_not_fixed(
        population=population, population_components=population_components
    ):
        while (mutation_probability > 0) or is_population_not_fixed(
            population=population, population_components=population_components
        ):
            scores = score_all_individuals(
                A=A,
                population=population,
                interaction_graph_adjacency_matrix=interaction_graph_adjacency_matrix,
            )

            population = update_population(
                population=population,
                scores=scores,
                mutation_probability=mutation_probability,
                original_set_of_strategies=original_set_of_strategies,
                replacement_stochastic_matrix=replacement_stochastic_matrix,
            )

            yield population
    else:
        yield population


def fixation_probabilities(
    A: npt.NDArray,
    initial_population: npt.NDArray,
    repetitions: int,
    replacement_stochastic_matrix: Optional[npt.NDArray] = None,
    interaction_graph_adjacency_matrix: Optional[npt.NDArray] = None,
) -> Dict[tuple, float]:
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
    replacement_stochastic_matrix: array
        Individual i chosen for replacement will replace individual j with
        probability P_{ij}.
        Default is None: this is equivalent to P_{ij} = 1 / N for all i, j.
    interaction_graph_adjacency_matrix : array
        the adjacency matrix for the interaction graph G: individuals of type i
        interact with individuals of type j count towards fitness iff G_{ij} =
        1.  Default is None: if so a complete graph is used -- this corresponds
        to all individuals interacting with each other (with no self
        interactions)


    Returns
    -------
    array
        The probability of all obtained fixation states
    """

    if interaction_graph_adjacency_matrix is None:
        interaction_graph_adjacency_matrix = get_complete_graph_adjacency_matrix(
            population=initial_population
        )

    state_counts: Dict[Tuple, int] = {}
    for repetition in range(repetitions):
        generations = tuple(
            moran_process(
                A=A,
                initial_population=initial_population,
                interaction_graph_adjacency_matrix=interaction_graph_adjacency_matrix,
                replacement_stochastic_matrix=replacement_stochastic_matrix,
            )
        )
        last_population = tuple(generations[-1])
        try:
            state_counts[last_population] += 1
        except KeyError:
            state_counts[last_population] = 1

    return {state: count / repetitions for state, count in state_counts.items()}
