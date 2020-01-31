"""
A class for integer pivoting. Used for an implementation of the Lemke Howson
algorithm.
"""
import numpy as np

import warnings


def make_tableau(M):
    """
    Make a tableau for the given matrix M.

    This tableau corresponds to the polytope of the form:

       Mx <= 1 and x >= 0
    """
    return np.append(
        np.append(M, np.eye(M.shape[0]), axis=1), np.ones((M.shape[0], 1)), axis=1,
    )


def find_pivot_row_lex(tableau, column_index, slack_variables):

    """
    Find the index of the row to pivot.

    Identifies the row to pivot by finding the first fow in a lexicographical 
    ordering of rows. (First checks minimum ratio test, then uses lexicographical
     ordering to break ties)
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
        warnings.filterwarnings("ignore", r"invalid value encountered in true_divide")

        ratio = np.divide(Cq, pivot_column)

    # filters for column coefficients <=0 (to preserve feasibility)
    filtered_ratio = np.where(pivot_column <= 0, np.full(ratio.shape, np.inf), ratio)

    return np.lexsort(np.flipud((filtered_ratio, lex_order)))[0]


def non_basic_variables(tableau):
    """
    Identifies the non basic variables of a tableau,
    these correspond to the labels.
    """
    columns = tableau[:, :-1].transpose()
    return set(np.where([np.count_nonzero(col) != 1 for col in columns])[0])


def zero_basic_variables(tableau):
    """
    Identifies basic variables equal to 0.
    Needed to find solutions of degenerate games
    """

    Cq = tableau[:, -1]
    zero_rows = set(np.where(Cq == 0)[0])
    basic_variables = set(range(tableau.shape[1] - 1)) - non_basic_variables(tableau)

    # gives list of pairs (basic_col_index, non-zero row index)
    basic_variable_rows = [
        (col, np.where(tableau[:, col] != 0)[0][0]) for col in basic_variables
    ]
    return set(
        map(lambda x: x[0], filter(lambda x: x[1] in zero_rows, basic_variable_rows))
    )


def pivot_tableau_lex(tableau, column_index, slack_variables):
    """
    Pivots the tableau and returns the dropped label
    """
    original_labels = non_basic_variables(tableau)
    pivot_row_index = find_pivot_row_lex(tableau, column_index, slack_variables)
    pivot_element = tableau[pivot_row_index, column_index]

    for i, _ in enumerate(tableau):
        if i != pivot_row_index:
            tableau[i, :] = (
                tableau[i, :] * pivot_element
                - tableau[pivot_row_index, :] * tableau[i, column_index]
            )

    return non_basic_variables(tableau) - original_labels
