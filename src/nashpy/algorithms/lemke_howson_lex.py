"""A class for the Lemke Howson algorithm with lexicographical ordering"""
from itertools import cycle

import numpy as np

from nashpy.integer_pivoting import make_tableau, pivot_tableau_lex

from .lemke_howson import shift_tableau, tableau_to_strategy


def lemke_howson_lex(A, B, initial_dropped_label=0):
    """
     Obtain the Nash equilibria using the Lemke Howson algorithm implemented
     using lexicographical integer pivoting. (Able to solve degenerate games)

     1. Start at the artificial equilibrium (which is fully labeled)
     2. Choose an initial label to drop and move in the polytope for which
        the vertex has that label to the edge that does not share that label.
    (This is implemented using integer pivoting and the choice of label
    to drop is implemented using lexicographical ordering)
     3. A label will now be duplicated in the other polytope, drop it in a
        similar way.
     4. Repeat steps 2 and 3 until have Nash Equilibrium.

    Parameters
    ----------
    A : array
        The row player payoff matrix
    B : array
        The column player payoff matrix
    initial_dropped_label: int
        The initial dropped label.

    Returns
    -------
    Tuple
        An equilibria
    """

    if np.min(A) <= 0:
        A = A + abs(np.min(A)) + 1
    if np.min(B) <= 0:
        B = B + abs(np.min(B)) + 1

    # build tableaux
    col_tableau = make_tableau(A)
    col_tableau = shift_tableau(col_tableau, A.shape)
    row_tableau = make_tableau(B.transpose())
    full_labels = set(range(sum(A.shape)))

    # slack variables
    row_slack_variables = range(B.shape[0], sum(B.shape))
    col_slack_variables = range(A.shape[0])

    # non-basic variables
    row_non_basic_variables = full_labels - set(row_slack_variables)
    col_non_basic_variables = full_labels - set(col_slack_variables)

    # print(initial_dropped_label)
    if initial_dropped_label in row_non_basic_variables:
        tableaux = cycle(
            (
                (row_tableau, row_slack_variables, row_non_basic_variables),
                (col_tableau, col_slack_variables, col_non_basic_variables),
            )
        )
    else:
        tableaux = cycle(
            (
                (col_tableau, col_slack_variables, col_non_basic_variables),
                (row_tableau, row_slack_variables, row_non_basic_variables),
            )
        )

    # First pivot (to drop a label)
    next_tableau, next_slack_variables, next_non_basic_variables = next(tableaux)

    entering_label = pivot_tableau_lex(
        next_tableau,
        initial_dropped_label,
        next_slack_variables,
        next_non_basic_variables,
    )

    # keeps track of each tableau's non-basic variables
    next_non_basic_variables.add(entering_label)
    next_non_basic_variables.remove(initial_dropped_label)

    while col_non_basic_variables.union(row_non_basic_variables) != full_labels:
        next_tableau, next_slack_variables, next_non_basic_variables = next(tableaux)

        # the first label is 'entering' in the sense that it will enter the next
        # tableau's set of basic variables
        just_entered_label = entering_label
        entering_label = pivot_tableau_lex(
            next_tableau,
            entering_label,
            next_slack_variables,
            next_non_basic_variables,
        )

        next_non_basic_variables.add(entering_label)
        next_non_basic_variables.remove(just_entered_label)

    row_strategy = tableau_to_strategy(
        row_tableau,
        full_labels - row_non_basic_variables,
        range(A.shape[0]),
    )

    col_strategy = tableau_to_strategy(
        col_tableau,
        full_labels - col_non_basic_variables,
        range(A.shape[0], sum(A.shape)),
    )

    return row_strategy, col_strategy
