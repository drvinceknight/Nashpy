"""Code for implementation of a Moran process"""
import numpy as np
import numpy.typing as npt

from typing import Generator


def score_all_individuals(
    A: npt.NDArray,
    population: npt.NDArray,
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

    Returns
    -------
    array
        the scores of every player in the population

    Raises
    ------
    ValueError
        If the payoff matrix A has a non positive value. Currently only
        positive valued matrices are supported.

    """
    if np.min(A) <= 0:
        raise ValueError("Only positive valued payoff matrices are currently supported")

    scores = []

    for i, player in enumerate(population):
        total = 0
        for j, opponent in enumerate(population):
            if i != j:
                total += A[player, opponent]
        scores.append(total)

    return np.array(scores)


def update_population(
    population: npt.NDArray,
    scores: npt.NDArray,
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

    Returns
    -------
    array
        the next population
    """
    N = len(population)
    next_population = np.array(population)
    probabilities = scores / np.sum(scores)

    birth_index = np.random.choice(range(N), p=probabilities)
    death_index = np.random.randint(N)

    next_population[death_index] = next_population[birth_index]

    return next_population


def moran_process(
    A: npt.NDArray,
    initial_population: npt.NDArray,
) -> Generator[npt.NDArray, None, None]:
    """
    Return a generator of population across the Moran process. The last
    population is when only a single type of individual is present in the
    population.

    Parameters
    ----------
    A : array
        a payoff matrix
    initial_population : array
        the initial population


    Yields
    -------
    Generator
        The generations.
    """
    population = initial_population
    while len(set(population)) != 1:

        scores = score_all_individuals(A=A, population=population)
        population = update_population(population=population, scores=scores)

        yield population
