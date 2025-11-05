"""
Tests for the moran process
"""

import numpy as np

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
    expected_steps = [
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
    ]
    beta = 1

    np.random.seed(0)
    steps = introspection_dynamics(
        M_r,
        M_c,
        number_of_iterations=number_of_iterations,
        beta=beta,
    )
    assert steps == expected_steps


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
    expected_steps = [
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
    ]
    beta = 1
    initial_actions = [2, 1]

    np.random.seed(0)
    steps = introspection_dynamics(
        M_r,
        M_c,
        number_of_iterations=number_of_iterations,
        beta=beta,
        initial_actions=initial_actions,
    )
    assert steps == expected_steps


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
    expected_steps = [
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
    ]
    beta = 1
    initial_actions = [2, 1]

    np.random.seed(1)
    steps = introspection_dynamics(
        M_r,
        M_c,
        number_of_iterations=number_of_iterations,
        beta=beta,
        initial_actions=initial_actions,
    )
    assert steps == expected_steps


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
    expected_steps = [
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
    ]
    beta = 0.2
    initial_actions = [2, 1]

    np.random.seed(1)
    steps = introspection_dynamics(
        M_r,
        M_c,
        number_of_iterations=number_of_iterations,
        beta=beta,
        initial_actions=initial_actions,
    )
    assert steps == expected_steps
