"""
Tests for the game class
"""

import unittest
import nash
import numpy as np

class TestGame(unittest.TestCase):
    """
    Tests for the game class
    """
    def test_bi_matrix_init(self):
        """Test that can create a bi matrix game"""
        A = np.array([[1, 2], [2, 1]])
        B = np.array([[2, 1], [1, 2]])
        g = nash.Game(A, B)
        self.assertEqual(g.payoff_matrices, (A, B))
        self.assertFalse(g.zero_sum)

    def test_zero_sum_game_init(self):
        """Test that can create a zero sum game"""
        A = np.array([[1, 2], [2, 1]])
        g = nash.Game(A)
        self.assertTrue(np.array_equal(g.payoff_matrices[0], A))
        self.assertTrue(np.array_equal(g.payoff_matrices[0],
                                       -g.payoff_matrices[1]))
        self.assertTrue(g.zero_sum)

    def test_zero_sum_property_from_bi_matrix(self):
        """Test that can create a zero sum game"""
        A = np.array([[1, 2], [2, 1]])
        B = -A
        g = nash.Game(A, B)
        self.assertTrue(g.zero_sum)
