"""Code to carry out stochastic fictitious learning"""
import numpy as np
from nashpy.learning.fictitious_play import update_play_count


def get_distribution_response_to_play_count(A, play_count, epsilon_bar, etha):
    strategies = play_count / np.sum(play_count)
    utilities = A @ strategies
    noisy_utilities = utilities + np.random.random(len(utilities)) * epsilon_bar
    logit_choice = np.exp(etha ** -1 * noisy_utilities) / np.sum(
        np.exp(etha ** -1 * noisy_utilities)
    )
    return logit_choice
