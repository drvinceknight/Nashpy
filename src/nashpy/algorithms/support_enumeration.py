"""A class for a normal form game"""

import warnings
from itertools import chain, combinations
from math import comb

import numpy as np
import numpy.typing as npt
from typing import Generator, Any, Iterator, Tuple, Union


def powerset(n: int) -> Iterator[Tuple[Any, ...]]:
    """
    A power set of range(n)

    Based on recipe from python itertools documentation:

    https://docs.python.org/2/library/itertools.html#recipes

    Parameters
    ----------
    n : int
        The defining parameter of the powerset.

    Returns
    -------
    Iterator
        The powerset
    """
    return chain.from_iterable(combinations(range(n), r) for r in range(n + 1))


def solve_indifference(A, rows=None, columns=None) -> Union[bool, Any]:
    """
    Solve the indifference for a payoff matrix assuming support for the
    strategies given by columns

    Finds vector of probabilities that makes player indifferent between
    rows.  (So finds probability vector for corresponding column player)

    Parameters
    ----------
    A : array
        The row player utility matrix.
    rows : array
        Array of integers corresponding to rows to consider.
    columns : array
        Array of integers corresponding to columns to consider.

    Returns
    -------
    Union
        The solution to the indifference equations.
    """
    # Ensure differences between pairs of pure strategies are the same
    M = (A[np.array(rows)] - np.roll(A[np.array(rows)], 1, axis=0))[:-1]
    # Columns that must be played with prob 0
    zero_columns = set(range(A.shape[1])) - set(columns)

    if zero_columns != set():
        M = np.append(
            M,
            [[int(i == j) for i, col in enumerate(M.T)] for j in zero_columns],
            axis=0,
        )

    # Ensure have probability vector
    M = np.append(M, np.ones((1, M.shape[1])), axis=0)
    b = np.append(np.zeros(len(M) - 1), [1])

    try:
        prob = np.linalg.solve(M, b)
        if all(prob >= 0):
            return prob
        return False
    except np.linalg.LinAlgError:
        return False


def potential_support_pairs(
    A: npt.NDArray, B: npt.NDArray, non_degenerate: bool = False
) -> Generator[tuple, Any, None]:
    """
    A generator for the potential support pairs


    Parameters
    ----------
    A : array
        The row player utility matrix.
    B : array
        The column player utility matrix
    non_degenerate : bool
        Whether or not to consider supports of equal size. By default
        (False) only considers supports of equal size.

    Yields
    -------
    Generator
        A pair of possible supports.
    """
    p1_num_strategies, p2_num_strategies = A.shape
    for support1 in (s for s in powerset(p1_num_strategies) if len(s) > 0):
        for support2 in (
            s
            for s in powerset(p2_num_strategies)
            if (len(s) > 0 and not non_degenerate) or len(s) == len(support1)
        ):
            yield support1, support2


def indifference_strategies(
    A: npt.NDArray, B: npt.NDArray, non_degenerate: bool = False, tol: float = 10**-16
) -> Generator[Tuple[bool, bool, Any, Any], Any, None]:
    """
    A generator for the strategies corresponding to the potential supports

    Parameters
    ----------
    A : array
        The row player utility matrix.
    B : array
        The column player utility matrix
    non_degenerate : bool
        Whether or not to consider supports of equal size. By default
        (False) only considers supports of equal size.
    tol : float
        A tolerance parameter for equality.

    Yields
    ------
    Generator
        A generator of all potential strategies that are indifferent on each
        potential support. Return False if they are not valid (not a
        probability vector OR not fully on the given support).
    """
    if non_degenerate:
        tol = min(tol, 0)

    for pair in potential_support_pairs(A, B, non_degenerate=non_degenerate):
        s1 = solve_indifference(B.T, *(pair[::-1]))
        s2 = solve_indifference(A, *pair)

        if obey_support(s1, pair[0], tol=tol) and obey_support(s2, pair[1], tol=tol):
            yield s1, s2, pair[0], pair[1]


