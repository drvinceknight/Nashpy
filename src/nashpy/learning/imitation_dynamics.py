"""Code to simulate an imitate-the-best population process."""

from typing import Generator, Optional, Tuple

import numpy as np
import numpy.typing as npt


def payoff(
    row_strategy: npt.NDArray,
    column_strategy: npt.NDArray,
    payoff_matrix: npt.NDArray,
) -> float:
    """Calculate the expected payoff for a mixed-strategy profile.

    Parameters
    ----------
    row_strategy : array
        The mixed strategy of the row player.
    column_strategy : array
        The mixed strategy of the column player.
    payoff_matrix : array
        The payoff matrix of the player whose payoff is being calculated.

    Returns
    -------
    float
        The expected payoff.
    """
    return float(row_strategy @ payoff_matrix @ column_strategy)


def imitation_dynamics(
    A: npt.NDArray,
    B: npt.NDArray,
    population_size: int = 100,
    iterations: int = 1000,
    random_seed: Optional[int] = None,
    threshold: float = 0.5,
    *,
    seed: Optional[int] = None,
) -> Generator[Tuple[npt.NDArray, npt.NDArray], None, None]:
    """Simulate an imitate-the-best process for a bimatrix game.

    Each individual in the row population is paired with the individual at the
    same position in the column population. After payoffs are calculated, every
    individual in a population copies that population's highest-payoff mixed
    strategy. The generator yields one pair of thresholded final population
    profiles, preserving the existing public return contract.

    Parameters
    ----------
    A : array
        The row player payoff matrix.
    B : array
        The column player payoff matrix.
    population_size : int
        The number of individuals in each population.
    iterations : int
        The number of generations to simulate.
    random_seed : int, optional
        Backwards-compatible alias for ``seed``.
    threshold : float
        Values in the final mean population profiles that are greater than or
        equal to this value are represented by 1; lower values by 0.
    seed : int, optional
        Seed for a local NumPy random number generator.

    Yields
    ------
    tuple
        The thresholded final row and column population profiles.

    Raises
    ------
    ValueError
        If the payoff matrices or simulation parameters are invalid, or if
        both ``seed`` and ``random_seed`` are supplied.
    """
    A = np.asarray(A)
    B = np.asarray(B)

    if A.ndim != 2 or B.ndim != 2:
        raise ValueError("A and B must be two-dimensional payoff matrices.")
    if A.shape != B.shape:
        raise ValueError("A and B must have the same shape.")
    if population_size <= 0:
        raise ValueError("population_size must be positive.")
    if iterations < 0:
        raise ValueError("iterations must be non-negative.")
    if not 0 <= threshold <= 1:
        raise ValueError("threshold must be between 0 and 1 inclusive.")
    if seed is not None and random_seed is not None:
        raise ValueError("seed and random_seed cannot both be supplied.")
    if seed is None:
        seed = random_seed

    number_of_row_strategies, number_of_column_strategies = A.shape
    random_generator = np.random.default_rng(seed)
    row_population = random_generator.dirichlet(
        np.ones(number_of_row_strategies), size=population_size
    )
    column_population = random_generator.dirichlet(
        np.ones(number_of_column_strategies), size=population_size
    )

    for _ in range(iterations):
        row_payoffs = np.array(
            [
                payoff(row_population[i], column_population[i], A)
                for i in range(population_size)
            ]
        )
        column_payoffs = np.array(
            [
                payoff(row_population[i], column_population[i], B)
                for i in range(population_size)
            ]
        )

        fittest_row_index = np.argmax(row_payoffs)
        fittest_column_index = np.argmax(column_payoffs)
        row_population = np.tile(
            row_population[fittest_row_index], (population_size, 1)
        )
        column_population = np.tile(
            column_population[fittest_column_index], (population_size, 1)
        )

    row_profile = (np.mean(row_population, axis=0) >= threshold).astype(float)
    column_profile = (np.mean(column_population, axis=0) >= threshold).astype(float)

    yield row_profile, column_profile
