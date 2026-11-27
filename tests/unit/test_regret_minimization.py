"""Tests for cumulative regret matching in bimatrix games."""

import warnings

import numpy as np
import pytest

from nashpy.learning.regret_minimization import (
    compute_regrets,
    regret_minimization,
    update_strategy,
)


def test_compute_regrets_uses_expected_utility_and_preserves_negative_values():
    """Regret compares action utilities with the mixed strategy's payoff."""
    utilities = np.array([3.0, -1.0, 2.0])
    strategy = np.array([0.25, 0.5, 0.25])

    # The expected utility is 0.75, not a vector of strategy probabilities.
    np.testing.assert_allclose(
        compute_regrets(utilities, strategy), [2.25, -1.75, 1.25]
    )
    np.testing.assert_array_equal(utilities, [3.0, -1.0, 2.0])
    np.testing.assert_array_equal(strategy, [0.25, 0.5, 0.25])


def test_update_strategy_normalizes_positive_cumulative_regrets():
    """Only the positive part determines play; the stored regrets stay signed."""
    regrets = np.array([-4.0, 2.0, 6.0])

    np.testing.assert_array_equal(update_strategy(regrets), [0.0, 0.25, 0.75])
    np.testing.assert_array_equal(regrets, [-4.0, 2.0, 6.0])


@pytest.mark.parametrize("regrets", [[0.0, 0.0, 0.0], [-1.0, -2.0, -3.0]])
def test_update_strategy_is_uniform_without_positive_regret(regrets):
    """No positive regrets gives a uniform distribution.

    Parameters
    ----------
    regrets : list
        Non-positive cumulative regrets.
    """
    np.testing.assert_allclose(update_strategy(np.array(regrets)), [1 / 3] * 3)


@pytest.mark.parametrize("iterations", [0, 1, np.int64(1)])
def test_zero_or_one_round_returns_uniform_strategies(iterations):
    """The first played profile is uniform; zero rounds also returns it.

    Parameters
    ----------
    iterations : int
        The number of rounds, including NumPy integer input.
    """
    A = np.array([[3, 0, 1], [1, 2, 4]])
    B = np.array([[2, 5, 0], [3, 1, 4]])
    outcomes = list(regret_minimization(A, B, iterations=iterations))

    assert len(outcomes) == 1
    row_strategy, column_strategy = outcomes[0]
    assert isinstance(row_strategy, np.ndarray)
    assert isinstance(column_strategy, np.ndarray)
    np.testing.assert_allclose(row_strategy, [0.5, 0.5])
    np.testing.assert_allclose(column_strategy, [1 / 3] * 3)


def test_rectangular_game_has_correct_column_payoffs_and_synchronous_updates():
    """Average a uniform round and independently calculated second-round play."""
    A = np.array([[3, 0, 1], [1, 2, 4]])
    B = np.array([[2, 5, 0], [3, 1, 4]])

    # At the uniform profile, row utilities are (4/3, 7/3) and column
    # utilities are (5/2, 3, 2). The second profile is (0, 1), (0, 1, 0).
    row_strategy, column_strategy = next(regret_minimization(A, B, iterations=2))

    np.testing.assert_allclose(row_strategy, [1 / 4, 3 / 4])
    np.testing.assert_allclose(column_strategy, [1 / 6, 2 / 3, 1 / 6])


def test_signed_regrets_accumulate_across_rounds():
    """Distinguish cumulative matching from instantaneous matching and RM+."""
    A = np.array([[3, 0], [0, 1]])

    # Played row strategies: (1/2, 1/2), (1, 0), (1/2, 1/2).
    # Played column strategies: (1/2, 1/2), (0, 1), (0, 1).
    # After round two the row's signed regrets are (1/2, 1/2).
    row_strategy, column_strategy = next(regret_minimization(A, -A, iterations=3))

    np.testing.assert_allclose(row_strategy, [2 / 3, 1 / 3])
    np.testing.assert_allclose(column_strategy, [1 / 6, 5 / 6])


def test_average_strategies_approach_a_nonuniform_zero_sum_equilibrium():
    """Check exploitability where uniform initialization is not an equilibrium."""
    A = np.array([[3, 0], [0, 1]])
    row_strategy, column_strategy = next(regret_minimization(A, -A, iterations=5000))

    np.testing.assert_allclose(row_strategy, [1 / 4, 3 / 4], atol=0.02)
    np.testing.assert_allclose(column_strategy, [1 / 4, 3 / 4], atol=0.02)
    duality_gap = np.max(A @ column_strategy) - np.min(row_strategy @ A)
    assert duality_gap < 0.05


def test_rock_paper_scissors_preserves_the_uniform_equilibrium():
    """Zero cumulative regrets at an equilibrium keep both profiles uniform."""
    A = np.array([[0, -1, 1], [1, 0, -1], [-1, 1, 0]])

    for strategy in next(regret_minimization(A, -A)):
        np.testing.assert_allclose(strategy, [1 / 3] * 3)


