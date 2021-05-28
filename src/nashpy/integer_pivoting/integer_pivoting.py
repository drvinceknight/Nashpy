"""
A class for integer pivoting. Used for an implementation of the Lemke Howson
algorithm.
"""
import numpy as np


def make_tableau(M):
    """
    Make a tableau for the given matrix M.

    This tableau corresponds to the polytope of the form:

       Mx <= 1 and x >= 0

    Parameters
    ----------
    M : array
        A matrix with linear coefficients defining the polytope.

    Returns
    -------
    array
        The tableau that corresponds to the polytope.
    """
    return np.append(
        np.append(M, np.eye(M.shape[0]), axis=1),
        np.ones((M.shape[0], 1)),
        axis=1,
    )


def find_pivot_row(tableau, column_index):
    """
    Find the index of the row to pivot.

    Identifies the row to pivot by performing a minimum ratio test. (In fact
    implemented to calculate the maximum ratio test to avoid divide by zero
    errors).

    Parameters
    ----------
    tableau : array
        a tableau corresponding to a vertex of a polytope.
    column_index : int
        the index of a tableau on which to pivot.

    Returns
    -------
    int
        The row on which to pivot.
    """
    return np.argmax(tableau[:, column_index] / tableau[:, -1])


def non_basic_variables(tableau):
    """
    Identifies the non basic variables of a tableau,
    these correspond to the labels.

    Parameters
    ----------
    tableau : array
        A tableau corresponding to a vertex of a Polytope.

    Returns
    -------
    set
        The indices of the non basic variables.
    """
    columns = tableau[:, :-1].transpose()
    return set(np.where([np.count_nonzero(col) != 1 for col in columns])[0])


def pivot_tableau(tableau, column_index):
    """
    Pivots the tableau and returns the dropped label

    Parameters
    ----------
    tableau : array
        A tableau corresponding to a vertex of a Polytope.
    column_index : int
        The index of a tableau on which to pivot.

    Returns
    -------
    int
        The dropped label.
    """
    original_labels = non_basic_variables(tableau)
    pivot_row_index = find_pivot_row(tableau, column_index)
    pivot_element = tableau[pivot_row_index, column_index]

    for i, _ in enumerate(tableau):
        if i != pivot_row_index:
            tableau[i, :] = (
                tableau[i, :] * pivot_element
                - tableau[pivot_row_index, :] * tableau[i, column_index]
            )

    return non_basic_variables(tableau) - original_labels
