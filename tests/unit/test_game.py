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

    def test_obtain_equilibria_for_bi_matrix(self):
        """Test for the equilibria calculation"""
        A = np.array([[160, 205, 44],
                      [175, 180, 45],
                      [201, 204, 50],
                      [120, 207, 49]])
        B = np.array([[2, 2, 2],
                      [1, 0, 0],
                      [3, 4, 1],
                      [4, 1, 2]])
        g = nash.Game(A, B)
        self.assertTrue(g.obtain_equilibria(),
                        [[(0, 0, 3/4, 1/4), (1/28, 27/28, 0)]])

        A = np.array([[1, 0], [-2, 3]])
        B = np.array([[3, 2], [-1, 0]])
        g = nash.Game(A, B)
        self.assertTrue(g.obtain_equilibria(), [[(0, 1), (0, 1)],
                                                [(1/2, 1/2), (1/2, 1/2)],
                                                [(1, 0), (1, 0)]])
