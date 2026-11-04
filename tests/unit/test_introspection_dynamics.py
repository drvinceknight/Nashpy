"""
Tests for introspection dynamics
"""

import numpy as np
import pytest
from hypothesis import given
from hypothesis.extra.numpy import arrays
from hypothesis.strategies import integers

from nashpy.learning.introspection_dynamics import (
    introspection_dynamics,
    introspection_dynamics_state_distribution,
)


def test_introspection_dynamics_with_seed_0():
    M_r = np.array(
        (
            (3, 4),
            (5, 1),
            (6, 3),
        )
    )
    M_c = np.array(
        (
            (5, 2),
            (3, 4),
            (1, 9),
        )
    )
    number_of_iterations = 10
    expected_steps = (
        [0, 1],
        [0, 0],
        [0, 0],
        [0, 0],
        [1, 0],
        [1, 0],
        [1, 0],
        [1, 1],
        [1, 1],
        [1, 1],
        [2, 1],
    )
    beta = 1

    np.random.seed(0)
    steps = tuple(
        introspection_dynamics(
            M_r,
            M_c,
            number_of_iterations=number_of_iterations,
            beta=beta,
        )
    )
    assert np.array_equal(steps, expected_steps)


@pytest.mark.parametrize("shape", [(2, 2), (2, 3), (3, 2)])
def test_state_distribution_without_learning(shape):
    A = np.arange(np.prod(shape)).reshape(shape)
    B = -A
    distribution = introspection_dynamics_state_distribution(A, B, beta=0)
    assert np.allclose(distribution, np.full(shape, 1 / np.prod(shape)))


def test_state_distribution_with_independent_payoffs():
    # Each player's stationary marginal is proportional to exp(beta * payoff).
    # With beta = log(2), the unnormalised marginals are [1, 2] and [1, 2, 4].
    A = np.array([[0, 0, 0], [1, 1, 1]])
    B = np.array([[0, 1, 2], [0, 1, 2]])
    distribution = introspection_dynamics_state_distribution(A, B, beta=np.log(2))
    assert np.allclose(distribution, np.array([[1, 2, 4], [2, 4, 8]]) / 21)


def test_state_distribution_satisfies_balance_equations():
    # Hand-calculated one-step probabilities in row-major order.
    # At beta = log(3), a payoff gain/loss of one is accepted
    # with probability 3/4 or 1/4, respectively; each player is selected 1/2.
    A = np.array([[1, 0, 1], [0, 1, 1]])
    B = np.array([[0, 1, 0], [1, 0, 1]])
    transition_matrix = (
        np.array(
            [
                [9, 3, 2, 2, 0, 0],
                [1, 8, 1, 0, 6, 0],
                [2, 3, 7, 0, 0, 4],
                [6, 0, 0, 7, 1, 2],
                [0, 2, 0, 3, 8, 3],
                [0, 0, 4, 2, 1, 9],
            ]
        )
        / 16
    )
    distribution = introspection_dynamics_state_distribution(A, B, beta=np.log(3))
    assert distribution.shape == A.shape
    assert np.all(distribution >= 0)
    assert np.isclose(distribution.sum(), 1)
    assert np.allclose(distribution.ravel() @ transition_matrix, distribution.ravel())


@given(
    A=arrays(np.int8, (2, 3), elements=integers(-3, 3)),
    B=arrays(np.int8, (2, 3), elements=integers(-3, 3)),
)
def test_state_distribution_is_unchanged_by_relabelling_players(A, B):
    distribution = introspection_dynamics_state_distribution(A, B, beta=0.5)
    swapped_distribution = introspection_dynamics_state_distribution(B.T, A.T, beta=0.5)
    assert np.all(distribution >= 0)
    assert np.isclose(distribution.sum(), 1)
    assert np.allclose(distribution, swapped_distribution.T)


def test_state_distribution_ignores_payoff_offsets():
    A = np.array([[3, 0, 2], [1, 4, 0]])
    B = np.array([[0, 1, 3], [3, 0, 2]])
    distribution = introspection_dynamics_state_distribution(A, B, beta=0.5)
    shifted_distribution = introspection_dynamics_state_distribution(
        A + [10, -5, 3], B + np.array([[7], [-4]]), beta=0.5
    )
    assert np.allclose(distribution, shifted_distribution)


