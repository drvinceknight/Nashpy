"""
Tests for stochastic fictitious learning
"""
import types

import numpy as np
from hypothesis import given
from hypothesis.extra.numpy import arrays
from hypothesis.strategies import integers

import nashpy as nash
from nashpy.learning.stochastic_fictitious_play import (
    get_distribution_response_to_play_count,
    stochastic_fictitious_play,
)


def test_first():
    x = 4 + 5
    assert x == 9


@given(M=arrays(np.int8, (2, 2)))
def test_property_get_distribution_response_to_play_count(M):
    etha = 2
    epsilon_bar = 2
    play_count = np.ones(M.shape[1])
    distribution_response = get_distribution_response_to_play_count(
        M, play_count, epsilon_bar, etha
    )
    assert len(distribution_response) == len(play_count)
    assert np.all(distribution_response) >= 0
    assert np.isclose(np.sum(distribution_response), 1)


# def test_get_distribution_response_to_play_count_1():
#    np.random.seed(3)
#    M = np.array([[1, -1], [-1, 1]])
#    play_count = np.array([1, 1])
#    etha = 2
#    epsilon_bar = 2
#
#    expected_distribution = np.array([0.44126619, 0.55873381])
#    distribution_response = get_distribution_response_to_play_count(
#        A=M, play_count=play_count, epsilon_bar=epsilon_bar, etha=etha
#    )
#    assert np.allclose(distribution_response, expected_distribution)


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
    # assert np.isclose(np.sum(distribution_response), 1)


# def test_stochastic_fictitious_play():
#    np.random.seed(0)
#    M = np.array([[3, 2], [7, 6]])
#    iterations = 3
#    etha = 2
#    epsilon_bar = 2
#    play_count = [40, 30]
#    apple = tuple(
#        stochastic_fictitious_play(
#            A=M,
#            B=-M,
#            iterations=iterations,
#            play_counts=play_count,
#            etha=etha,
#            epsilon_bar=epsilon_bar,
#        )
#    )
#    final_row_play, final_col_play = play_counts[-1]
#    assert np.array_equal(final_row_play, [41, 30])


def test_stochastic_fictitious_play():
    np.random.seed(0)
    iterations = 3
    M = np.array([[3, 2], [7, 6]])
    etha = 2
    epsilon_bar = 2
    x = tuple(
        stochastic_fictitious_play(
            A=M, B=-M, etha=etha, epsilon_bar=epsilon_bar, iterations=iterations
        )
    )
    playcounts, dist = x[-1]
    r_playcounts, c_playcounts = playcounts
    r_dist, c_dist = dist
    assert np.array_equal(playcounts, [np.array([2.0, 3.0]), np.array([1.0, 4.0])])
    assert np.array_equal(r_playcounts, np.array([2.0, 3.0]))
    assert np.allclose(r_dist, np.array([0.08646736, 0.91353264]))
    assert np.allclose(c_dist, np.array([0.37376622, 0.62623378]))
