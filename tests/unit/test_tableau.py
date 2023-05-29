"""
Tests for the integer pivoting
"""
import unittest

import numpy as np
from hypothesis import given
from hypothesis.extra.numpy import arrays

from nashpy.linalg import Tableau, create_row_tableau, create_col_tableau


class TestPolytope(unittest.TestCase):
    """
    Tests for the functions for integer pivoting
    """

    @given(M=arrays(np.int8, (4, 5)))
    def test_creation_of_tableaux(self, M):
        t = create_row_tableau(M.transpose(), False)
        tableau = t._tableau
        number_of_strategies, dimension = M.shape
        self.assertEqual(
            tableau.shape,
            (number_of_strategies, number_of_strategies + dimension + 1),
        )
        self.assertTrue(
            np.array_equal(tableau[:, dimension:-1], np.eye(number_of_strategies))
        )
        self.assertTrue(np.array_equal(tableau[:, -1], np.ones(number_of_strategies)))

    def test_creation_of_particular_row_tableau(self):
        M = np.array([[3, 2, -1], [3, 5, 6]])
        expected_tableau = np.array(
            [
                [5.0, 5.0, 1.0, 0.0, 0.0, 1.0],
                [4.0, 7.0, 0.0, 1.0, 0.0, 1.0],
                [1.0, 8.0, 0.0, 0.0, 1.0, 1.0],
            ]
        )
        t = create_row_tableau(M, False)
        self.assertTrue(np.array_equal(t._tableau, expected_tableau))
        self.assertEqual(t.non_basic_variables, set([0, 1]))
        self.assertEqual(t._original_basic_labels, set([0, 1]))
        self.assertEqual(t.labels, set(range(sum(M.shape))))
        self.assertEqual(t.basic_variables, set([2, 3, 4]))
        self.assertEqual(t.slack_variables, set([2, 3, 4]))

    def test_creation_of_particular_col_tableau(self):
        M = np.array([[3, 2, 3], [2, 6, 1]])
        expected_tableau = np.array(
            [[1.0, 0.0, 3.0, 2.0, 3.0, 1.0], [0.0, 1.0, 2.0, 6.0, 1.0, 1.0]]
        )
        t = create_col_tableau(M, False)
        self.assertTrue(np.array_equal(t._tableau, expected_tableau))
        self.assertEqual(t.non_basic_variables, set([2, 3, 4]))
        self.assertEqual(t._original_basic_labels, set([2, 3, 4]))
        self.assertEqual(t.labels, set(range(sum(M.shape))))
        self.assertEqual(t.basic_variables, set([0, 1]))
        self.assertEqual(t.slack_variables, set([0, 1]))

    def test_find_particular_pivot_row(self):
        tableau = np.array(
            [
                [3.0, 3.0, 1.0, 0.0, 0.0, 1.0],
                [2.0, 5.0, 0.0, 1.0, 0.0, 1.0],
                [0.0, 6.0, 0.0, 0.0, 1.0, 1.0],
            ]
        )
        t = Tableau(tableau)
        for column, row in [(0, 0), (1, 2), (2, 0), (3, 1), (4, 2)]:
            self.assertEqual(t._find_pivot_row(column_index=column), row)

        tableau = np.array(
            [[3.0, 2.0, 3.0, 1.0, 0.0, 1.0], [2.0, 6.0, 1.0, 0.0, 1.0, 1.0]]
        )
        t = Tableau(tableau)
        for column, row in [(0, 0), (1, 1), (2, 0), (3, 0), (4, 1)]:
            self.assertEqual(t._find_pivot_row(column_index=column), row)

    def test_non_basic_variables(self):
        tableau = np.array(
            [
                [3.0, 3.0, 1.0, 0.0, 0.0, 1.0],
                [2.0, 5.0, 0.0, 1.0, 0.0, 1.0],
                [0.0, 6.0, 0.0, 0.0, 1.0, 1.0],
            ]
        )
        t = Tableau(tableau)
        self.assertEqual(t.non_basic_variables, set([0, 1]))

        tableau = np.array(
            [[3.0, 2.0, 3.0, 1.0, 0.0, 1.0], [2.0, 6.0, 1.0, 0.0, 1.0, 1.0]]
        )
        t = Tableau(tableau)
        self.assertEqual(t.non_basic_variables, set([0, 1, 2]))

    def test_particular_pivot(self):
        tableau = np.array(
            [
                [3.0, 3.0, 1.0, 0.0, 0.0, 1.0],
                [2.0, 5.0, 0.0, 1.0, 0.0, 1.0],
                [0.0, 6.0, 0.0, 0.0, 1.0, 1.0],
            ]
        )
        t = Tableau(tableau)
        self.assertEqual(t.pivot_and_drop_label(column_index=0), 2)
        next_tableau = np.array(
            [
                [3.0, 3.0, 1.0, 0.0, 0.0, 1.0],
                [0.0, 9.0, -2.0, 3.0, 0.0, 1.0],
                [0.0, 18.0, 0.0, 0.0, 3.0, 3.0],
            ]
        )
        self.assertTrue(
            np.array_equal(t._tableau, next_tableau),
            msg="{} != {}".format(tableau, next_tableau),
        )
        self.assertEqual(t.pivot_and_drop_label(column_index=2), 0)
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
            np.array_equal(t._tableau, next_tableau),
            msg="{} != {}".format(tableau, next_tableau),
        )

    def test_fail_fast_on_no_dropped_label(self):
        tableau = Tableau(np.array([[3.0]]))
        with self.assertRaises(ValueError):
            tableau._find_dropped(0, set())
