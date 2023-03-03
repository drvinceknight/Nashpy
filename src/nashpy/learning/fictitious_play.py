"""Code to carry out fictitious learning"""
import numpy as np
import numpy.typing as npt
from typing import Generator, Optional, Any


def fictitious_play(
    A: npt.NDArray, B: npt.NDArray, iterations: int, play_counts: Optional[Any] = None
) -> Generator:
    """
    Implement fictitious play

    Parameters
    ----------
    A : array
        The row player payoff matrix.
    B : array
        The column player payoff matrix.
    iterations : int
        The number of iterations of the algorithm.
    play_counts : Optional
        The play counts.

    Yields
    -------
    Generator
        The play counts.
    """
    actions1, actions2 = A.shape

    if play_counts is None:
        play_counts1 = np.zeros(actions1, dtype=int)
        play_counts2 = np.zeros(actions2, dtype=int)
        payoff1 = np.zeros(actions1)
        payoff2 = np.zeros(actions2)
    else:
        play_counts1, play_counts2 = play_counts
        payoff1 = A @ play_counts2
        payoff2 = play_counts1 @ B

    A_t = A.T
    yield play_counts1, play_counts2

    for _ in range(iterations):

        best_move1 = np.random.choice(np.flatnonzero(payoff1 == payoff1.max()))
        best_move2 = np.random.choice(np.flatnonzero(payoff2 == payoff2.max()))

        payoff1 += A_t[best_move2]
        payoff2 += B[best_move1]

        play_counts1[best_move1] += 1
        play_counts2[best_move2] += 1

        yield play_counts1, play_counts2
