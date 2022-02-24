"""
A class for integer pivoting. Used for an implementation of the lemke_howson_lex
algorithm.
"""
import warnings

import numpy as np
import numpy.typing as npt
from typing import Iterable, Any


def find_pivot_row_lex(
    tableau: npt.NDArray, column_index: int, slack_variables: Any
) -> int:

    """
    Find the index of the row to pivot.

    Identifies the row to pivot by finding the first row in a lexicographical
    ordering of rows. (First checks minimum ratio test, then uses lexicographical
    ordering to break ties)

    Lexicographical ordering implementation is described in pg 20 of the text below:
    B. von Stengel (2007), Equilibrium computation for two-player games in strategic
    and extensive form. Chapter 3, Algorithmic Game Theory, eds. N. Nisan, T.
    Roughgarden, E. Tardos, and V. Vazirani, Cambridge Univ. Press, Cambridge, 53-78.
    http://www.maths.lse.ac.uk/personal/stengel/TEXTE/agt-stengel.pdf

    C describes the transformations on the system, as stored by the coefficients of
    the slack variables (which is initially the identity matrix). This is required in
    order to keep track of lexicographical ordering after pivoting.

    Cq is the rightmost column of the tableau, used in the minimum ration test.

    Parameters
    ----------
    tableau : array
        A tableau corresponding to a vertex of a Polytope.
    column_index : int
        The index of a tableau on which to pivot.
    slack_variables : Any
        The iterable of slack variables  # FIX the type hint here to be iterable

    Returns
    -------
    int
        The dropped label.
    """

    # gets correct lexicographical ordering
    C = tableau[:, slack_variables]
    lex_order_reversed = np.lexsort(np.rot90(C))
    lex_order = -lex_order_reversed + lex_order_reversed.shape[0]

    # gets ratio of each row
    pivot_column = tableau[:, column_index]
    Cq = tableau[:, -1]

    # catch divide by zero warning
    with warnings.catch_warnings():
        warnings.filterwarnings(
            "ignore",
            r"invalid value encountered in true_divide|divide by zero encountered in true_divide",
        )

        ratio = np.divide(Cq, pivot_column)

    # filters for column coefficients <=0 (to preserve feasibility)
    filtered_ratio = np.where(pivot_column <= 0, np.full(ratio.shape, np.inf), ratio)

    return np.lexsort(np.flipud((filtered_ratio, lex_order)))[0]


def find_entering_variable(
    tableau: npt.NDArray, pivot_row_index: int, non_basic_variables: set
) -> Any:
    """
    Finds the non-basic variable which becomes basic after pivoting

    Parameters
    ----------
    tableau : array
        A tableau corresponding to a vertex of a Polytope.
    pivot_row_index : int
        The index of the pivot row
    non_basic_variables : set
        The set of non basic variables

    Returns
    -------
    Any
        The integer of the entering variable.
    """

    basic_variables = set(range(tableau.shape[1] - 1)) - non_basic_variables
    for i in basic_variables:
        if tableau[pivot_row_index, i] != 0:
            return i


def pivot_tableau_lex(
    tableau,
    column_index,
    slack_variables,
    non_basic_variables,
):
    """
    Pivots the tableau and returns the dropped label

    Parameters
    ----------
    tableau : array
        A tableau corresponding to a vertex of a Polytope.
    column_index : int
        The index of a tableau on which to pivot.
    slack_variables : iterable
        The collection of slack variables
    non_basic_variables : set
        The set of non basic variables

    Returns
    -------
    int
        The dropped label.
    """
    original_labels = non_basic_variables
    pivot_row_index = find_pivot_row_lex(tableau, column_index, slack_variables)
    pivot_element = tableau[pivot_row_index, column_index]
    entering_variable = find_entering_variable(
        tableau, pivot_row_index, original_labels
    )

    for i, _ in enumerate(tableau):
        if i != pivot_row_index:
            tableau[i, :] = (
                tableau[i, :] * pivot_element
                - tableau[pivot_row_index, :] * tableau[i, column_index]
            )

    return entering_variable
