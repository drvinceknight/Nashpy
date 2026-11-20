"""
Tests for stochastic fictitious learning
"""

from hypothesis import given
from hypothesis.extra.numpy import arrays
import numpy as np
import pytest

from nashpy.learning.stochastic_fictitious_play import (
    get_distribution_response_to_play_count,
    stochastic_fictitious_play,
)


@given(M=arrays(np.int8, (2, 2)))
def test_property_get_distribution_response_to_play_count(M):
    etha = 2
    epsilon_bar = 2
    play_count = np.zeros(M.shape[0])
    distribution_response = get_distribution_response_to_play_count(
        A=M, play_count=play_count, epsilon_bar=epsilon_bar, etha=etha
    )
    assert len(distribution_response) == len(play_count)
    assert np.all(distribution_response) >= 0
    assert np.isclose(np.sum(distribution_response), 1)


def test_get_distribution_response_to_play_count_2():
    rng = np.random.default_rng(0)
    M = np.array([[3, 2], [7, 6]])
    etha = 2
    epsilon_bar = 2
    play_count = [40, 30]
    expected_distribution = np.array([0.16344373, 0.83655627])
    distribution_response = get_distribution_response_to_play_count(
        A=M, play_count=play_count, epsilon_bar=epsilon_bar, etha=etha, rng=rng
    )
    assert np.allclose(distribution_response, expected_distribution)
    np.testing.assert_allclose(
        np.sum(distribution_response), 1, rtol=0, atol=np.finfo(float).eps
    )


def test_get_distribution_response_to_play_for_bug_reported_by_user():
    """
    This is a bug reported by email.

    Captured here: https://github.com/drvinceknight/Nashpy/issues/214
    """
    A = np.array([[113, 65, 112], [141, 93, -56], [120, 73, -76]])
    etha = 10**-1
    epsilon_bar = 10**-2
    play_count = [1, 1, 1]
    distribution = get_distribution_response_to_play_count(
        A=A,
        play_count=play_count,
        epsilon_bar=epsilon_bar,
        etha=etha,
        rng=np.random.default_rng(0),
    )
    assert np.all(np.isfinite(distribution))
    assert np.isclose(np.sum(distribution), 1)


@pytest.mark.parametrize("payoff", [71.0, 70.9, -100.0])
@pytest.mark.parametrize("play_count", [np.zeros(4), np.array([1, 2, 3, 4])])
def test_large_constant_payoffs_have_uniform_response(payoff, play_count):
    """Overflow, an overflowing normalizer, and underflow preserve a uniform response.

    Parameters
    ----------
    payoff : float
        The common payoff for every action.
    play_count : array
        Counts defining the opponent's empirical strategy.
    """
    distribution = get_distribution_response_to_play_count(
        A=np.full((4, 4), payoff),
        play_count=play_count,
        epsilon_bar=0,
        etha=0.1,
    )
    np.testing.assert_array_equal(distribution, np.full(4, 0.25))


@pytest.mark.parametrize("offset", [0, 1000, -1000])
def test_logit_response_depends_on_payoff_differences(offset):
    """A common payoff offset leaves the nonsaturated logit probabilities unchanged.

    Parameters
    ----------
    offset : float
        The common payoff added to both actions.
    """
    distribution = get_distribution_response_to_play_count(
        A=np.array([[0, 0], [1, 1]], dtype=float) + offset,
        play_count=np.zeros(2),
        epsilon_bar=0,
        etha=0.5,
    )
    first = 1 / (1 + np.exp(2))
    np.testing.assert_allclose(distribution, [first, 1 - first], rtol=1e-14)


def test_nonfinite_payoffs_still_raise():
    """Undefined utilities must not silently become an arbitrary distribution."""
    with pytest.raises(ValueError):
        get_distribution_response_to_play_count(
            A=np.full((2, 2), np.nan),
            play_count=np.zeros(2),
            epsilon_bar=0,
            etha=0.1,
        )


def test_get_distribution_response_to_play_count_3():
    rng = np.random.default_rng(0)
    M = np.array([[3, 2], [7, 6]])
    etha = 0.2
    epsilon_bar = 0.05
    play_count = np.array([0, 0])
    r_dist = get_distribution_response_to_play_count(
        A=M, play_count=play_count, epsilon_bar=epsilon_bar, etha=etha, rng=rng
    )
    assert np.allclose(r_dist, np.array([2.25931027e-09, 9.99999998e-01]))

    c_dist = get_distribution_response_to_play_count(
        A=M.transpose(),
        play_count=play_count,
        epsilon_bar=epsilon_bar,
        etha=etha,
        rng=rng,
    )
    assert np.allclose(c_dist, np.array([0.99334766, 0.00665234]))


