import unittest
import warnings

import numpy as np

from nashpy.algorithms.lemke_howson import lemke_howson
from nashpy.linalg import TableauBuilder, Tableau


class TestLemkeHowson(unittest.TestCase):
    """
    Tests for the Lemke Howson algorithm
    """

    def test_col_tableau_creation(self):
        payoffs = np.array(
            [
                [3.0, 3.0],
                [2.0, 5.0],
                [0.0, 6.0],
            ]
        )
        t = TableauBuilder.column(payoffs).build()
        expected = np.array(
            [
                [1.0, 0.0, 0.0, 3.0, 3.0, 1.0],
                [0.0, 1.0, 0.0, 2.0, 5.0, 1.0],
                [0.0, 0.0, 1.0, 0.0, 6.0, 1.0],
            ]
        )
        self.assertTrue(
            np.array_equal(t._tableau, expected),
            msg="{} != {}".format(t._tableau, expected),
        )
        self.assertEqual(t.non_basic_variables, set([3, 4]))
        self.assertEqual(t._original_basic_labels, set([3, 4]))
        self.assertEqual(t.labels, set(range(sum(payoffs.shape))))

    def test_row_tableau_creation(self):
        payoffs = np.array(
            [
                [3.0, 3.0],
                [2.0, -5.0],
                [0.0, 1.0],
            ]
        )
        t = TableauBuilder.row(payoffs).make_positive().build()
        expected = np.array(
            [
                [9.0, 8.0, 6.0, 1.0, 0.0, 1.0],
                [9.0, 1.0, 7.0, 0.0, 1.0, 1.0],
            ]
        )
        self.assertTrue(
            np.array_equal(t._tableau, expected),
            msg="{} != {}".format(t._tableau, expected),
        )
        self.assertEqual(t.non_basic_variables, set([0, 1, 2]))
        self.assertEqual(t._original_basic_labels, set([0, 1, 2]))
        self.assertEqual(t.labels, set(range(sum(payoffs.shape))))

    def test_particular_tableau_to_strategy(self):
        t_arr = np.array(
            [
                [3.0, 0, 1.0, 1.0, 0.0, 1.0],
                [0.0, 0, 1.0, 1.0, 1.0, 1.0],
                [0.0, 6.0, 0.0, 0.0, 1.0, 1.0],
            ]
        )
        basic_labels = set([0, 1])
        strategy_labels = set([0, 1])
        t = Tableau(t_arr, strategy_labels)
        strategy = t.to_strategy(basic_labels)
        self.assertTrue(np.array_equal(strategy, np.array([2 / 3, 1 / 3])))

        t_arr = np.array(
            [
                [3.0, 0, 1.0, 0, 0.0, 1.0],
                [0.0, 3.0, 1.0, 3.0, 1.0, 1.0],
                [0.0, 6.0, 0.0, 0.0, 1.0, 1.0],
            ]
        )
        basic_labels = set([0, 3])
        strategy_labels = set([0, 1])
        t = Tableau(t_arr, strategy_labels)
        strategy = t.to_strategy(basic_labels)
        self.assertTrue(np.array_equal(strategy, np.array([1, 0])))

    def test_particular_lemke_howson(self):
        A = np.array([[3, 3], [2, 5], [0, 6]])
        B = np.array([[3, 2], [2, 6], [3, 1]])
        for label, output in [
            (0, (np.array([1, 0, 0]), np.array([1, 0]))),
            (1, (np.array([0, 1 / 3, 2 / 3]), np.array([1 / 3, 2 / 3]))),
            (2, (np.array([1, 0, 0]), np.array([1, 0]))),
            (3, (np.array([1, 0, 0]), np.array([1, 0]))),
            (4, (np.array([0, 1 / 3, 2 / 3]), np.array([1 / 3, 2 / 3]))),
        ]:
            for eq, expected_eq in zip(lemke_howson(A, B, label), output):
                self.assertTrue(all(np.isclose(eq, expected_eq)))

        A = np.array([[1, -1], [-1, 1]])
        B = -A
        for label in range(4):
            for eq in lemke_howson(A, B, label):
                self.assertTrue(
                    all(np.isclose(eq, np.array([1 / 2, 1 / 2]))), msg=str(eq)
                )

    def test_particular_lemke_howson_raises_warning(self):
        """
        This is a degenerate game so the algorithm fails.
        This was raised in
        https://github.com/drvinceknight/Nashpy/issues/35
        """
        A = np.array([[-1, -1, -1], [0, 0, 0], [-1, -1, -10000]])
        B = np.array([[-1, -1, -1], [0, 0, 0], [-1, -1, -10000]])
        with warnings.catch_warnings(record=True) as w:
            eqs = lemke_howson(A, B, initial_dropped_label=0)
            self.assertEqual(len(eqs[0]), 2)
            self.assertEqual(len(eqs[1]), 4)
            self.assertGreater(len(w), 0)
            self.assertEqual(w[-1].category, RuntimeWarning)
