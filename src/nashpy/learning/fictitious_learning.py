"""Code to carry out fictitious learning"""
import numpy as np

def get_best_response_to_belief(A, belief):
    """
    Returns the best response to a belief of the playing distribution of the opponent
    """
    utilities = A @ belief
    return np.random.choice(
        np.argwhere(
            utilities == np.max(utilities)
        ).transpose()[0]
    )
