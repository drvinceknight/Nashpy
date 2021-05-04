"""
Tests for the integer pivoting
"""
import unittest

import numpy as np
from hypothesis import given
from hypothesis.extra.numpy import arrays

from nashpy.integer_pivoting.integer_pivoting import (
    find_pivot_row,
    make_tableau,
    non_basic_variables,
    pivot_tableau,
)


class TestPolytope(unittest.TestCase):
    """
    Tests for the functions for integer pivoting
    """

    @given(M=arrays(np.int8, (4, 5)))
    def test_creation_of_tableaux(self, M):
        tableau = make_tableau(M)
        number_of_strategies, dimension = M.shape
        self.assertEqual(
            tableau.shape,
            (number_of_strategies, number_of_strategies + dimension + 1),
        )
        self.assertTrue(
            np.array_equal(tableau[:, dimension:-1], np.eye(number_of_strategies))
        )
        self.assertTrue(np.array_equal(tableau[:, -1], np.ones(number_of_strategies)))

    def test_creationg_of_particular_tableaux(self):
        M = np.array([[3, 3], [2, 5], [0, 6]])
        expected_tableau = np.array(
            [
                [3.0, 3.0, 1.0, 0.0, 0.0, 1.0],
                [2.0, 5.0, 0.0, 1.0, 0.0, 1.0],
                [0.0, 6.0, 0.0, 0.0, 1.0, 1.0],
            ]
        )
        tableau = make_tableau(M)
        self.assertTrue(np.array_equal(tableau, expected_tableau))

        M = np.array([[3, 2, 3], [2, 6, 1]])
        expected_tableau = np.array(
            [[3.0, 2.0, 3.0, 1.0, 0.0, 1.0], [2.0, 6.0, 1.0, 0.0, 1.0, 1.0]]
        )
        tableau = make_tableau(M)
        self.assertTrue(np.array_equal(tableau, expected_tableau))

    def test_find_particular_pivot_row(self):
        tableau = np.array(
            [
                [3.0, 3.0, 1.0, 0.0, 0.0, 1.0],
                [2.0, 5.0, 0.0, 1.0, 0.0, 1.0],
                [0.0, 6.0, 0.0, 0.0, 1.0, 1.0],
            ]
        )
        for column, row in [(0, 0), (1, 2), (2, 0), (3, 1), (4, 2)]:
            self.assertEqual(find_pivot_row(tableau=tableau, column_index=column), row)

        tableau = np.array(
            [[3.0, 2.0, 3.0, 1.0, 0.0, 1.0], [2.0, 6.0, 1.0, 0.0, 1.0, 1.0]]
        )
        for column, row in [(0, 0), (1, 1), (2, 0), (3, 0), (4, 1)]:
            self.assertEqual(find_pivot_row(tableau=tableau, column_index=column), row)

    def test_non_basic_variables(self):
        tableau = np.array(
            [
                [3.0, 3.0, 1.0, 0.0, 0.0, 1.0],
                [2.0, 5.0, 0.0, 1.0, 0.0, 1.0],
                [0.0, 6.0, 0.0, 0.0, 1.0, 1.0],
            ]
        )
        self.assertEqual(non_basic_variables(tableau), set([0, 1]))

        tableau = np.array(
            [[3.0, 2.0, 3.0, 1.0, 0.0, 1.0], [2.0, 6.0, 1.0, 0.0, 1.0, 1.0]]
        )
        self.assertEqual(non_basic_variables(tableau), set([0, 1, 2]))

    def test_particular_pivot(self):
        tableau = np.array(
            [
                [3.0, 3.0, 1.0, 0.0, 0.0, 1.0],
                [2.0, 5.0, 0.0, 1.0, 0.0, 1.0],
                [0.0, 6.0, 0.0, 0.0, 1.0, 1.0],
            ]
        )
        self.assertEqual(pivot_tableau(tableau, column_index=0), set([2]))
        next_tableau = np.array(
            [
                [3.0, 3.0, 1.0, 0.0, 0.0, 1.0],
                [0.0, 9.0, -2.0, 3.0, 0.0, 1.0],
                [0.0, 18.0, 0.0, 0.0, 3.0, 3.0],
            ]
        )
        self.assertTrue(
            np.array_equal(tableau, next_tableau),
            msg="{} != {}".format(tableau, next_tableau),
        )
        self.assertEqual(pivot_tableau(tableau, column_index=2), set([0]))
        next_tableau = np.array(
            np.array(
                [
                    [3.0, 3.0, 1.0, 0.0, 0.0, 1.0],
                    [6.0, 15.0, 0.0, 3.0, 0.0, 3.0],
                    [0.0, 18.0, 0.0, 0.0, 3.0, 3.0],
                ]
            )
        )
        self.assertTrue(
            np.array_equal(tableau, next_tableau),
            msg="{} != {}".format(tableau, next_tableau),
        )
