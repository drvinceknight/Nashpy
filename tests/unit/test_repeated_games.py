"""
Tests for functionality to create games from repeated games.
"""

import numpy as np

import nashpy as nash
import nashpy.repeated_games


def test_obtain_states_after_1_repetition_for_2_by_2_game():
    A = np.array([[1, 2], [3, 4]])
    expected_states_after_1_repetition = [((), ())]
    states = list(nashpy.repeated_games.obtain_states(A=A, repetitions=1))
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
    states = list(nashpy.repeated_games.obtain_states(A=A, repetitions=2))
    assert expected_states_after_2_repetitions == states


def test_obtain_states_after_2_repetitions_for_2_by_3_game():
    A = np.array([[1, 2, 3], [4, 5, 6]])
    expected_states_after_2_repetitions = [
        ((), ()),
        ((0,), (0,)),
        ((0,), (1,)),
        ((0,), (2,)),
        ((1,), (0,)),
        ((1,), (1,)),
        ((1,), (2,)),
    ]
    states = list(nashpy.repeated_games.obtain_states(A=A, repetitions=2))
    assert expected_states_after_2_repetitions == states


def test_obtain_states_after_2_repetitions_for_3_by_2_game():
    B = np.array([[1, 2, 3], [4, 5, 6]])
    expected_states_after_2_repetitions = [
        ((), ()),
        ((0,), (0,)),
        ((0,), (1,)),
        ((1,), (0,)),
        ((1,), (1,)),
        ((2,), (0,)),
        ((2,), (1,)),
    ]
    states = list(nashpy.repeated_games.obtain_states(A=B.T, repetitions=2))
    assert expected_states_after_2_repetitions == states


def test_obtain_strategy_space_after_1_repetition_for_2_by_2_game():
    A = np.array([[1, 2, 3], [4, 5, 6]])
    expected_strategy_space = [{((), ()): (1.0, 0.0)}, {((), ()): (0.0, 1.0)}]
    strategy_space = list(
        nashpy.repeated_games.obtain_strategy_space(A=A, repetitions=1)
    )
    assert expected_strategy_space == strategy_space


def test_obtain_strategy_space_after_2_repetition_for_2_by_3_game():
    """
    This tests that the output is of the expected format: a dictionary of the
    right size (in the case of a 2 by 3 game repeated twice this is

    128 = 2 ^ (1 + 2 * 3)

    The size of the state space is 1 + 2 * 3. There are two options for each of
    the states giving 128.
    """
    A = np.array([[1, 2, 3], [4, 5, 6]])
    repetitions = 2
    count = 0
    states = sorted(
        list(nashpy.repeated_games.obtain_states(A=A, repetitions=repetitions))
    )
    for strategy in nashpy.repeated_games.obtain_strategy_space(
        A=A, repetitions=repetitions
    ):
        assert sorted(strategy.keys()) == states
        count += 1
    assert count == 128


def test_obtain_strategy_space_after_2_repetition_for_3_by_2_game():
    """
    This tests that the output is of the expected format: a dictionary of the
    right size (in the case of a 2 by 3 game repeated twice this is

    2187 = 3 ^ (1 + 2 * 3)

    The size of the state space is 1 + 2 * 3. There are three options for each of
    the states giving 2187
    """
    B = np.array([[1, 2, 3], [4, 5, 6]])
    repetitions = 2
    count = 0
    states = sorted(
        list(nashpy.repeated_games.obtain_states(A=B.T, repetitions=repetitions))
    )
    for strategy in nashpy.repeated_games.obtain_strategy_space(
        A=B.T, repetitions=repetitions
    ):
        assert sorted(strategy.keys()) == states
        count += 1
    assert count == 2187


def test_play_game_with_1_repetitions_for_2_by_2_game():
    A = np.array([[0, 1], [2, 3]])
    game = nash.Game(A)
    expected_utilities = (1.0, -1.0)
    utilities = nashpy.repeated_games.play_game(
        game,
        repetitions=1,
        row_strategy={((), ()): (1.0, 0.0)},
        col_strategy={((), ()): (0, 1)},
    )
    assert expected_utilities == utilities


