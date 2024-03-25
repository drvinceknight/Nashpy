import numpy as np
from nashpy.learning.regret_minimization import regret_minimization


def test_regret_minimization_for_zerosum_game():
    # Test case values
    A = np.array(
        [[0, -1, 1], [1, 0, -1], [-1, 1, 0]]
    )  # Example payoff matrix for Player A
    B = -A  # Example payoff matrix for Player B ( Zero Sum Game )
    learning_rate = 0.1
    max_iterations = 100
    expected_nash_equilibrium_A = np.array(
        [0.3333333333333333, 0.3333333333333333, 0.3333333333333333]
    )  # Expected Nash equilibrium strategy for Player 1
    expected_nash_equilibrium_B = np.array(
        [0.3333333333333333, 0.3333333333333333, 0.3333333333333333]
    )  # Expected Nash equilibrium strategy for Player 2

    # Execute the regret minimization algorithm
    actual_nash_equilibrium_A, actual_nash_equilibrium_B = next(
        regret_minimization(A, B, learning_rate, max_iterations)
    )

    # Assert if the actual Nash equilibrium strategies match the expected strategies
    assert np.array_equal(actual_nash_equilibrium_A, expected_nash_equilibrium_A)
    assert np.array_equal(actual_nash_equilibrium_B, expected_nash_equilibrium_B)


def test_regret_minimization_non_zerosum_game():
    # Test case values
    A = np.array([[3, -1, 3], [-1, 3, 6], [-1, 1, 2]])
    B = np.array([[-3, 1, 4], [1, -3, 3], [-1, 3, 4]])
    learning_rate = 0.1
    iterations = 100

    expected_nash_equilibrium_A = np.array(
        [0.0, 1.0, 0.0]
    )  # Expected Nash equilibrium strategy for Player 1
    expected_nash_equilibrium_B = np.array(
        [0.0, 0.0, 1.0]
    )  # Expected Nash equilibrium strategy for Player 2
    # Execute the regret minimization algorithm
    actual_nash_equilibrium_A, actual_nash_equilibrium_B = next(
        regret_minimization(A, B, learning_rate, iterations)
    )

    # Assert if the actual Nash equilibrium strategies match the expected strategies
    assert np.array_equal(actual_nash_equilibrium_A, expected_nash_equilibrium_A)
    assert np.array_equal(actual_nash_equilibrium_B, expected_nash_equilibrium_B)
