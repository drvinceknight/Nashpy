import itertools


def obtain_states(A, repetitions):
    """
    Yield all possible states for the row player in a repeated game.

    Parameters
    ----------
    - A : array
          2 dimensional list/array representing the payoff
          matrix for the row player in a game.
    """
    size_row_strategy_space, size_col_strategy_space = row_player_matrix.shape
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
