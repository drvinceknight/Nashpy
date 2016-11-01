"""
Tests for the game class
"""

import unittest
import nash

class TestGame(unittest.TestCase):
    """
    Tests for the game class
    """
    def test_init(self):
        A = [[1, 2], [2, 1]]
        B = [[2, 1], [1, 2]]
        g = nash.Game(A, B)
        self.assertEqual(g.payoffs, (A, B))