def test_state_distribution_with_strong_learning():
    A = np.array([[0, 0, 0], [1, 1, 1]])
    B = np.array([[0, 1, 2], [0, 1, 2]])
    with np.errstate(over="raise"):
        distribution = introspection_dynamics_state_distribution(A, B, beta=50)
    row_weights = np.exp(np.array([-50, 0]))
    column_weights = np.exp(np.array([-100, -50, 0]))
    expected = np.outer(
        row_weights / row_weights.sum(), column_weights / column_weights.sum()
    )
    assert np.all(distribution >= 0)
    assert np.allclose(distribution, expected, atol=0, rtol=1e-12)


def test_state_distribution_reports_transition_underflow():
    A = np.eye(2)
    with np.errstate(over="raise"):
        with pytest.raises(np.linalg.LinAlgError, match="underflow"):
            introspection_dynamics_state_distribution(A, A, beta=1000)


@pytest.mark.parametrize("beta", [-1, np.inf, -np.inf, np.nan])
def test_state_distribution_rejects_invalid_learning_intensity(beta):
    with pytest.raises(ValueError, match="finite and non-negative"):
        introspection_dynamics_state_distribution(
            np.zeros((2, 2)), np.zeros((2, 2)), beta
        )


@pytest.mark.parametrize(
    "A, B",
    [
        (np.zeros(2), np.zeros(2)),
        (np.zeros((2, 2)), np.zeros((2, 3))),
        (np.zeros((1, 2)), np.zeros((1, 2))),
        (np.zeros((2, 1)), np.zeros((2, 1))),
    ],
)
def test_state_distribution_rejects_invalid_shapes(A, B):
    with pytest.raises(ValueError, match="same shape.*at least two actions"):
        introspection_dynamics_state_distribution(A, B, beta=1)


@pytest.mark.parametrize("payoff", [np.nan, np.inf, -np.inf])
def test_state_distribution_rejects_nonfinite_payoffs(payoff):
    A = np.array([[payoff, 0], [0, 0]])
    with pytest.raises(ValueError, match="finite payoffs"):
        introspection_dynamics_state_distribution(A, np.zeros((2, 2)), beta=1)


def test_introspection_dynamics_with_seed_0_and_initial_action_set():
    M_r = np.array(
        (
            (3, 4),
            (5, 1),
            (6, 3),
        )
    )
    M_c = np.array(
        (
            (5, 2),
            (3, 4),
            (1, 9),
        )
    )
    number_of_iterations = 10
    expected_steps = (
        [2, 1],
        [2, 1],
        [2, 1],
        [2, 1],
        [2, 1],
        [2, 1],
        [0, 1],
        [0, 1],
        [0, 1],
        [0, 0],
        [2, 0],
    )
    beta = 1
    initial_actions = [2, 1]

    np.random.seed(0)
    steps = tuple(
        introspection_dynamics(
            M_r,
            M_c,
            number_of_iterations=number_of_iterations,
            beta=beta,
            initial_actions=initial_actions,
        )
    )
    assert np.array_equal(steps, expected_steps)


def test_introspection_dynamics_with_seed_1_and_initial_action_set():
    M_r = np.array(
        (
            (3, 4),
            (5, 1),
            (6, 3),
        )
    )
    M_c = np.array(
        (
            (5, 2),
            (3, 4),
            (1, 9),
        )
    )
    number_of_iterations = 10
    expected_steps = (
        [2, 1],
        [2, 1],
        [2, 1],
        [2, 1],
        [2, 1],
        [2, 1],
        [2, 1],
        [2, 1],
        [2, 1],
        [2, 1],
        [2, 1],
    )
    beta = 1
    initial_actions = [2, 1]

    np.random.seed(1)
    steps = tuple(
        introspection_dynamics(
            M_r,
            M_c,
            number_of_iterations=number_of_iterations,
            beta=beta,
            initial_actions=initial_actions,
        )
    )
    assert np.array_equal(steps, expected_steps)


def test_introspection_dynamics_with_seed_1_and_initial_action_set_and_low_beta():
    M_r = np.array(
        (
            (3, 4),
            (5, 1),
            (6, 3),
        )
    )
    M_c = np.array(
        (
            (5, 2),
            (3, 4),
            (1, 9),
        )
    )
    number_of_iterations = 10
    expected_steps = (
        [2, 1],
        [2, 1],
        [1, 1],
        [1, 0],
        [2, 0],
        [2, 1],
        [2, 1],
        [2, 1],
        [2, 1],
        [2, 1],
        [2, 1],
    )
    beta = 0.2
    initial_actions = [2, 1]

    np.random.seed(1)
    steps = tuple(
        introspection_dynamics(
            M_r,
            M_c,
            number_of_iterations=number_of_iterations,
            beta=beta,
            initial_actions=initial_actions,
        )
    )
    assert np.array_equal(steps, expected_steps)
