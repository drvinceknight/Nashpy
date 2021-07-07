"""
Tests for the best response check
"""
import numpy as np

from nashpy.utils.is_best_response import (
    is_best_response,
)


def test_is_best_response_example_1():
    """
    This tests an example from the discussion documentation.

    The second assert checks that the column player strategy is as expected.
    """
    A = np.array(((0, -1, 1), (1, 0, -1), (-1, 1, 0)))
    sigma_c = np.array((0, 1 / 2, 1 / 2))
    sigma_r = np.array((0, 0, 1))
    assert is_best_response(A=A, sigma_c=sigma_c, sigma_r=sigma_r) is True
    assert is_best_response(A=-A.T, sigma_c=sigma_r, sigma_r=sigma_c) is False


def test_is_best_response_example_2():
    """
    This tests an example from the discussion documentation.

    The second assert checks that the column player strategy is as expected.
    """
    A = np.array(((0, -1, 1), (1, 0, -1), (-1, 1, 0)))
    sigma_c = np.array((0, 1 / 2, 1 / 2))
    sigma_r = np.array((1 / 3, 1 / 3, 1 / 3))
    assert is_best_response(A=A, sigma_c=sigma_c, sigma_r=sigma_r) is False
    assert is_best_response(A=-A.T, sigma_c=sigma_r, sigma_r=sigma_c) is True


def test_is_best_response_example_3():
    """
    This tests an example from the discussion documentation.

    The second assert checks that the column player strategy is as expected.
    """
    A = np.array(((0, -1, 1), (1, 0, -1), (-1, 1, 0)))
    sigma_c = np.array((1 / 3, 1 / 3, 1 / 3))
    sigma_r = np.array((1 / 3, 1 / 3, 1 / 3))
    assert is_best_response(A=A, sigma_c=sigma_c, sigma_r=sigma_r) is True
    assert is_best_response(A=-A.T, sigma_c=sigma_r, sigma_r=sigma_c) is True
