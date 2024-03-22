"""A function for a Imitation Dynamics algorithm"""

import numpy as np
from typing import Generator, Tuple, Any
import numpy.typing as npt


def payoff(player_strategy, opponent_strategy, player_payoff_matrix):
    """
    Calculate the payoff of a player given their strategy and the opponent's strategy.

    Parameters
    ----------
    player_strategy: numpy array
        representing the strategy of the player
    opponent_strategy: numpy array
        representing the strategy of the opponent
    player_payoff_matrix: numpy matrix
        representing the payoff matrix for the player

    Returns
    -------
    return_value: scalar representing strategy and payoff matrix
    """
    return_value = np.dot(
        player_strategy, np.dot(player_payoff_matrix, opponent_strategy)
    )
    return return_value


def imitation_dynamics(
    A: npt.NDArray,
    B: npt.NDArray,
    population_size=100,
    iterations=1000,
    random_seed=None,
    threshold=0.5,
) -> Generator[Tuple[float, float], Any, None]:
    """
    Simulate the imitation dynamics for a given game represented by payoff matrices A and B.

    Parameters
    ----------
    A : numpy matrix
        representing the payoff matrix for Player 1
    B : numpy matrix
        representing the payoff matrix for Player 2
    population_size : number
        number of individuals in the population of the group (default: 100)
    iterations : number
        number of generations to simulate (default: 1000)
    random_seed : number
        seed for reproducibility (default: None)
    threshold : float
        threshold value for representing strategies as 0 or 1 (default: 0.5)

    Yields
    -------
    Generator
        The equilibria.
    """
    num_strategies = len(A)

    # Initialize population
    if random_seed:
        np.random.seed(random_seed)  # Set random seed for reproducibility

    population_A = np.random.dirichlet(np.ones(num_strategies), size=population_size)
    population_B = np.random.dirichlet(np.ones(num_strategies), size=population_size)

    for generation in range(iterations):
        # Play the game
        payoffs_A = np.array(
            [
                payoff(population_A[i], population_B[i], A)
                for i in range(population_size)
            ]
        )
        payoffs_B = np.array(
            [
                payoff(population_B[i], population_A[i], B)
                for i in range(population_size)
            ]
        )

        # Update population based on payoffs
        # Used Imitation dynamics in which the players copy the strategy of the most successful individual
        fittest_A_index = np.argmax(payoffs_A)
        fittest_B_index = np.argmax(payoffs_B)
        population_A = np.tile(population_A[fittest_A_index], (population_size, 1))
        population_B = np.tile(population_B[fittest_B_index], (population_size, 1))

    # Calculate Nash equilibrium strategies
    nash_equilibrium_A = np.mean(population_A, axis=0)
    nash_equilibrium_B = np.mean(population_B, axis=0)

    # Threshold the strategies
    nash_equilibrium_A[nash_equilibrium_A >= threshold] = 1
    nash_equilibrium_A[nash_equilibrium_A < threshold] = 0
    nash_equilibrium_B[nash_equilibrium_B >= threshold] = 1
    nash_equilibrium_B[nash_equilibrium_B < threshold] = 0

    yield nash_equilibrium_A, nash_equilibrium_B
