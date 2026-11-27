"""Cumulative external regret matching for two-player normal-form games."""

import warnings
from typing import Generator, Optional

import numpy as np
import numpy.typing as npt


def compute_regrets(
    strategy_utilities: npt.NDArray, current_strategy: npt.NDArray
) -> npt.NDArray:
    """Calculate signed instantaneous regret for each pure action.

    Parameters
    ----------
    strategy_utilities : array
        Expected utilities of each pure action against the opponent's strategy.
    current_strategy : array
        The player's current mixed strategy.

    Returns
    -------
    array
        Each action's utility minus the current strategy's expected utility.
        Negative values are retained when accumulating regrets.
    """
    return strategy_utilities - (current_strategy @ strategy_utilities)


def update_strategy(cumulative_regrets: npt.NDArray) -> npt.NDArray:
    """Match a mixed strategy to positive cumulative regrets.

    Parameters
    ----------
    cumulative_regrets : array
        Signed cumulative regrets, one per pure action.

    Returns
    -------
    array
        Normalized positive regrets, or the uniform strategy if none are
        positive. The input regrets are not modified.
    """
    positive_regrets = np.maximum(cumulative_regrets, 0)
    total = positive_regrets.sum()
    if total > 0:
        return positive_regrets / total
    return np.full(len(cumulative_regrets), 1 / len(cumulative_regrets))


def regret_minimization(
    A: npt.NDArray,
    B: npt.NDArray,
    learning_rate: Optional[float] = None,
    iterations: int = 100,
) -> Generator[tuple[npt.NDArray, npt.NDArray], None, None]:
    """Yield average mixed strategies obtained through cumulative regret matching.

    Both players start uniformly and update simultaneously using expected
    utilities. Signed regrets accumulate across rounds. Their positive parts
    determine the next strategies. The algorithm is deterministic.

    The generator yields one pair after all rounds. The average includes the
    strategies used in those rounds, starting with the uniform profile, and
    excludes the unplayed update after the last round. In zero-sum games these
    averages approach the set of Nash equilibria as iterations increase.

    Parameters
    ----------
    A : array
        Finite, real row-player payoffs with shape (m, n).
    B : array
        Finite, real column-player payoffs with the same shape as A.
    learning_rate : float, optional
        Deprecated and ignored. The argument retains its positional slot for
        compatibility. Values other than None emit DeprecationWarning.
    iterations : int
        Number of rounds to average, default 100. Zero returns the initial
        uniform strategies.

    Yields
    ------
    tuple
        Two NumPy arrays of average action probabilities, of lengths m and n.

    Raises
    ------
    ValueError
        If matrices are not non-empty, finite, real, two-dimensional arrays
        of the same shape, or iterations is not a non-negative integer.
    """
    if np.iscomplexobj(A) or np.iscomplexobj(B):
        raise ValueError("A and B must contain real payoffs.")
    A = np.asarray(A, dtype=float)
    B = np.asarray(B, dtype=float)
    if A.ndim != 2 or B.ndim != 2:
        raise ValueError("A and B must be two-dimensional payoff matrices.")
    if A.shape != B.shape:
        raise ValueError("A and B must have the same shape.")
    if A.size == 0:
        raise ValueError("A and B must be non-empty payoff matrices.")
    if not np.isfinite(A).all() or not np.isfinite(B).all():
        raise ValueError("A and B must contain only finite payoffs.")
    if (
        isinstance(iterations, (bool, np.bool_))
        or not isinstance(iterations, (int, np.integer))
        or iterations < 0
    ):
        raise ValueError("iterations must be a non-negative integer.")
    if learning_rate is not None:
        warnings.warn(
            "learning_rate is deprecated and ignored by cumulative regret "
            "matching. Use iterations=... to set the number of rounds.",
            DeprecationWarning,
            stacklevel=2,
        )

    # Scaling each player's payoffs by a positive factor preserves regret
    # matching. Powers of two keep regret sums bounded even at extreme scales.
    A = np.ldexp(A, -np.frexp(np.abs(A).max())[1])
    B = np.ldexp(B, -np.frexp(np.abs(B).max())[1])

    number_of_row_strategies, number_of_column_strategies = A.shape
    row_regrets = np.zeros(number_of_row_strategies)
    column_regrets = np.zeros(number_of_column_strategies)
    row_strategy_sum = np.zeros(number_of_row_strategies)
    column_strategy_sum = np.zeros(number_of_column_strategies)

    for _ in range(iterations):
        row_strategy = update_strategy(row_regrets)
        column_strategy = update_strategy(column_regrets)
        row_strategy_sum += row_strategy
        column_strategy_sum += column_strategy

        row_utilities = A @ column_strategy
        column_utilities = B.T @ row_strategy
        row_regrets += compute_regrets(row_utilities, row_strategy)
        column_regrets += compute_regrets(column_utilities, column_strategy)

    if iterations == 0:
        yield update_strategy(row_regrets), update_strategy(column_regrets)
    else:
        yield row_strategy_sum / iterations, column_strategy_sum / iterations
