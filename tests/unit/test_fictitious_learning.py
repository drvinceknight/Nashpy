"""
Tests for fictitious learning
"""
import types

import numpy as np
from hypothesis import given
from hypothesis.extra.numpy import arrays
from hypothesis.strategies import integers

import nashpy as nash
from nashpy.learning.fictitious_learning import (
    get_best_response_to_belief,
    update_belief,
    fictitious_play,
)


@given(M=arrays(np.int8, (4, 5)))
def test_property_find_best_response_to_belief(M):
    belief = np.zeros(M.shape[1])
    best_response = get_best_response_to_belief(M, belief)
    assert best_response >= 0
    assert best_response <= M.shape[1] - 1
    assert type(best_response) is np.int64


def test_find_best_response_to_belief():
    M = np.array([[3, 2, 3], [4, 1, 1], [2, 3, 1]])
    beliefs = (np.array([1, 0, 0]), np.array([2, 1, 0]), np.array([0, 0, 2]))
    best_responses = (1, 1, 0)
    for belief, expected_best_response in zip(beliefs, best_responses):
        best_response = get_best_response_to_belief(M, belief)
        assert best_response == expected_best_response, belief


@given(play=integers(min_value=0, max_value=9))
def test_property_update_belief(play):
    belief = np.zeros(10)
    updated_belief = update_belief(belief, play)
    assert belief[play] + 1 == updated_belief[play]
    assert np.array_equal(belief[:play], updated_belief[:play])
    assert np.array_equal(belief[play + 1 :], updated_belief[play + 1 :])


@given(
    A=arrays(np.int8, (4, 5)),
    B=arrays(np.int8, (4, 5)),
    iterations=integers(min_value=10, max_value=25),
)
def test_property_fictitious_play(A, B, iterations):
    plays = fictitious_play(A, B, iterations=iterations)
    assert type(plays) is types.GeneratorType
    plays = tuple(plays)
    assert len(plays) == iterations + 1
    assert max(tuple(map(len, plays))) == min(tuple(map(len, plays))) == 2


def test_fictitious_play():
    A = np.array([[1 / 2, 1, 0], [0, 1 / 2, 1], [1, 0, 1 / 2]])
    B = np.array([[1 / 2, 0, 1], [1, 1 / 2, 0], [0, 1, 1 / 2]])
    iterations = 10_000

    np.random.seed(0)
    plays = tuple(fictitious_play(A, B, iterations=iterations))
    assert len(plays) == iterations + 1
    final_row_play, final_column_play = plays[-1]
    assert np.array_equal(final_row_play, [3290, 3320, 3390])

    np.random.seed(1)
    plays = tuple(fictitious_play(A, B, iterations=iterations))
    assert len(plays) == iterations + 1
    final_row_play, final_column_play = plays[-1]
    assert np.array_equal(final_row_play, [3312, 3309, 3379])


# TODO Add test for asymmetric game (to make sure I've got the output order
# correct.
