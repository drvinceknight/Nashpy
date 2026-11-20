"""Reproducibility and random-state isolation for fictitious play."""

import numpy as np
import pytest

from nashpy import Game
from nashpy.learning.fictitious_play import fictitious_play
from nashpy.learning.stochastic_fictitious_play import stochastic_fictitious_play


@pytest.fixture(params=["fictitious_play", "stochastic_fictitious_play"])
def simulation(request):
    """Exercise both public Game methods on a rectangular game with ties."""
    game = Game(np.zeros((2, 3)), np.zeros((2, 3)))
    return getattr(game, request.param)


def assert_same_history(actual, expected):
    """Compare all counts and probability distributions, including initial state."""
    assert len(actual) == len(expected)
    for actual_state, expected_state in zip(actual, expected):
        if isinstance(actual_state, tuple):
            actual_counts, actual_distributions = actual_state
            expected_counts, expected_distributions = expected_state
            for actual_dist, expected_dist in zip(
                actual_distributions, expected_distributions
            ):
                np.testing.assert_array_equal(actual_dist, expected_dist)
        else:
            actual_counts, expected_counts = actual_state, expected_state
        for actual_count, expected_count in zip(actual_counts, expected_counts):
            np.testing.assert_array_equal(actual_count, expected_count)


def test_same_seed_repeats_entire_history(simulation):
    """A seed determines a whole run independently of global random draws."""
    expected = list(simulation(iterations=20, seed=7))
    np.random.random(100)
    actual = list(simulation(iterations=20, seed=7))
    assert_same_history(actual, expected)


@pytest.mark.parametrize("seed", [None, 3])
def test_simulation_preserves_global_random_state(simulation, seed):
    """Neither default nor explicit seeding consumes NumPy's legacy RNG."""
    before = np.random.get_state()
    list(simulation(iterations=20, seed=seed))
    after = np.random.get_state()
    assert before[0] == after[0]
    np.testing.assert_array_equal(before[1], after[1])
    assert before[2:] == after[2:]


def test_interleaved_simulations_do_not_interfere(simulation):
    """Concurrent generator consumption does not change either trajectory."""
    expected = list(simulation(iterations=20, seed=9))
    first = simulation(iterations=20, seed=9)
    other = simulation(iterations=20, seed=31)
    actual = []
    for first_state, _ in zip(first, other):
        actual.append(first_state)
    assert_same_history(actual, expected)


def test_generator_seed_is_reused_and_advanced(simulation):
    """A caller can pass and share an existing Generator without reseeding it."""
    rng = np.random.default_rng(42)
    expected_rng = np.random.default_rng(42)
    first = list(simulation(iterations=20, seed=rng))
    second = list(simulation(iterations=20, seed=rng))
    assert_same_history(first, list(simulation(iterations=20, seed=expected_rng)))
    assert_same_history(second, list(simulation(iterations=20, seed=expected_rng)))
    assert rng.bit_generator.state == expected_rng.bit_generator.state
    assert rng.bit_generator.state != np.random.default_rng(42).bit_generator.state


@pytest.mark.parametrize("algorithm", [fictitious_play, stochastic_fictitious_play])
def test_game_wrapper_forwards_seed(algorithm):
    """The Game entry point and module-level API consume the same random draws."""
    game = Game(np.zeros((2, 3)), np.zeros((2, 3)))
    direct = list(algorithm(*game.payoff_matrices, iterations=20, seed=5))
    wrapped = list(getattr(game, algorithm.__name__)(iterations=20, seed=5))
    assert_same_history(wrapped, direct)
