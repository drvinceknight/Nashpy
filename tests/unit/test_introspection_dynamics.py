"""
Tests for the moran process
"""

import numpy as np
import pytest

from nashpy.learning.introspection_dynamics import introspection_dynamics


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


@pytest.mark.parametrize("shape", [(1, 1), (1, 2), (2, 1)])
@pytest.mark.parametrize("initial_actions", [None, np.array([0, 0])])
def test_introspection_with_single_action_player(shape, initial_actions):
    """A player without alternative actions leaves the current state unchanged."""
    payoffs = np.ones(shape)
    np.random.seed(0)
    steps = np.array(
        tuple(
            introspection_dynamics(
                payoffs,
                payoffs,
                number_of_iterations=50,
                beta=0,
                initial_actions=initial_actions,
            )
        )
    )
    assert steps.shape == (51, 2)
    for player, number_of_actions in enumerate(shape):
        assert np.all(steps[:, player] >= 0)
        assert np.all(steps[:, player] < number_of_actions)
        assert np.array_equal(np.unique(steps[:, player]), np.arange(number_of_actions))


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
