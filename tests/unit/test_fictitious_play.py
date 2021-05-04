"""
Tests for fictitious learning
"""
import types

import numpy as np
from hypothesis import given
from hypothesis.extra.numpy import arrays
from hypothesis.strategies import integers

from nashpy.learning.fictitious_play import (
    fictitious_play,
    get_best_response_to_play_count,
    update_play_count,
)


@given(M=arrays(np.int8, (4, 5)))
def test_property_find_best_response_to_play_count(M):
    play_count = np.zeros(M.shape[1])
    best_response = get_best_response_to_play_count(M, play_count)
    assert best_response >= 0
    assert best_response <= M.shape[1] - 1


def test_find_best_response_to_play_count():
    M = np.array([[3, 2, 3], [4, 1, 1], [2, 3, 1]])
    play_counts = (
        np.array([1, 0, 0]),
        np.array([2, 1, 0]),
        np.array([0, 0, 2]),
    )
    best_responses = (1, 1, 0)
    for play_count, expected_best_response in zip(play_counts, best_responses):
        best_response = get_best_response_to_play_count(M, play_count)
        assert best_response == expected_best_response, play_count


@given(play=integers(min_value=0, max_value=9))
def test_property_update_belief(play):
    play_count = np.zeros(10)
    updated_play_count = update_play_count(play_count, play)
    assert play_count[play] + 1 == updated_play_count[play]
    assert np.array_equal(play_count[:play], updated_play_count[:play])
    assert np.array_equal(play_count[play + 1 :], updated_play_count[play + 1 :])


@given(
    A=arrays(np.int8, (4, 5)),
    B=arrays(np.int8, (4, 5)),
    iterations=integers(min_value=10, max_value=25),
)
def test_property_fictitious_play(A, B, iterations):
    play_counts = fictitious_play(A, B, iterations=iterations)
    assert isinstance(play_counts, types.GeneratorType)
    play_counts = tuple(play_counts)
    assert len(play_counts) == iterations + 1
    assert max(tuple(map(len, play_counts))) == min(tuple(map(len, play_counts))) == 2


def test_fictitious_play():
    A = np.array([[1 / 2, 1, 0], [0, 1 / 2, 1], [1, 0, 1 / 2]])
    B = np.array([[1 / 2, 0, 1], [1, 1 / 2, 0], [0, 1, 1 / 2]])
    iterations = 10000

    np.random.seed(0)
    play_counts = tuple(fictitious_play(A, B, iterations=iterations))
    assert len(play_counts) == iterations + 1
    final_row_play, final_column_play = play_counts[-1]
    assert np.array_equal(final_row_play, [3290, 3320, 3390])

    np.random.seed(1)
    play_counts = tuple(fictitious_play(A, B, iterations=iterations))
    assert len(play_counts) == iterations + 1
    final_row_play, final_column_play = play_counts[-1]
    assert np.array_equal(final_row_play, [3312, 3309, 3379])


def test_fictitious_play_with_asymetric_game_and_initial_play_counts():
    A = np.array([[1 / 2, 2, 0, 0], [0, 1 / 2, 1, 1], [1, 0, 1 / 2, 0]])
    B = np.array([[1 / 2, 0, 1 / 2, 1], [1 / 2, 1 / 2, 0, 1], [0, 1, 1 / 2, 2]])
    iterations = 10000
    play_counts = tuple(
        fictitious_play(
            A,
            B,
            iterations=iterations,
            play_counts=(np.array([1, 0, 0]), np.array([0, 0, 1, 0])),
        )
    )
    final_row_play, final_column_play = play_counts[-1]
    assert np.array_equal(final_row_play, [1, iterations, 0])
    assert np.array_equal(final_column_play, [0, 0, 1, iterations])