def obey_support(strategy, support: npt.NDArray, tol: float = 10**-16) -> bool:
    """
    Test if a strategy obeys its support

    Parameters
    ----------
    strategy: array
        A given strategy vector
    support: array
        A strategy support
    tol : float
        A tolerance parameter for equality.

    Returns
    -------
    bool
        whether or not that strategy does indeed have the given support
    """
    if strategy is False:
        return False
    if not all(
        (i in support and value > tol) or (i not in support and value <= tol)
        for i, value in enumerate(strategy)
    ):
        return False
    return True


def is_ne(
    strategy_pair: tuple,
    support_pair: Tuple[npt.NDArray, npt.NDArray],
    payoff_matrices: Tuple[npt.NDArray, npt.NDArray],
) -> bool:
    """
    Test if a given strategy pair is a pair of best responses

    Parameters
    ----------
    strategy_pair: tuple
        a 2-tuple of numpy arrays.
    support_pair: tuple
        a 2-tuple of numpy arrays of integers.
    payoff_matrices: tuple
        a 2-tuple of numpy array of payoff matrices.

    Returns
    -------
    bool
        True if a given strategy pair is a pair of best responses.
    """
    A, B = payoff_matrices
    # Payoff against opponents strategies:
    u = strategy_pair[1].reshape(strategy_pair[1].size, 1)
    row_payoffs = np.dot(A, u)

    v = strategy_pair[0].reshape(strategy_pair[0].size, 1)
    column_payoffs = np.dot(B.T, v)

    # Pure payoffs on current support:
    row_support_payoffs = row_payoffs[np.array(support_pair[0])]
    column_support_payoffs = column_payoffs[np.array(support_pair[1])]

    return (
        row_payoffs.max() == row_support_payoffs.max()
        and column_payoffs.max() == column_support_payoffs.max()
    )


def _already_seen(strategy_pair: tuple, seen: list, atol: float = 1e-8) -> bool:
    """
    Test if a strategy pair has already been recorded

    Parameters
    ----------
    strategy_pair : tuple
        A 2-tuple of numpy arrays.
    seen : list
        The pairs recorded so far.
    atol : float
        A tolerance parameter for equality.

    Returns
    -------
    bool
        True if the pair matches one in `seen` up to `atol`.
    """
    s1, s2 = strategy_pair
    for t1, t2 in seen:
        if np.allclose(s1, t1, atol=atol) and np.allclose(s2, t2, atol=atol):
            return True
    return False


def support_ne_vertices(
    A: npt.NDArray,
    B: npt.NDArray,
    support1,
    support2,
    atol: float = 1e-8,
) -> list:
    """
    Vertices of the set of Nash equilibria whose supports are contained in the
    given pair.

    Used when the indifference system for a support pair is singular (degenerate
    games). The vertices are the extreme / limit points of that NE component.

    One probability-vector equality per player is always tight, so
    ``dimension - 2`` further inequalities are needed to pin a vertex down.
    Both the number of inequalities and the resulting number of solves are
    known before any of them are built, so an intractable support pair is
    discarded up front.

    Parameters
    ----------
    A : array
        The row player utility matrix.
    B : array
        The column player utility matrix
    support1 : tuple
        Candidate support of the row player.
    support2 : tuple
        Candidate support of the column player.
    atol : float
        Numerical tolerance.

    Returns
    -------
    list
        Distinct (row strategy, column strategy) vertices.
    """
    rows = list(support1)
    cols = list(support2)
    n1, n2 = A.shape
    m = len(rows)
    n = len(cols)
    dimension = m + n

    n_tight = dimension - 2
    if n_tight < 0:
        return []
    n_inequalities = dimension + m * (n1 - 1) + n * (n2 - 1)
    if n_tight > 0 and comb(n_inequalities, n_tight) > 64:
        return []

    inequalities = []
    for index in range(dimension):
        coeff = np.zeros(dimension)
        coeff[index] = 1.0
        inequalities.append((coeff, 0.0))

    for i in rows:
        for k in range(n1):
            if k == i:
                continue
            coeff = np.zeros(dimension)
            for offset, column in enumerate(cols):
                coeff[m + offset] = A[i, column] - A[k, column]
            inequalities.append((coeff, 0.0))

    for j in cols:
        for ell in range(n2):
            if ell == j:
                continue
            coeff = np.zeros(dimension)
            for offset, row in enumerate(rows):
                coeff[offset] = B[row, j] - B[row, ell]
            inequalities.append((coeff, 0.0))

    eq_row = np.zeros(dimension)
    eq_row[:m] = 1.0
    eq_col = np.zeros(dimension)
    eq_col[m:] = 1.0
    equalities = [(eq_row, 1.0), (eq_col, 1.0)]

    vertices: list = []
    for combo in combinations(range(len(inequalities)), n_tight):
        # The system is square: `dimension` rows made up of the two equalities
        # and `n_tight` tight inequalities. `np.linalg.solve` therefore raises
        # exactly when the matrix is rank deficient, and such a combination
        # does not pin down a single point.
        matrix = np.vstack(
            [eq[0] for eq in equalities] + [inequalities[i][0] for i in combo]
        )
        rhs = np.array(
            [eq[1] for eq in equalities] + [inequalities[i][1] for i in combo]
        )
        try:
            point = np.linalg.solve(matrix, rhs)
        except np.linalg.LinAlgError:
            continue
        if np.any(point < -atol):
            continue
        if any(coeff.dot(point) < bound - atol for coeff, bound in inequalities):
            continue
        # The equalities are rows of the solved system so each block of `point`
        # already sums to 1: the normalisation below only removes drift.
        row_strategy = np.zeros(n1)
        col_strategy = np.zeros(n2)
        row_strategy[rows] = np.maximum(point[:m], 0.0)
        col_strategy[cols] = np.maximum(point[m:], 0.0)
        row_strategy = row_strategy / row_strategy.sum()
        col_strategy = col_strategy / col_strategy.sum()
        pair = (row_strategy, col_strategy)
        if not _already_seen(pair, vertices, atol=atol):
            vertices.append(pair)
    return vertices


