"""
Tests for functionality to create games from repeated games.
"""
import numpy as np

import nashpy.repeated_games


def test_obtain_states_after_1_repetition_for_2_by_2_game():
    A = np.array([[1, 2], [3, 4]])
    expected_states_after_1_repetition = [((), ())]
    states = list(
        nashpy.repeated_games.obtain_states(row_player_matrix=A, repetitions=1)
    )
    assert expected_states_after_1_repetition == states


def test_obtain_states_after_2_repetitions_for_2_by_2_game():
    A = np.array([[1, 2], [3, 4]])
    expected_states_after_2_repetitions = [
        ((), ()),
        ((0,), (0,)),
        ((0,), (1,)),
        ((1,), (0,)),
        ((1,), (1,)),
    ]
    states = list(
        nashpy.repeated_games.obtain_states(row_player_matrix=A, repetitions=2)
    )
    assert expected_states_after_2_repetitions == states
