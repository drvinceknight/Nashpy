from nashpy.learning.imitation_dynamics import imitation_dynamics
import numpy as np
import random


def test_positive_payoffs():
    A = np.array([[3, 0], [1, 3]])  # Payoff matrix for Player 1
    B = np.array([[0, 1], [3, 0]])  # Payoff matrix for Player 2
    nash_equilibrium_player1, nash_equilibrium_player2 = next(imitation_dynamics(A, B))
    # Assert that Nash equilibrium strategies are within the expected range
    assert np.all(nash_equilibrium_player1 >= 0)
    assert np.all(nash_equilibrium_player1 <= 1)
    assert np.all(nash_equilibrium_player2 >= 0)
    assert np.all(nash_equilibrium_player2 <= 1)


def test_negative_payoffs():
    A = np.array([[-1, 0], [0, -1]])  # Payoff matrix for Player 1 (negative payoffs)
    B = np.array([[0, -1], [-1, 0]])  # Payoff matrix for Player 2 (negative payoffs)
    nash_equilibrium_player1, nash_equilibrium_player2 = next(imitation_dynamics(A, B))
    # Assert that Nash equilibrium strategies are within the expected range
    assert np.all(nash_equilibrium_player1 >= 0)
    assert np.all(nash_equilibrium_player1 <= 1)
    assert np.all(nash_equilibrium_player2 >= 0)
    assert np.all(nash_equilibrium_player2 <= 1)


def test_randomness():
    # Define parameters for the imitation dynamics function
    A = np.array([[3, 0], [1, 3]])  # Example payoff matrix for Player 1
    B = np.array([[0, 1], [3, 0]])  # Example payoff matrix for Player 2
    population_size = 100
    num_generations = 1000

    # Run imitation dynamics multiple times and collect the results
    results = []
    for i in range(10):  # Run 10 iterations
        # Run imitation dynamics with random seed set to None (random initialization)
        nash_equilibrium_player1, nash_equilibrium_player2 = next(
            imitation_dynamics(A, B, population_size, num_generations)
        )
        results.append(
            (tuple(nash_equilibrium_player1), tuple(nash_equilibrium_player2))
        )  # Convert numpy arrays to tuples
    # Check if the results are different in at least one pair of iterations
    assert np.all(len(set(results)) > 1)


def test_random_seed_constant():
    # Define parameters for the imitation dynamics function
    A = np.array([[3, 0], [1, 3]])  # Example payoff matrix for Player 1
    B = np.array([[0, 1], [3, 0]])  # Example payoff matrix for Player 2
    population_size = 100
    iterations = 100
    random_seed = random.randrange(
        0, 1000
    )  # Add a random_seed value as constant to generate same results in the evolution

    # Run imitation dynamics multiple times and collect the results
    results = []
    for i in range(100):  # Run 10 iterations
        # Run imitation dynamics with random seed set to None (random initialization)
        nash_equilibrium_player1, nash_equilibrium_player2 = next(
            imitation_dynamics(A, B, population_size, iterations, random_seed)
        )
        results.append(
            (tuple(nash_equilibrium_player1), tuple(nash_equilibrium_player2))
        )  # Convert numpy arrays to tuples
    # Check if the results are different in at least one pair of iterations
    assert np.all(len(set(results)) == 1)
