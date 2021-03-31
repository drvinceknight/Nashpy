"""
Tests for stochastic fictitious learning
"""
import numpy as np
from hypothesis import given
from hypothesis.extra.numpy import arrays

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
    np.random.seed(0)
    M = np.array([[3, 2], [7, 6]])
    etha = 2
    epsilon_bar = 2
    play_count = [40, 30]
    expected_distribution = np.array([0.1028108461, 0.8971891539])
    distribution_response = get_distribution_response_to_play_count(
        A=M, play_count=play_count, epsilon_bar=epsilon_bar, etha=etha
    )
    assert np.allclose(distribution_response, expected_distribution)
    assert np.sum(distribution_response) == 1


def test_get_distribution_response_to_play_count_3():
    np.random.seed(0)
    M = np.array([[3, 2], [7, 6]])
    etha = 0.2
    epsilon_bar = 0.05
    play_count = np.array([0, 0])
    r_dist = get_distribution_response_to_play_count(
        A=M, play_count=play_count, epsilon_bar=epsilon_bar, etha=etha
    )
    assert np.allclose(r_dist, np.array([1.97718056e-09, 9.99999998e-01]))

    c_dist = get_distribution_response_to_play_count(
        A=M.transpose(),
        play_count=play_count,
        epsilon_bar=epsilon_bar,
        etha=etha,
    )
    assert np.allclose(c_dist, np.array([0.99340266, 0.00659734]))


def test_stochastic_fictitious_play_given_etha_epsilon():
    np.random.seed(0)
    iterations = 1
    M = np.array([[3, 2], [7, 6]])
    etha = 0.2
    epsilon_bar = 0.05
    counts_and_distributions = tuple(
        stochastic_fictitious_play(
            A=M, B=-M, etha=etha, epsilon_bar=epsilon_bar, iterations=iterations
        )
    )
    playcounts, dist = counts_and_distributions[1]
    r_playcounts, c_playcounts = playcounts
    r_dist, c_dist = dist
    assert np.array_equal(playcounts, [np.array([0, 1.0]), np.array([0, 1.0])])
    assert np.array_equal(r_playcounts, np.array([0, 1.0]))
    assert np.allclose(r_dist, np.array([1.97718056e-09, 9.99999998e-01]))
    assert len(counts_and_distributions) == 2
    assert np.allclose(c_dist, np.array([0.00678974, 0.99321026]))


def test_stochastic_fictitious_play_default_inputs():
    np.random.seed(0)
    iterations = 3
    M = np.array([[3, 2], [7, 6]])
    counts_and_distributions = tuple(
        stochastic_fictitious_play(A=M, B=-M, iterations=iterations)
    )
    playcounts, dist = counts_and_distributions[-1]
    r_playcounts, c_playcounts = playcounts
    r_dist, c_dist = dist
    assert np.array_equal(playcounts, [np.array([0, 3]), np.array([0, 3])])
    assert np.allclose(r_dist, np.array([4.09913701e-18, 1.00000000e00]))
    assert np.allclose(c_dist, np.array([4.53248709e-05, 9.99954675e-01]))
    assert len(counts_and_distributions) == 4
    assert np.sum(playcounts) == 2 * iterations


def test_stochastic_fictitious_play_2x3():
    np.random.seed(0)
    iterations = 3
    M = np.array([[3, 2, -2], [7, -2, 6]])
    N = np.array([[2, -2, 3], [-4, 2, 6]])
    etha = 2
    epsilon_bar = 0.2
    counts_and_distributions = tuple(
        stochastic_fictitious_play(
            A=M, B=N, etha=etha, epsilon_bar=epsilon_bar, iterations=iterations
        )
    )
    playcounts, dist = counts_and_distributions[-1]
    r_playcounts, c_playcounts = playcounts
    r_dist, c_dist = dist
    assert np.array_equal(r_playcounts, np.array([0, 3]))
    assert np.array_equal(c_playcounts, np.array([0, 0, 3.0]))
    assert np.allclose(r_dist, np.array([0.01795781, 0.98204219]))
    assert np.allclose(c_dist, np.array([0.00546793, 0.11912101, 0.87541106]))
    assert len(counts_and_distributions) == iterations + 1
    assert np.sum(r_playcounts) == iterations
    assert np.sum(c_playcounts) == iterations


def test_stochastic_fictitious_play_longrun_default_inputs():
    np.random.seed(0)
    iterations = 10000
    A = np.array([[1 / 2, 1, 0], [0, 1 / 2, 1], [1, 0, 1 / 2]])
    B = np.array([[1 / 2, 0, 1], [1, 1 / 2, 0], [0, 1, 1 / 2]])
    counts_and_distributions = tuple(
        stochastic_fictitious_play(A=A, B=B, iterations=iterations)
    )
    playcounts, dist = counts_and_distributions[-1]
    r_playcounts, c_playcounts = playcounts
    r_dist, c_dist = dist
    assert len(counts_and_distributions) == iterations + 1
    assert np.sum(r_playcounts) == iterations
    assert np.sum(c_playcounts) == iterations
    assert np.allclose(r_dist, np.array([0.35888645, 0.32741658, 0.31369697]))
    assert np.allclose(c_dist, np.array([0.30257911, 0.3463743, 0.35104659]))
