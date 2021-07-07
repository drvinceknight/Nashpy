"""Functions for testing of best responses"""
import numpy as np


def is_best_response(A, sigma_c, sigma_r):
    """
    Checks if sigma_r is a best response to sigma_c when A is the payoff matrix
    for the player playing sigma_r.

    Parameters
    ----------
    A : array
        The row player payoff matrix
    sigma_c : array
        The column player strategy
    sigma_r : array
        The row player strategy

    Returns
    -------
    bool
        If True it indicates that sigma_r is a best response to sigma_c
    """
    row_utilities = A @ sigma_c
    max_utility = np.max(row_utilities)
    return all(row_utilities[sigma_r > 0] == max_utility)