def test_play_game_with_2_repetitions_for_2_by_2_game():
    A = np.array([[0, 11], [-22, 3]])
    B = np.array([[2, 1], [-2, -3]])
    game = nash.Game(A, B)
    expected_utilities = (22.0, 2.0)
    utilities = nashpy.repeated_games.play_game(
        game=game,
        repetitions=2,
        row_strategy={
            ((), ()): (1.0, 0.0),
            ((0,), (0,)): (1.0, 0.0),
            ((1,), (0,)): (1.0, 0.0),
            ((0,), (1,)): (1.0, 0.0),
            ((1,), (1,)): (1.0, 0.0),
        },
        col_strategy={
            ((), ()): (0.0, 1.0),
            ((0,), (0,)): (0.0, 1.0),
            ((1,), (0,)): (1.0, 0.0),
            ((0,), (1,)): (0, 1.0),
            ((1,), (1,)): (1.0, 0.0),
        },
    )
    assert expected_utilities == utilities


def test_play_game_with_2_repetitions_for_3_by_2_game():
    A = np.array([[0, 11], [-22, 3], [0, 0]])
    B = np.array([[2, 1], [-2, -3], [1, 2]])
    game = nash.Game(A, B)
    expected_utilities = (22.0, 2.0)
    utilities = nashpy.repeated_games.play_game(
        game=game,
        repetitions=2,
        row_strategy={
            ((), ()): (1.0, 0.0, 0.0),
            ((0,), (0,)): (1.0, 0.0, 0.0),
            ((1,), (0,)): (1.0, 0.0, 0.0),
            ((2,), (0,)): (1.0, 0.0, 0.0),
            ((0,), (1,)): (1.0, 0.0, 0.0),
            ((1,), (1,)): (1.0, 0.0, 0.0),
            ((2,), (1,)): (1.0, 0.0, 0.0),
        },
        col_strategy={
            ((), ()): (0.0, 1.0),
            ((0,), (0,)): (0.0, 1.0),
            ((1,), (0,)): (1.0, 0.0),
            ((2,), (0,)): (1.0, 0.0),
            ((0,), (1,)): (0, 1.0),
            ((1,), (1,)): (1.0, 0.0),
            ((2,), (1,)): (1.0, 0.0),
        },
    )
    assert expected_utilities == utilities


def test_get_repeated_game_with_2_by_2_stage_game():
    """
    Checks the dimension of a repeated game.

    TODO More tests needed to check actual value of game.
    """
    A = np.array([[0, 11], [-22, 3]])
    B = np.array([[2, 1], [-2, -3]])
    stage_game = nash.Game(A, B)
    repetitions = 2
    repeated_game = nashpy.repeated_games.obtain_repeated_game(
        game=stage_game, repetitions=repetitions
    )
    new_dimension = repeated_game.payoff_matrices[0].shape
    assert new_dimension == (32, 32)


def test_get_repeated_game_with_2_by_3_stage_game():
    """
    Checks the dimension of a repeated game.

    The expected number of rows is:

    2 ^ (1 + 2 * 3) (there are 7 possible histories, for each there are two
                     possible actions)

    The expected number of columns is:

    3 ^ (1 + 2 * 3) (there are 7 possible histories, for each there are two
                     possible actions)

    TODO More tests needed to check actual value of game.
    """
    A = np.array([[0, 11, 5], [-22, 3, 4]])
    B = np.array([[2, 1, 2], [-2, -3, 6]])
    stage_game = nash.Game(A, B)
    repetitions = 2
    repeated_game = nashpy.repeated_games.obtain_repeated_game(
        game=stage_game, repetitions=repetitions
    )
    new_dimension = repeated_game.payoff_matrices[0].shape
    assert new_dimension == (128, 2187)
