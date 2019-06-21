"""Code to carry out fictitious learning"""
import numpy as np


def get_best_response_to_belief(A, belief):
    """
    Returns the best response to a belief of the playing distribution of the opponent
    """
    utilities = A @ belief
    return np.random.choice(
        np.argwhere(utilities == np.max(utilities)).transpose()[0]
    )


def update_belief(belief, play):
    """
    Update a belief vector with a given play
    """
    extra_play = np.zeros(belief.shape)
    extra_play[play] = 1
    return belief + extra_play


def fictitious_play(A, B, iterations, beliefs=None):
    """
    Implement fictitious play
    """
    if beliefs is None:
        beliefs = [
            np.array([0 for _ in range(dimension)]) for dimension in A.shape
        ]

    yield beliefs

    for repetition in range(iterations):

        plays = [
            get_best_response_to_belief(matrix, belief)
            for matrix, belief in zip((A, B.transpose()), beliefs[::-1])
        ]

        beliefs = [
            update_belief(belief, play) for belief, play in zip(beliefs, plays)
        ]
        yield beliefs
