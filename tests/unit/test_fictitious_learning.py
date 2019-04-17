"""
Tests for fictitious learning
"""
import unittest

import numpy as np
from hypothesis import given
from hypothesis.extra.numpy import arrays
from hypothesis.strategies import integers

import nashpy as nash
from nashpy.learning.fictitious_learning import (
    get_best_response_to_belief,
)



class TestFicticiousLearning(unittest.TestCase):
    """
    Tests for the functions for fictitious learning
    """

    @given(M=arrays(np.int8, (4, 5)))
    def test_find_best_response_to_belief(self, M):
        belief = np.zeros(M.shape[1])
        best_response = get_best_response_to_belief(M, belief)
        self.assertGreaterEqual(best_response, 0)
        self.assertLessEqual(best_response, M.shape[1] - 1)
        self.assertIsInstance(best_response, np.int64)
