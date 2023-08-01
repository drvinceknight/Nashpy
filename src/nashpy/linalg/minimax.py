"""
This module contains
"""
import numpy.typing as npt
import numpy as np


def get_c(number_of_rows: int) -> npt.NDArray:
    """
    Return the coefficient vector for the objective function of the LP that
    corresponds to the minimax theorem.

    Parameters
    ----------
    number_of_rows : array
        The number of rows in the payoff matrix
    Returns
    -------
    array
        A vector with m 0s followed by a single 1 where m is the number of rows
        in the payoff matrix.
    """
    return np.zeros(shape=(number_of_rows + 1))


def get_A_ub(row_player_payoff_matrix: npt.NDArray) -> npt.NDArray:
    """
    Return the upper bound linear matrix for the objective function of the LP
    that corresponds to the minimax theorem.

    Parameters
    ----------
    the row_player_payoff_matrix : array
        The payoff matrix
    Returns
    -------
    array
        A matrix that corresponds to the upper bound.
    """
    _, number_of_columns = row_player_payoff_matrix.shape
    return np.hstack(
        (-row_player_payoff_matrix.T, np.ones(shape=(number_of_columns, 1)))
    )


def get_b_ub(number_of_columns: int) -> npt.NDArray:
    """
    Return the upper bound vector for the LP that corresponds to the minimax
    theorem.

    Parameters
    ----------
    number_of_columns : int
        The number of columns in the payoff matrix
    Returns
    -------
    array
        A vector of zeros
    """
    return np.zeros(shape=(number_of_columns, 1))


def get_A_eq(number_of_rows: int) -> npt.NDArray:
    """
    Return the equality linear coefficients for the LP that corresponds to the
    minimax theorem.

    Parameters
    ----------
    number_of_rows : int
        The number of rows in the payoff matrix
    Returns
    -------
    array
        A vector with m 1s followed by a single 0 where m is the number of rows
        in the payoff matrix.
    """
    A_eq = np.ones(shape=(1, number_of_rows + 1))
    A_eq[0, -1] = 0
    return A_eq
