import itertools

import numpy as np
import nashpy as nash


def obtain_states(A, repetitions, row_player=True):
    """
    Yield all possible states for the row player in a repeated game.

    Parameters
    ----------
    A : array
        2 dimensional list/array representing the payoff
        matrix for the row player in a game.
    repetitions : int
        The number of times to repeat the stage game.
    row_player : bool
        A boolean indicating if this assumes the strategy space is for the row
        player. If False the states are reversed.

    Yields
    ------
    Tuple
        A possible state of play, the first element is a tuple of plays by the
        row player and the second element is a tuple of plays by the column
        player.
    """
    size_row_strategy_space, size_col_strategy_space = A.shape
    for period in range(repetitions):
        for pair in itertools.product(
            itertools.product(
                range(size_row_strategy_space),
                repeat=period,
            ),
            itertools.product(
                range(size_col_strategy_space),
                repeat=period,
            ),
        ):
            if row_player is False:
                pair = pair[1], pair[0]
            yield pair


def obtain_strategy_space(A, repetitions, row_player=True):
    """
    Yield all possible strategies for the row player in a repeated game.

    Parameters
    ----------
    A : array
        2 dimensional list/array representing the payoff
        matrix for the row player in a game.
    repetitions : int
        The number of times to repeat the stage game.
    row_player : bool
        A boolean indicating if this assumes the strategy space is for the row
        player. If False then the transpose of the matrix is used and the states
        are reversed.

    Yields
    ------
    Dict
        A mapping from states of the repeated game to strategies.
    """
    if row_player is False:
        A = A.T
    size_row_strategy_space, size_col_strategy_space = A.shape
    row_strategy_space = np.eye(size_row_strategy_space)
    state_space_size = int(
        (1 - (size_col_strategy_space * size_row_strategy_space) ** (repetitions))
        / (1 - (size_col_strategy_space * size_row_strategy_space))
    )
    for strategy in itertools.product(row_strategy_space, repeat=state_space_size):
        yield {
            state: tuple(action)
            for state, action in zip(
                obtain_states(A=A, repetitions=repetitions, row_player=row_player),
                strategy,
            )
        }


def play_game(game, repetitions, row_strategy, col_strategy):
    """
    Obtain the utilities when repeating the game `game` for `repetitions`
    repetitions as specified by the `row_strategy` and the `col_strategy`.

    Parameters
    ----------
    game : nashpy.Game
           The stage game
    repetitions : int
                  The number of times to play the game
    row_strategy : dict
                  A mapping from all possible histories of play to an action of
                  the row player.
    col_strategy : dict
                  A mapping from all possible histories of play to an action of
                  the column player.

    Returns
    -------
    Tuple
    """
    row_utility, col_utility = 0, 0
    state = ((), ())
    for _ in range(repetitions):
        assert state in row_strategy, f"{state} not in row_strategy: {row_strategy}"
        assert state in col_strategy, f"{state} not in col_strategy: {col_strategy}"
        utilities = game[row_strategy[state], col_strategy[state]]

        row_utility += utilities[0]
        col_utility += utilities[1]
        row_action = row_strategy[state].index(1)
        col_action = col_strategy[state].index(1)
        state = tuple(list(state[0]) + [row_action]), tuple(
            list(state[1]) + [col_action]
        )

    return row_utility, col_utility


def obtain_repeated_game(game, repetitions):
    """
    Obtain a nashpy.Game instance by repeating a given stage game. The rows and
    columns
    correspond to strategies of the repeated game as given by
    `nashpy.learning_games.obtain_strategy_space`.

    Note that the returned game becomes large quickly.

    Parameters
    ----------
    game : nashpy.Game
        A stage game
    repetitions : int
        The number of repetitions of the game.

    Returns
    -------
    nashpy.Game
    """

    A, B = game.payoff_matrices
    repeated_game_row_matrix = []
    repeated_game_col_matrix = []

    for row_strategy in obtain_strategy_space(A=A, repetitions=repetitions):
        row_matrix_row = []
        col_matrix_row = []
        for col_strategy in obtain_strategy_space(
            A=B, repetitions=repetitions, row_player=False
        ):
            row_util, col_util = play_game(
                game=game,
                repetitions=repetitions,
                row_strategy=row_strategy,
                col_strategy=col_strategy,
            )
            row_matrix_row.append(row_util)
            col_matrix_row.append(col_util)
        repeated_game_row_matrix.append(row_matrix_row)
        repeated_game_col_matrix.append(col_matrix_row)

    return nash.Game(repeated_game_row_matrix, repeated_game_col_matrix)
