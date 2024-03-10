"""
This module contains
"""

import numpy as np
import numpy.typing as npt
import scipy.optimize


def get_c(number_of_rows: int) -> npt.NDArray:
    """
    Return the coefficient vector for the objective function of the LP that
    corresponds to the minimax theorem.

    Parameters
    ----------
    number_of_rows : int
        The number of rows in the payoff matrix
    Returns
    -------
    array
        A vector with m 0s followed by a single 1 where m is the number of rows
        in the payoff matrix.
    """
    c = np.zeros(shape=(number_of_rows + 1))
    c[-1] = -1
    return c


def get_A_ub(row_player_payoff_matrix: npt.NDArray) -> npt.NDArray:
    """
    Return the upper bound linear matrix for the objective function of the LP
    that corresponds to the minimax theorem.

    Parameters
    ----------
    row_player_payoff_matrix : array
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


def get_bounds(number_of_rows: int) -> list:
    """
    Return the bounds for each variable the LP that corresponds to the
    minimax theorem.

    Parameters
    ----------
    number_of_rows : int
        The number of rows in the payoff matrix
    Returns
    -------
    list
        A list of tuples, each tuple contains the lower and upper bound for each
        variable.
    """
    return [(0, None) for _ in range(number_of_rows)] + [(None, None)]


def linear_program(row_player_payoff_matrix: npt.NDArray) -> npt.NDArray:
    """
    The Linear Program that corresponds to the minimax theorem. This builds and
    returns the row players' strategy.

    Parameters
    ----------
    row_player_payoff_matrix : array
        The payoff matrix
    Returns
    -------
    array
        The row player maxmin strategy
    """
    number_of_rows, number_of_columns = row_player_payoff_matrix.shape
    c = get_c(number_of_rows=number_of_rows)
    A_ub = get_A_ub(row_player_payoff_matrix=row_player_payoff_matrix)
    b_ub = get_b_ub(number_of_columns=number_of_columns)
    A_eq = get_A_eq(number_of_rows=number_of_rows)
    b_eq = 1
    bounds = get_bounds(number_of_rows=number_of_rows)

    res = scipy.optimize.linprog(
        c=c,
        A_ub=A_ub,
        b_ub=b_ub,
        A_eq=A_eq,
        b_eq=b_eq,
        bounds=bounds,
    )
    return res.x[:-1]
