"""A class for the Lemke Howson algorithm with lexicographical ordering"""

from deprecated import deprecated  # type: ignore
import numpy.typing as npt
from typing import Tuple

from .lemke_howson import lemke_howson


@deprecated(
    version="0.0.38",
    reason="Standard lemke_howson function now supports lex sort, this class will be removed soon",
)
def lemke_howson_lex(
    A: npt.NDArray, B: npt.NDArray, initial_dropped_label: int = 0
) -> Tuple[npt.NDArray, npt.NDArray]:
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
    return lemke_howson(A, B, initial_dropped_label, True)
