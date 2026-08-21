"""Tests for imitation dynamics."""

import numpy as np
import pytest

from nashpy.learning.imitation_dynamics import imitation_dynamics, payoff


def test_payoff_for_rectangular_game():
    """A payoff is calculated in row-player, column-player order."""
    payoff_matrix = np.array(((3, 0, 1), (2, 4, 5)))
    row_strategy = np.array((0.25, 0.75))
    column_strategy = np.array((0.2, 0.3, 0.5))

    expected_payoff = row_strategy @ payoff_matrix @ column_strategy

    assert payoff(row_strategy, column_strategy, payoff_matrix) == expected_payoff


def test_imitation_dynamics_supports_rectangular_games():
    """The two populations use their respective numbers of strategies."""
    A = np.array(((3, 0, 1), (1, 2, 4)))
    B = np.array(((2, 5, 0), (3, 1, 4)))

    row_profile, column_profile = next(
        imitation_dynamics(
            A,
            B,
            population_size=5,
            iterations=2,
            threshold=0.4,
            seed=0,
        )
    )

    assert row_profile.shape == (2,)
    assert column_profile.shape == (3,)
    assert set(np.unique(row_profile)) <= {0, 1}
    assert set(np.unique(column_profile)) <= {0, 1}


def test_seed_zero_is_reproducible():
    """Zero is a valid seed."""
    A = np.array(((3, 0), (1, 2)))
    B = np.array(((2, 1), (0, 3)))

    first_result = next(
        imitation_dynamics(A, B, population_size=10, iterations=2, seed=0)
    )
    second_result = next(
        imitation_dynamics(A, B, population_size=10, iterations=2, seed=0)
    )

    for first_profile, second_profile in zip(first_result, second_result):
        np.testing.assert_array_equal(first_profile, second_profile)


def test_seed_does_not_modify_numpy_global_random_state():
    """The function uses a local random number generator."""
    A = np.array(((3, 0), (1, 2)))
    B = np.array(((2, 1), (0, 3)))

    np.random.seed(12)
    expected_next_random_value = np.random.random()

    np.random.seed(12)
    next(imitation_dynamics(A, B, population_size=5, iterations=1, seed=4))
    actual_next_random_value = np.random.random()

    assert actual_next_random_value == expected_next_random_value


def test_random_seed_is_a_backwards_compatible_alias_for_seed():
    """The old ``random_seed`` parameter produces the same result as ``seed``."""
    A = np.array(((3, 0), (1, 2)))
    B = np.array(((2, 1), (0, 3)))

    result_with_seed = next(
        imitation_dynamics(A, B, population_size=10, iterations=2, seed=0)
    )
    result_with_random_seed = next(
        imitation_dynamics(A, B, population_size=10, iterations=2, random_seed=0)
    )

    for seed_profile, random_seed_profile in zip(
        result_with_seed, result_with_random_seed
    ):
        np.testing.assert_array_equal(seed_profile, random_seed_profile)


def test_seed_and_random_seed_cannot_both_be_set():
    """Two conflicting seeds are rejected."""
    A = np.eye(2)

    with pytest.raises(ValueError, match="seed and random_seed"):
        next(imitation_dynamics(A, A, seed=1, random_seed=1))


def test_imitation_dynamics_validates_payoff_matrix_shapes():
    """Both payoff matrices must describe the same bimatrix game."""
    A = np.ones((2, 3))

    with pytest.raises(ValueError, match="two-dimensional"):
        next(imitation_dynamics(np.ones(2), np.ones(2), seed=0))

    with pytest.raises(ValueError, match="same shape"):
        next(imitation_dynamics(A, np.ones((3, 2)), seed=0))


@pytest.mark.parametrize(
    ("population_size", "iterations", "threshold", "message"),
    (
        (0, 1, 0.5, "population_size"),
        (1, -1, 0.5, "iterations"),
        (1, 1, -0.1, "threshold"),
        (1, 1, 1.1, "threshold"),
    ),
)
def test_imitation_dynamics_validates_simulation_parameters(
    population_size, iterations, threshold, message
):
    """Invalid simulation parameters have informative errors.

    Parameters
    ----------
    population_size : int
        The population size passed to the simulation.
    iterations : int
        The number of generations passed to the simulation.
    threshold : float
        The threshold passed to the simulation.
    message : str
        The text expected in the error message.
    """
    A = np.eye(2)

    with pytest.raises(ValueError, match=message):
        next(
            imitation_dynamics(
                A,
                A,
                population_size=population_size,
                iterations=iterations,
                threshold=threshold,
                seed=0,
            )
        )


def test_threshold_is_applied_to_the_final_population_profiles():
    """The threshold controls the binary representation returned to users."""
    A = np.eye(2)

    profiles_with_zero_threshold = next(
        imitation_dynamics(A, A, population_size=2, iterations=0, threshold=0, seed=0)
    )
    profiles_with_one_threshold = next(
        imitation_dynamics(A, A, population_size=2, iterations=0, threshold=1, seed=0)
    )

    for profile in profiles_with_zero_threshold:
        np.testing.assert_array_equal(profile, np.ones(2))
    for profile in profiles_with_one_threshold:
        np.testing.assert_array_equal(profile, np.zeros(2))


def test_imitation_dynamics_yields_one_final_profile_pair():
    """The existing final-result generator contract is preserved."""
    A = np.eye(2)

    outcomes = list(imitation_dynamics(A, A, population_size=2, iterations=2, seed=0))

    assert len(outcomes) == 1
