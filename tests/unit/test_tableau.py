"""
Tests for the integer pivoting
"""
import unittest

import numpy as np
from hypothesis import given
from hypothesis.extra.numpy import arrays

from nashpy.linalg import TableauBuilder, Tableau


class TestPolytope(unittest.TestCase):
    """
    Tests for the functions for integer pivoting
    """

    @given(M=arrays(np.int8, (4, 5)))
    def test_creation_of_tableaux(self, M):
        t = TableauBuilder.row(M.transpose()).build()
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

    def test_creationg_of_particular_tableaux(self):
        M = np.array([[3, 3], [2, 5], [0, 6]])
        expected_tableau = np.array(
            [
                [3.0, 3.0, 1.0, 0.0, 0.0, 1.0],
                [2.0, 5.0, 0.0, 1.0, 0.0, 1.0],
                [0.0, 6.0, 0.0, 0.0, 1.0, 1.0],
            ]
        )
        t = TableauBuilder.row(M.transpose()).build()
        self.assertTrue(np.array_equal(t._tableau, expected_tableau))

        M = np.array([[3, 2, 3], [2, 6, 1]])
        expected_tableau = np.array(
            [[3.0, 2.0, 3.0, 1.0, 0.0, 1.0], [2.0, 6.0, 1.0, 0.0, 1.0, 1.0]]
        )
        t = TableauBuilder.row(M.transpose()).build()
        self.assertTrue(np.array_equal(t._tableau, expected_tableau))

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

    def test_unknown_algorithm(self):
        payoffs = np.eye(3)
        with self.assertRaises(ValueError) as context:
            TableauBuilder.row(payoffs).build("unknownalgorithm")
            self.assertEquals(
                "Algorithm 'unknownalgorithm' is not known, use 'basic' or 'lex'",
                context.exception,
            )

    def test_fail_fast_on_no_dropped_label(self):
        tableau = Tableau(np.array([[3.0]]))
        with self.assertRaises(ValueError):
            tableau._find_dropped(0, set())
