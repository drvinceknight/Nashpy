"""Code to carry out fictitious learning"""
import numpy as np


def get_best_response_to_play_count(A, play_count):
    """
    Returns the best response to a belief based on the playing distribution of the opponent
    """
    utilities = A @ play_count
    return np.random.choice(
        np.argwhere(utilities == np.max(utilities)).transpose()[0]
    )


def update_play_count(play_count, play):
    """
    Update a belief vector with a given play
    """
    extra_play = np.zeros(play_count.shape)
    extra_play[play] = 1
    return play_count + extra_play


def fictitious_play(A, B, iterations, play_counts=None):
    """
    Implement fictitious play
    """
    if play_counts is None:
        play_counts = [
            np.array([0 for _ in range(dimension)]) for dimension in A.shape
        ]

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
