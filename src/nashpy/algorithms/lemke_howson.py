"""A class for the Lemke Howson algorithm"""

import warnings
from itertools import cycle

import numpy.typing as npt
from typing import Tuple
from nashpy.linalg import create_col_tableau, create_row_tableau


def lemke_howson(
    A: npt.NDArray,
    B: npt.NDArray,
    initial_dropped_label: int = 0,
    lexicographic: bool = True,
) -> Tuple[npt.NDArray, npt.NDArray]:
    """
    Obtain the Nash equilibria using the Lemke Howson algorithm implemented
    using integer pivoting.

    Algorithm implemented here is Algorithm 3.6 of [Nisan2007]_.

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
    A : array
        The row player payoff matrix
    B : array
        The column player payoff matrix
    initial_dropped_label: int
        The initial dropped label.
    lexicographic: bool
        Whether to apply lexicographic sorting during pivoting, default True.
        Lexiographic sorting ensures solutions on degenerate games

    Returns
    -------
    Tuple
        An equilibria
    """
    col_tableau = create_col_tableau(A, lexicographic)
    row_tableau = create_row_tableau(B, lexicographic)

    if initial_dropped_label in row_tableau.non_basic_variables:
        tableux = cycle((row_tableau, col_tableau))
    else:
        tableux = cycle((col_tableau, row_tableau))

    full_labels = col_tableau.labels
    fully_labeled = False
    entering_label = initial_dropped_label
    while not fully_labeled:
        tableau = next(tableux)
        entering_label = tableau.pivot_and_drop_label(entering_label)
        current_labels = col_tableau.non_basic_variables.union(
            row_tableau.non_basic_variables
        )
        fully_labeled = current_labels == full_labels

    row_strat = row_tableau.to_strategy(col_tableau.non_basic_variables)
    col_strat = col_tableau.to_strategy(row_tableau.non_basic_variables)
    if row_strat.shape != (A.shape[0],) and col_strat.shape != (A.shape[0],):
        msg = """The Lemke Howson algorithm has returned probability vectors of·
incorrect shapes. This indicates an error. Your game could be degenerate."""

        warnings.warn(msg, RuntimeWarning)
    return row_strat, col_strat
