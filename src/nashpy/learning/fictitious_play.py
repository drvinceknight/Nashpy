"""Code to carry out fictitious learning"""

import numpy as np
import numpy.typing as npt
from typing import Generator, Optional, Any, Union


def get_best_response_to_play_count(
    A: npt.NDArray,
    play_count: npt.NDArray,
    *,
    rng: Optional[np.random.Generator] = None,
) -> int:
    """
    Returns the best response to a belief based on the playing distribution of the opponent

    Parameters
    ----------
    A : array
        The utility matrix.
    play_count : array
        The play counts.
    rng : numpy.random.Generator, optional
        The random number generator used to break ties.

    Returns
    -------
    int
        The action that corresponds to the best response.
    """
    rng = np.random.default_rng(rng)
    utilities = A @ play_count
    return rng.choice(np.argwhere(utilities == np.max(utilities)).transpose()[0])


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
    A: npt.NDArray,
    B: npt.NDArray,
    iterations: int,
    play_counts: Optional[Any] = None,
    *,
    seed: Optional[Union[int, np.random.Generator]] = None,
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
    seed : int or numpy.random.Generator, optional
        A seed or generator for the local random number generator.

    Yields
    -------
    Generator
        The play counts.
    """
    rng = np.random.default_rng(seed)
    if play_counts is None:
        play_counts = [np.array([0 for _ in range(dimension)]) for dimension in A.shape]

    yield play_counts

    for repetition in range(iterations):
        plays = [
            get_best_response_to_play_count(matrix, play_count, rng=rng)
            for matrix, play_count in zip((A, B.transpose()), play_counts[::-1])
        ]

        play_counts = [
            update_play_count(play_count, play)
            for play_count, play in zip(play_counts, plays)
        ]
        yield play_counts