def support_enumeration(
    A: npt.NDArray, B: npt.NDArray, non_degenerate: bool = False, tol: float = 10**-16
) -> Generator[Tuple[bool, bool], Any, None]:
    """
    Obtain the Nash equilibria using support enumeration.

    Algorithm implemented here is Algorithm 3.4 of [Nisan2007]_

    1. For each k in 1...min(size of strategy sets)
    2. For each I,J supports of size k
    3. Solve indifference conditions
    4. Check that have Nash Equilibrium.

    On degenerate support pairs the indifference system can be singular. In that
    case the extreme points (limit points) of the NE set on those supports are
    returned.

    Parameters
    ----------
    A : array
        The row player utility matrix.
    B : array
        The column player utility matrix
    non_degenerate : bool
        Whether or not to consider supports of equal size. By default
        (False) only considers supports of equal size.
    tol : float
        A tolerance parameter for equality.

    Yields
    -------
    Generator
        The equilibria.
    """
    count = 0
    seen = []
    recovered_pairs = []
    for pair in potential_support_pairs(A, B, non_degenerate=non_degenerate):
        s1 = solve_indifference(B.T, *(pair[::-1]))
        s2 = solve_indifference(A, *pair)
        if obey_support(s1, pair[0], tol=tol) and obey_support(s2, pair[1], tol=tol):
            if is_ne((s1, s2), (pair[0], pair[1]), (A, B)):
                count += 1
                seen.append((s1, s2))
                yield s1, s2
        elif s1 is False or s2 is False:
            recovered_pairs.append(pair)

    for sup1, sup2 in recovered_pairs:
        for s1, s2 in support_ne_vertices(A, B, sup1, sup2):
            actual1 = tuple(i for i, value in enumerate(s1) if value > tol)
            actual2 = tuple(j for j, value in enumerate(s2) if value > tol)
            if not actual1 or not actual2:
                continue
            if not is_ne((s1, s2), (np.array(actual1), np.array(actual2)), (A, B)):
                continue
            if _already_seen((s1, s2), seen):
                continue
            count += 1
            seen.append((s1, s2))
            yield s1, s2
    if count % 2 == 0:
        warning = """
An even number of ({}) equilibria was returned. This
indicates that the game is degenerate. Consider using another algorithm
to investigate.
                  """.format(count)
        warnings.warn(warning, RuntimeWarning)
