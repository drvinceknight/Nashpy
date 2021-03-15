"""Code to carry out stochastic fictitious learning"""
import numpy as np
from nashpy.learning.fictitious_play import update_play_count


def get_distribution_response_to_play_count(A, play_count):
    strategies = play_count / np.sum(play_count)
    return strategies
