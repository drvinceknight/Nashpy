import itertools

import numpy as np


def obtain_states(A, repetitions):
    """
    Yield all possible states for the row player in a repeated game.

    Parameters
    ----------
    A : array
        2 dimensional list/array representing the payoff
        matrix for the row player in a game.
    repetitions : int
        The number of times to repeat the stage game.

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
            yield pair


def obtain_strategy_space(A, repetitions):
    """
    Yield all possible states for the row player in a repeated game.

    Parameters
    ----------
    A : array
        2 dimensional list/array representing the payoff
        matrix for the row player in a game.
    repetitions : int
        The number of times to repeat the stage game.

    Yields
    ------
    Dict
        A mapping from states of the repeated game to strategies.
    """
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
                obtain_states(A=A, repetitions=repetitions),
                strategy,
            )
        }
