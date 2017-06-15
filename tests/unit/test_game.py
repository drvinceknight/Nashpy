"""
Tests for the game class
"""

import unittest
import numpy as np

from hypothesis import given
from hypothesis.extra.numpy import arrays
from hypothesis.strategies import integers

import nash

class TestGame(unittest.TestCase):
    """
    Tests for the game class
    """
    @given(A=arrays(np.int8, (4, 5)), B=arrays(np.int8, (4, 5)))
    def test_bi_matrix_init(self, A, B):
        """Test that can create a bi matrix game"""
        g = nash.Game(A, B)
        self.assertEqual(g.payoff_matrices, (A, B))
        if A.any() or B.any():  # Check if A or B are non zero
            self.assertFalse(g.zero_sum)
        else:
            self.assertTrue(g.zero_sum)

        # Can also init with lists
        A = A.tolist()
        B = B.tolist()
        g = nash.Game(A, B)
        self.assertTrue(np.array_equal(g.payoff_matrices[0], np.asarray(A)))
        self.assertTrue(np.array_equal(g.payoff_matrices[1], np.asarray(B)))

    def test_bi_matrix_repr(self):
        """Test that can create a bi matrix game"""
        A = np.array([[1, 2], [2, 1]])
        B = np.array([[2, 1], [1, 2]])
        g = nash.Game(A, B)
        string_repr = """Bi matrix game with payoff matrices:

Row player:
[[1 2]
 [2 1]]

Column player:
[[2 1]
 [1 2]]"""
        self.assertEqual(g.__repr__(), string_repr)

    @given(A=arrays(np.int8, (4, 5)))
    def test_zero_sum_game_init(self, A):
        """Test that can create a zero sum game"""
        g = nash.Game(A)
        self.assertTrue(np.array_equal(g.payoff_matrices[0], A))
        self.assertTrue(np.array_equal(g.payoff_matrices[0],
                                       -g.payoff_matrices[1]))
        self.assertTrue(g.zero_sum)

        # Can also init with lists
        A = A.tolist()
        g = nash.Game(A)
        self.assertTrue(np.array_equal(g.payoff_matrices[0], np.asarray(A)))
        self.assertTrue(np.array_equal(g.payoff_matrices[0],
                                       -g.payoff_matrices[1]))
        self.assertTrue(g.zero_sum)

    def test_zero_sum_repr(self):
        """Test that can create a bi matrix game"""
        A = np.array([[1, -1], [-1, 1]])
        g = nash.Game(A)
        string_repr = """Zero sum game with payoff matrices:

Row player:
[[ 1 -1]
 [-1  1]]

Column player:
[[-1  1]
 [ 1 -1]]"""
        self.assertEqual(g.__repr__(), string_repr)

    @given(A=arrays(np.int8, (4, 5)))
    def test_zero_sum_property_from_bi_matrix(self, A):
        """Test that can create a zero sum game"""
        B = -A
        g = nash.Game(A, B)
        self.assertTrue(g.zero_sum)

    @given(A=arrays(np.int8, (3, 4)), B=arrays(np.int8, (3, 4)))
    def test_property_support_enumeration(self, A, B):
        """Property based test for the equilibria calculation"""
        g = nash.Game(A, B)
        for equilibrium in g.support_enumeration():
            for i, s in enumerate(equilibrium):
                # Test that have a probability vector (subject to numerical
                # error)
                self.assertAlmostEqual(s.sum(), 1)

                # Test that it is of the correct size
                self.assertEqual(s.size, [3, 4][i])

                # Test that it is non negative
                self.assertTrue(all(s >= 0))

    def test_support_enumeration_for_bi_matrix(self):
        """Test for the equilibria calculation support enumeration"""
        A = np.array([[160, 205, 44],
                      [175, 180, 45],
                      [201, 204, 50],
                      [120, 207, 49]])
        B = np.array([[2, 2, 2],
                      [1, 0, 0],
                      [3, 4, 1],
                      [4, 1, 2]])
        g = nash.Game(A, B)
        expected_equilibria = [(np.array([0, 0, 3/4, 1/4]),
                                np.array([1/28, 27/28, 0]))]
        for obtained, expected in zip(g.support_enumeration(),
                                      expected_equilibria):
            for s1, s2 in zip(obtained, expected):
                self.assertTrue(np.array_equal(s1, s2),
                                msg="obtained: {} !=expected: {}".format(obtained,
                                                                         expected))

        A = np.array([[1, 0], [-2, 3]])
        B = np.array([[3, 2], [-1, 0]])
        g = nash.Game(A, B)
        expected_equilibria = [(np.array([1, 0]), np.array([1, 0])),
                               (np.array([0, 1]), np.array([0, 1])),
                               (np.array([1/2, 1/2]), np.array([1/2, 1/2]))]
        for obtained, expected in zip(g.support_enumeration(),
                                      expected_equilibria):
            for s1, s2 in zip(obtained, expected):
                self.assertTrue(np.array_equal(s1, s2),
                                msg="obtained: {} !=expected: {}".format(obtained,
                                                                         expected))

        A = np.array([[2, 1], [0, 2]])
        B = np.array([[2, 0], [1, 2]])
        g = nash.Game(A, B)
        expected_equilibria = [(np.array([1, 0]), np.array([1, 0])),
                               (np.array([0, 1]), np.array([0, 1])),
                               (np.array([1/3, 2/3]), np.array([1/3, 2/3]))]
        for obtained, expected in zip(g.support_enumeration(),
                                      expected_equilibria):
            for s1, s2 in zip(obtained, expected):
                self.assertTrue(np.array_equal(s1, s2),
                                msg="obtained: {} !=expected: {}".format(obtained,
                                                                         expected))

    def test_vertex_enumeration_for_bi_matrix(self):
        """Test for the equilibria calculation using vertex enumeration"""
        A = np.array([[160, 205, 44],
                      [175, 180, 45],
                      [201, 204, 50],
                      [120, 207, 49]])
        B = np.array([[2, 2, 2],
                      [1, 0, 0],
                      [3, 4, 1],
                      [4, 1, 2]])
        g = nash.Game(A, B)
        expected_equilibria = [(np.array([0, 0, 3/4, 1/4]),
                                np.array([1/28, 27/28, 0]))]
        for obtained, expected in zip(g.vertex_enumeration(),
                                      expected_equilibria):
            for s1, s2 in zip(obtained, expected):
                self.assertTrue(all(np.isclose(s1, s2)),
                                msg="obtained: {} !=expected: {}".format(obtained,
                                                                         expected))

        A = np.array([[1, 0], [-2, 3]])
        B = np.array([[3, 2], [-1, 0]])
        g = nash.Game(A, B)
        expected_equilibria = [(np.array([1, 0]), np.array([1, 0])),
                               (np.array([0, 1]), np.array([0, 1])),
                               (np.array([1/2, 1/2]), np.array([1/2, 1/2]))]
        for obtained, expected in zip(g.vertex_enumeration(),
                                      expected_equilibria):
            for s1, s2 in zip(obtained, expected):
                self.assertTrue(all(np.isclose(s1, s2)),
                                msg="obtained: {} !=expected: {}".format(obtained,
                                                                         expected))

        A = np.array([[2, 1], [0, 2]])
        B = np.array([[2, 0], [1, 2]])
        g = nash.Game(A, B)
        expected_equilibria = [(np.array([1, 0]), np.array([1, 0])),
                               (np.array([0, 1]), np.array([0, 1])),
                               (np.array([1/3, 2/3]), np.array([1/3, 2/3]))]
        for obtained, expected in zip(g.vertex_enumeration(),
                                      expected_equilibria):
            for s1, s2 in zip(obtained, expected):
                self.assertTrue(all(np.isclose(s1, s2)),
                                msg="obtained: {} !=expected: {}".format(obtained,
                                                                         expected))

    def test_get_item(self):
        """Test solve indifference"""
        A = np.array([[1, -1], [-1, 1]])
        g = nash.Game(A)

        row_strategy = [0, 1]
        column_strategy = [1, 0]
        self.assertTrue(np.array_equal(g[row_strategy, column_strategy],
                                       np.array((-1, 1))))

        row_strategy = [1/2, 1/2]
        column_strategy = [1/2, 1/2]
        self.assertTrue(np.array_equal(g[row_strategy, column_strategy],
                                       np.array((0, 0))))
