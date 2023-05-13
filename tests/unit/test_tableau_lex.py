"""
Tests for the integer pivoting
"""
import unittest

import numpy as np

from nashpy.linalg import TableauBuilder, TableauLex


class TestPolytope(unittest.TestCase):
    """
    Tests for the functions for integer pivoting
    """

    def test_find_particular_pivot_row_lex(self):
        tableau = TableauLex(np.array(
            [
                [3.0, 3.0, 1.0, 0.0, 0.0, 1.0],
                [2.0, 5.0, 0.0, 1.0, 0.0, 1.0],
                [0.0, 6.0, 0.0, 0.0, 1.0, 1.0],
            ]
        ))
        for column, row in [(0, 0), (1, 2), (2, 0), (3, 1), (4, 2)]:
            self.assertEqual(
                tableau._find_pivot_row(column),
                row,
            )

        tableau = TableauLex(np.array(
            [[3.0, 2.0, 3.0, 1.0, 0.0, 1.0], [2.0, 6.0, 1.0, 0.0, 1.0, 1.0]]
        ))
        for column, row in [(0, 0), (1, 1), (2, 0), (3, 0), (4, 1)]:
            self.assertEqual(
                tableau._find_pivot_row(column),
                row,
            )

        # degenerate case
        tableau = TableauLex(np.array(
            [
                [3.0, 1.0, 3.0, 1.0, 0.0, 0.0, 1.0],
                [0.0, 0.0, -6.0, -3.0, 3.0, 0.0, 0.0],
                [0.0, 8.0, 6.0, -1.0, 0.0, 3.0, 2.0],
            ]
        ), original_basic_labels=set([0,1,2]))
        slack_variables = [3, 4, 5]
        for column, row in [(0, 0), (1, 2), (2, 0), (3, 0), (4, 1)]:
            self.assertEqual(
                tableau._find_pivot_row(column),
                row,
            )

    def test_find_entering_variable(self):
        tableau = TableauLex(np.array(
            [
                [3.0, 1.0, 3.0, 1.0, 0.0, 0.0, 1.0],
                [3.0, 1.0, 1.0, 0.0, 1.0, 0.0, 1.0],
                [1.0, 3.0, 3.0, 0.0, 0.0, 1.0, 1.0],
            ]
        ))
        for row_index, entering_variable in [(0, 3), (1, 4), (2, 5)]:
            self.assertEqual(
                tableau._find_dropped(row_index, tableau.slack_variables),
                entering_variable,
            )

        tableau = TableauLex(np.array(
            [
                [3.0, 1.0, 3.0, 1.0, 0.0, 0.0, 1.0],
                [0.0, 0.0, -6.0, -3.0, 3.0, 0.0, 0.0],
                [0.0, 8.0, 6.0, -1.0, 0.0, 3.0, 2.0],
            ]
        ))
        for row_index, entering_variable in [(0, 0), (1, 4), (2, 5)]:
            self.assertEqual(
                tableau._find_dropped(row_index, tableau.labels-{1,2,3}),
                entering_variable,
            )

    def test_particular_pivot(self):
        tableau = TableauLex(np.array(
            [
                [3.0, 3.0, 1.0, 0.0, 0.0, 1.0],
                [2.0, 5.0, 0.0, 1.0, 0.0, 1.0],
                [0.0, 6.0, 0.0, 0.0, 1.0, 1.0],
            ]
        ))
        self.assertEqual(
            tableau.pivot_and_drop_label(0),
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
            np.array_equal(tableau._tableau, next_tableau),
            msg="{} != {}".format(tableau._tableau, next_tableau),
        )
        self.assertEqual(
            tableau.pivot_and_drop_label(2),
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
            np.array_equal(tableau._tableau, next_tableau),
            msg="{} != {}".format(tableau._tableau, next_tableau),
        )

    def test_degenerate_pivot(self):
        tableau = TableauLex(np.array(
            [
                [3.0, 1.0, 3.0, 1.0, 0.0, 0.0, 1.0],
                [0.0, 0.0, -6.0, -3.0, 3.0, 0.0, 0.0],
                [0.0, 8.0, 6.0, -1.0, 0.0, 3.0, 2.0],
            ]
        ), original_basic_labels=[0,1,2])
        tableau._non_basic_variables = set([1, 2, 3])
        self.assertEqual(
            tableau.pivot_and_drop_label(1),
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
            np.array_equal(tableau._tableau, next_tableau),
            msg="{} != {}".format(tableau._tableau, next_tableau),
        )

        tableau = TableauLex(np.array(
            [
                [10.0, 11.0, 10.0, 1.0, 0.0, 0.0, 1.0],
                [10.0, 11.0, 10.0, 0.0, 1.0, 0.0, 1.0],
                [10.0, 11.0, 1.0, 0.0, 0.0, 1.0, 1.0],
            ]
        ))
        self.assertEqual(
            tableau.pivot_and_drop_label(0),
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
            np.array_equal(tableau._tableau, next_tableau),
            msg="{} != {}".format(tableau._tableau, next_tableau),
        )
