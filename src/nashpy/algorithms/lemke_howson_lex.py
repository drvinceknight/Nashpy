"""A class for the Lemke Howson algorithm with lexicographical ordering"""
import warnings
from itertools import cycle

import numpy as np

from nashpy.integer_pivoting import (
    make_tableau,
    non_basic_variables,
    zero_basic_variables,
    pivot_tableau_lex,
)
from .lemke_howson import shift_tableau, tableau_to_strategy


def lemke_howson_lex(A, B, initial_dropped_label=0):
    """
	Obtain the Nash equilibria using the Lemke Howson algorithm implemented
	using integer pivoting.

	1. Start at the artificial equilibrium (which is fully labeled)
	2. Choose an initial label to drop and move in the polytope for which
	   the vertex has that label to the edge
	   that does not share that label. (This is implemented using integer
	   pivoting)
	3. A label will now be duplicated in the other polytope, drop it in a
	   similar way.
	4. Repeat steps 2 and 3 until have Nash Equilibrium.

	Parameters
	----------

		initial_dropped_label: int

	Returns
	-------

		equilibria: A tuple.

	========

		* Edited such that zero basic variables are considered in nash equilibrium 
		and integer pivoting is done using lexicographical ordering

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

    if initial_dropped_label in non_basic_variables(row_tableau):
        tableux = cycle(
            (
                (row_tableau, row_slack_variables),
                (col_tableau, col_slack_variables),
            )
        )
    else:
        tableux = cycle(
            (
                (col_tableau, col_slack_variables),
                (row_tableau, row_slack_variables),
            )
        )

    # First pivot (to drop a label)
    next_tableau = next(tableux)
    entering_label = pivot_tableau_lex(
        next_tableau[0], initial_dropped_label, next_tableau[1]
    )
    while (
        non_basic_variables(row_tableau).union(
            non_basic_variables(col_tableau),
            zero_basic_variables(row_tableau),
            zero_basic_variables(col_tableau),
        )
        != full_labels
    ):
        next_tableau = next(tableux)

        # error handling to deal with games that are 'too degenerate(?)'
        try:
            entering_label = pivot_tableau_lex(
                next_tableau[0], next(iter(entering_label)), next_tableau[1]
            )
        except StopIteration:
            msg = """The algorithm has not found a new label after pivoting. 
			This indicates an error. Your game could be degenerate."""
            warnings.warn(msg, RuntimeWarning)
            raise Exception("No new label found. Terminating algorithm.")

    row_strategy = tableau_to_strategy(
        row_tableau,
        full_labels
        - non_basic_variables(row_tableau)
        - zero_basic_variables(row_tableau),
        range(A.shape[0]),
    )
    col_strategy = tableau_to_strategy(
        col_tableau,
        full_labels
        - non_basic_variables(col_tableau)
        - zero_basic_variables(col_tableau),
        range(A.shape[0], sum(A.shape)),
    )

    if row_strategy.shape != (A.shape[0],) and col_strategy.shape != (
        A.shape[0],
    ):
        msg = """The Lemke Howson algorithm has returned probability vectors of 
incorrect shapes. This indicates an error. Your game could be degenerate."""

        warnings.warn(msg, RuntimeWarning)
    return row_strategy, col_strategy