def test_stochastic_fictitious_play_given_etha_epsilon():
    iterations = 1
    M = np.array([[3, 2], [7, 6]])
    etha = 0.2
    epsilon_bar = 0.05
    counts_and_distributions = tuple(
        stochastic_fictitious_play(
            A=M, B=-M, etha=etha, epsilon_bar=epsilon_bar, iterations=iterations, seed=0
        )
    )
    playcounts, dist = counts_and_distributions[1]
    r_playcounts, c_playcounts = playcounts
    r_dist, c_dist = dist
    assert np.array_equal(playcounts, [np.array([0, 1.0]), np.array([0, 1.0])])
    assert np.array_equal(r_playcounts, np.array([0, 1.0]))
    assert np.allclose(r_dist, np.array([2.25931027e-09, 9.99999998e-01]))
    assert len(counts_and_distributions) == 2
    assert np.allclose(c_dist, np.array([0.0067336, 0.9932664]))


def test_stochastic_fictitious_play_default_inputs():
    iterations = 3
    M = np.array([[3, 2], [7, 6]])
    counts_and_distributions = tuple(
        stochastic_fictitious_play(A=M, B=-M, iterations=iterations, seed=0)
    )
    playcounts, dist = counts_and_distributions[-1]
    r_playcounts, c_playcounts = playcounts
    r_dist, c_dist = dist
    assert np.array_equal(playcounts, [np.array([0, 3]), np.array([0, 3])])
    assert np.allclose(r_dist, np.array([4.6131621e-18, 1.00000000e00]))
    assert np.allclose(c_dist, np.array([4.79837569e-05, 9.99952016e-01]))
    assert len(counts_and_distributions) == 4
    assert np.sum(playcounts) == 2 * iterations


def test_stochastic_fictitious_play_2x3():
    iterations = 3
    M = np.array([[3, 2, -2], [7, -2, 6]])
    N = np.array([[2, -2, 3], [-4, 2, 6]])
    etha = 2
    epsilon_bar = 0.2
    counts_and_distributions = tuple(
        stochastic_fictitious_play(
            A=M, B=N, etha=etha, epsilon_bar=epsilon_bar, iterations=iterations, seed=0
        )
    )
    playcounts, dist = counts_and_distributions[-1]
    r_playcounts, c_playcounts = playcounts
    r_dist, c_dist = dist
    assert np.array_equal(r_playcounts, np.array([0, 3]))
    assert np.array_equal(c_playcounts, np.array([0, 2.0, 1.0]))
    assert np.allclose(r_dist, np.array([0.2799721, 0.7200279]))
    assert np.allclose(c_dist, np.array([0.00622156, 0.12100703, 0.87277142]))
    assert len(counts_and_distributions) == iterations + 1
    assert np.sum(r_playcounts) == iterations
    assert np.sum(c_playcounts) == iterations


def test_stochastic_fictitious_play_longrun_default_inputs():
    iterations = 10000
    A = np.array([[1 / 2, 1, 0], [0, 1 / 2, 1], [1, 0, 1 / 2]])
    B = np.array([[1 / 2, 0, 1], [1, 1 / 2, 0], [0, 1, 1 / 2]])
    counts_and_distributions = tuple(
        stochastic_fictitious_play(A=A, B=B, iterations=iterations, seed=0)
    )
    playcounts, dist = counts_and_distributions[-1]
    r_playcounts, c_playcounts = playcounts
    r_dist, c_dist = dist
    assert len(counts_and_distributions) == iterations + 1
    assert np.sum(r_playcounts) == iterations
    assert np.sum(c_playcounts) == iterations
    assert np.allclose(r_dist, np.array([0.34857354, 0.34739881, 0.30402765]))
    assert np.allclose(c_dist, np.array([0.32385877, 0.35455558, 0.32158565]))


def test_bug_reported_by_user():
    """
    This is a bug reported by email.

    Captured here: https://github.com/drvinceknight/Nashpy/issues/214
    """
    A = np.array([[113, 65, 112], [141, 93, -56], [120, 73, -76]])
    B = np.array([[-113, -65, -112], [-141, -93, 56], [-120, -73, 76]])
    iterations = 500
    states = tuple(stochastic_fictitious_play(A=A, B=B, iterations=iterations, seed=0))
    assert len(states) == iterations + 1
    for play_counts, distributions in states[1:]:
        for distribution in distributions:
            assert np.all(np.isfinite(distribution))
            assert np.all(distribution >= 0)
            assert np.isclose(np.sum(distribution), 1)
    for play_count in play_counts:
        assert np.sum(play_count) == iterations
