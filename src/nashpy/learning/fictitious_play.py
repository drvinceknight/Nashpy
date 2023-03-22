"""Code to carry out fictitious learning"""
import numpy as np
import numpy.typing as npt
from typing import Generator, Optional, Any


def get_best_response_to_play_count(A: npt.NDArray, play_count: npt.NDArray) -> int:
    """
    Returns the best response to a belief based on the playing distribution of the opponent

    Parameters
    ----------
    A : array
        The utility matrix.
    play_count : array
        The play counts.

    Returns
    -------
    int
        The action that corresponds to the best response.
    """
    utilities = A @ play_count
    return np.random.choice(np.argwhere(utilities == np.max(utilities)).transpose()[0])


def update_play_count(play_count: npt.NDArray, play: int) -> npt.NDArray:
    """
    Update a belief vector with a given play

    Parameters
    ----------
    play_count : array
        The play counts.
    play : int
        The given play.

    Returns
    -------
    array
        The updated play counts.
    """
    extra_play = np.zeros(play_count.shape)
    extra_play[play] = 1
    return play_count + extra_play


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
    if play_counts is None:
        play_counts = [np.array([0 for _ in range(dimension)]) for dimension in A.shape]

    yield play_counts

    for repetition in range(iterations):
        plays = [
            get_best_response_to_play_count(matrix, play_count)
            for matrix, play_count in zip((A, B.transpose()), play_counts[::-1])
        ]

        play_counts = [
            update_play_count(play_count, play)
            for play_count, play in zip(play_counts, plays)
        ]
        yield play_counts
