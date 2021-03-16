"""Code to carry out stochastic fictitious learning"""
import numpy as np
from nashpy.learning.fictitious_play import update_play_count


def get_distribution_response_to_play_count(A, play_count, epsilon_bar, etha):
    strategies = play_count / np.sum(play_count)
    utilities = A @ strategies
    noisy_utilities = utilities + np.random.random(A.shape[0]) * epsilon_bar
    logit_choice = np.exp(etha ** -1 * noisy_utilities) / np.sum(
        np.exp(etha ** -1 * noisy_utilities)
    )
    return logit_choice


def stochastic_fictitious_play(A, play_counts=None):
    """
    Implement fictitious play
    """
    if play_counts is None:
        play_counts = [np.array([1 for _ in range(dimension)]) for dimension in A.shape]

    distributions = None, None

    yield play_counts, distributions

    # FROM SIG A, B, iterations, etha, epsilon_bar,

    # for repetition in range(iterations):


#
#    distributions = [
#        get_distribution_response_to_play_count(
#            matrix, play_count, etha, epsilon_bar
#        )
#        for matrix, play_count in zip((A, B.transpose()), play_counts[::-1])
#    ]
#    # pick move here
#    plays = [
#        np.random.choice(range(len(distributions)), p=distributions)
#        for distribution in distributions
#    ]
#
#    play_counts = [
#        update_play_count(play_count, play)
#        for play_count, play in zip(play_counts, plays)
#    ]
#    yield play_counts, distributions