def test_one_strategy_game():
    """A player with one action always assigns it probability one."""
    A = np.array([[1, 2, 3]])
    B = np.array([[4, 4, 4]])
    row_strategy, column_strategy = next(regret_minimization(A, B, iterations=5))

    np.testing.assert_array_equal(row_strategy, [1.0])
    np.testing.assert_allclose(column_strategy, [1 / 3] * 3)


def test_strategies_are_invariant_to_positive_affine_payoff_changes():
    """Positive scaling and shifting preserve play, including negative payoffs."""
    A = np.array([[3, 0, 1], [1, 2, 4]])
    B = np.array([[2, 5, 0], [3, 1, 4]])
    expected = next(regret_minimization(A, B, iterations=10))
    obtained = next(regret_minimization(2 * A - 20, 3 * B - 30, iterations=10))

    for actual, reference in zip(obtained, expected):
        np.testing.assert_allclose(actual, reference)
        assert np.isfinite(actual).all()
        assert (actual >= 0).all()
        np.testing.assert_allclose(actual.sum(), 1)


@pytest.mark.parametrize("scale", [np.finfo(float).max, np.nextafter(0.0, 1.0)])
def test_regret_matching_at_extreme_payoff_scales(scale):
    """Keep strategy probabilities valid at either end of the float range.

    Parameters
    ----------
    scale : float
        Magnitude of each nonzero payoff.
    """
    A = np.array([[1.0, 1.0]] * 2 + [[-1.0, -1.0]] * 2) * scale
    B = np.array([[-1.0, 1.0]] * 4) * scale

    with np.errstate(over="raise", invalid="raise"):
        row, column = next(regret_minimization(A, B, iterations=2))

    np.testing.assert_allclose(row, [3 / 8, 3 / 8, 1 / 8, 1 / 8])
    np.testing.assert_allclose(column, [1 / 4, 3 / 4])


def test_input_matrices_are_not_modified():
    """Running the algorithm does not overwrite caller-owned payoff matrices."""
    A = np.array([[3.0, 0.0], [0.0, 1.0]])
    B = -A
    original_A, original_B = A.copy(), B.copy()

    next(regret_minimization(A, B, iterations=3))

    np.testing.assert_array_equal(A, original_A)
    np.testing.assert_array_equal(B, original_B)


def test_deterministic_play_does_not_use_numpy_global_random_state():
    """The result is independent of the global seed and consumes no randomness."""
    A = np.array([[3, 0], [0, 1]])
    previous_state = np.random.get_state()
    try:
        np.random.seed(12)
        first = next(regret_minimization(A, -A, iterations=3))
        assert np.random.random() == np.random.RandomState(12).random_sample()
        np.random.seed(99)
        second = next(regret_minimization(A, -A, iterations=3))
    finally:
        np.random.set_state(previous_state)
    for actual, expected in zip(first, second):
        np.testing.assert_array_equal(actual, expected)


def test_legacy_learning_rate_warns_without_changing_results():
    """Old positional and keyword calls remain usable without a rate parameter."""
    A = np.array([[3, 0], [0, 1]])
    with warnings.catch_warnings():
        warnings.simplefilter("error", DeprecationWarning)
        expected = next(regret_minimization(A, -A, iterations=3))

    with pytest.warns(DeprecationWarning, match="learning_rate.*ignored"):
        positional = next(regret_minimization(A, -A, 0.1, 3))
    with pytest.warns(DeprecationWarning, match="learning_rate.*ignored"):
        keyword = next(regret_minimization(A, -A, learning_rate=0, iterations=3))

    for result in (positional, keyword):
        for actual, reference in zip(result, expected):
            np.testing.assert_array_equal(actual, reference)


@pytest.mark.parametrize(
    "A, B, message",
    [
        ([1, 2], [1, 2], "two-dimensional"),
        (np.ones((2, 2)), np.ones(2), "two-dimensional"),
        (np.ones((2, 3)), np.ones((3, 2)), "same shape"),
        (np.ones((0, 2)), np.ones((0, 2)), "non-empty"),
        (np.ones((2, 0)), np.ones((2, 0)), "non-empty"),
        ([[np.nan]], [[0]], "finite"),
        ([[0]], [[np.inf]], "finite"),
        ([[1j]], [[0]], "real"),
        ([[0]], [[1j]], "real"),
    ],
)
def test_invalid_payoff_matrices(A, B, message):
    """Reject matrices that do not describe a finite, real bimatrix game.

    Parameters
    ----------
    A : array
        The row payoff matrix.
    B : array
        The column payoff matrix.
    message : str
        The expected error message.
    """
    with pytest.raises(ValueError, match=message):
        next(regret_minimization(A, B))


@pytest.mark.parametrize("iterations", [-1, 1.5, True])
def test_invalid_iterations(iterations):
    """Only non-negative integer iteration counts are accepted.

    Parameters
    ----------
    iterations : object
        An invalid number of rounds.
    """
    with pytest.raises(ValueError, match="non-negative integer"):
        next(regret_minimization(np.eye(2), np.eye(2), iterations=iterations))
