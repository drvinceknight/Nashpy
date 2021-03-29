"""
Tests for the integer pivoting
"""
import unittest

import numpy as np

from nashpy.integer_pivoting.integer_pivoting_lex import (
    find_entering_variable,
    find_pivot_row_lex,
    pivot_tableau_lex,
)


class TestPolytope(unittest.TestCase):
    """
    Tests for the functions for integer pivoting
    """

    def test_find_particular_pivot_row_lex(self):
        tableau = np.array(
            [
                [3.0, 3.0, 1.0, 0.0, 0.0, 1.0],
                [2.0, 5.0, 0.0, 1.0, 0.0, 1.0],
                [0.0, 6.0, 0.0, 0.0, 1.0, 1.0],
            ]
        )
        slack_variables = [2, 3, 4]
        for column, row in [(0, 0), (1, 2), (2, 0), (3, 1), (4, 2)]:
            self.assertEqual(
                find_pivot_row_lex(
                    tableau=tableau,
                    column_index=column,
                    slack_variables=slack_variables,
                ),
                row,
            )

        tableau = np.array(
            [[3.0, 2.0, 3.0, 1.0, 0.0, 1.0], [2.0, 6.0, 1.0, 0.0, 1.0, 1.0]]
        )
        slack_variables = [3, 4]
        for column, row in [(0, 0), (1, 1), (2, 0), (3, 0), (4, 1)]:
            self.assertEqual(
                find_pivot_row_lex(
                    tableau=tableau,
                    column_index=column,
                    slack_variables=slack_variables,
                ),
                row,
            )

        # degenerate case
        tableau = np.array(
            [
                [3.0, 1.0, 3.0, 1.0, 0.0, 0.0, 1.0],
                [0.0, 0.0, -6.0, -3.0, 3.0, 0.0, 0.0],
                [0.0, 8.0, 6.0, -1.0, 0.0, 3.0, 2.0],
            ]
        )
        slack_variables = [3, 4, 5]
        for column, row in [(0, 0), (1, 2), (2, 0), (3, 0), (4, 1)]:
            self.assertEqual(
                find_pivot_row_lex(
                    tableau=tableau,
                    column_index=column,
                    slack_variables=slack_variables,
                ),
                row,
            )

    def test_find_entering_variable(self):
        tableau = np.array(
            [
                [3.0, 1.0, 3.0, 1.0, 0.0, 0.0, 1.0],
                [3.0, 1.0, 1.0, 0.0, 1.0, 0.0, 1.0],
                [1.0, 3.0, 3.0, 0.0, 0.0, 1.0, 1.0],
            ]
        )
        for row_index, entering_variable in [(0, 3), (1, 4), (2, 5)]:
            self.assertEqual(
                find_entering_variable(
                    tableau=tableau,
                    pivot_row_index=row_index,
                    non_basic_variables=set(range(3)),
                ),
                entering_variable,
            )

        tableau = np.array(
            [
                [3.0, 1.0, 3.0, 1.0, 0.0, 0.0, 1.0],
                [0.0, 0.0, -6.0, -3.0, 3.0, 0.0, 0.0],
                [0.0, 8.0, 6.0, -1.0, 0.0, 3.0, 2.0],
            ]
        )
        for row_index, entering_variable in [(0, 0), (1, 4), (2, 5)]:
            self.assertEqual(
                find_entering_variable(
                    tableau=tableau,
                    pivot_row_index=row_index,
                    non_basic_variables={1, 2, 3},
                ),
                entering_variable,
            )

    def test_particular_pivot(self):
        tableau = np.array(
            [
                [3.0, 3.0, 1.0, 0.0, 0.0, 1.0],
                [2.0, 5.0, 0.0, 1.0, 0.0, 1.0],
                [0.0, 6.0, 0.0, 0.0, 1.0, 1.0],
            ]
        )
        self.assertEqual(
            pivot_tableau_lex(
                tableau,
                column_index=0,
                slack_variables=range(2, 5),
                non_basic_variables={0, 1},
            ),
            2,
        )
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
        self.assertEqual(
            pivot_tableau_lex(
                tableau,
                column_index=2,
                slack_variables=range(2, 5),
                non_basic_variables={1, 2},
            ),
            0,
        )
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

        # degenerate cases
        tableau = np.array(
            [
                [3.0, 1.0, 3.0, 1.0, 0.0, 0.0, 1.0],
                [0.0, 0.0, -6.0, -3.0, 3.0, 0.0, 0.0],
                [0.0, 8.0, 6.0, -1.0, 0.0, 3.0, 2.0],
            ]
        )
        self.assertEqual(
            pivot_tableau_lex(
                tableau,
                column_index=1,
                slack_variables=range(3, 6),
                non_basic_variables={1, 2, 3},
            ),
            5,
        )
        next_tableau = np.array(
            [
                [24.0, 0.0, 18.0, 9.0, 0.0, -3.0, 6.0],
                [0.0, 0.0, -48.0, -24.0, 24.0, 0.0, 0.0],
                [0.0, 8.0, 6.0, -1.0, 0.0, 3.0, 2.0],
            ]
        )
        self.assertTrue(
            np.array_equal(tableau, next_tableau),
            msg="{} != {}".format(tableau, next_tableau),
        )

        tableau = np.array(
            [
                [10.0, 11.0, 10.0, 1.0, 0.0, 0.0, 1.0],
                [10.0, 11.0, 10.0, 0.0, 1.0, 0.0, 1.0],
                [10.0, 11.0, 1.0, 0.0, 0.0, 1.0, 1.0],
            ]
        )
        self.assertEqual(
            pivot_tableau_lex(
                tableau,
                column_index=0,
                slack_variables=range(3, 6),
                non_basic_variables={0, 1, 2},
            ),
            3,
        )
        next_tableau = np.array(
            [
                [10.0, 11.0, 10.0, 1.0, 0.0, 0.0, 1.0],
                [0.0, 0.0, 0.0, -10.0, 10.0, 0.0, 0.0],
                [0.0, 0.0, -90.0, -10.0, 0.0, 10.0, 0.0],
            ]
        )
        self.assertTrue(
            np.array_equal(tableau, next_tableau),
            msg="{} != {}".format(tableau, next_tableau),
        )
