"""
Tests for the game class
"""
import unittest

import numpy as np

from nashpy.algorithms.support_enumeration import (
    indifference_strategies,
    is_ne,
    obey_support,
    potential_support_pairs,
    powerset,
    solve_indifference,
)


class TestSupportEnumeration(unittest.TestCase):
    def test_potential_supports(self):
        """Test for the enumeration of potential supports"""
        A = np.array([[1, 0], [-2, 3]])
        B = np.array([[3, 2], [-1, 0]])
        self.assertEqual(
            list(potential_support_pairs(A, B)),
            [
                ((0,), (0,)),
                ((0,), (1,)),
                ((0,), (0, 1)),
                ((1,), (0,)),
                ((1,), (1,)),
                ((1,), (0, 1)),
                ((0, 1), (0,)),
                ((0, 1), (1,)),
                ((0, 1), (0, 1)),
            ],
        )

        A = np.array([[1, 0, 2], [-2, 3, 9]])
        B = np.array([[3, 2, 1], [-1, 0, 2]])
        self.assertEqual(
            list(potential_support_pairs(A, B)),
            [
                ((0,), (0,)),
                ((0,), (1,)),
                ((0,), (2,)),
                ((0,), (0, 1)),
                ((0,), (0, 2)),
                ((0,), (1, 2)),
                ((0,), (0, 1, 2)),
                ((1,), (0,)),
                ((1,), (1,)),
                ((1,), (2,)),
                ((1,), (0, 1)),
                ((1,), (0, 2)),
                ((1,), (1, 2)),
                ((1,), (0, 1, 2)),
                ((0, 1), (0,)),
                ((0, 1), (1,)),
                ((0, 1), (2,)),
                ((0, 1), (0, 1)),
                ((0, 1), (0, 2)),
                ((0, 1), (1, 2)),
                ((0, 1), (0, 1, 2)),
            ],
        )

        A = np.array([[1, 0], [-2, 3], [2, 1]])
        B = np.array([[3, 2], [-1, 0], [5, 2]])
        self.assertEqual(
            list(potential_support_pairs(A, B)),
            [
                ((0,), (0,)),
                ((0,), (1,)),
                ((0,), (0, 1)),
                ((1,), (0,)),
                ((1,), (1,)),
                ((1,), (0, 1)),
                ((2,), (0,)),
                ((2,), (1,)),
                ((2,), (0, 1)),
                ((0, 1), (0,)),
                ((0, 1), (1,)),
                ((0, 1), (0, 1)),
                ((0, 2), (0,)),
                ((0, 2), (1,)),
                ((0, 2), (0, 1)),
                ((1, 2), (0,)),
                ((1, 2), (1,)),
                ((1, 2), (0, 1)),
                ((0, 1, 2), (0,)),
                ((0, 1, 2), (1,)),
                ((0, 1, 2), (0, 1)),
            ],
        )

        A = np.array(
            [
                [52.46337363, 69.47195938, 0.0, 54.14372075],
                [77.0, 88.0, 84.85714286, 92.4],
                [77.78571429, 87.35294118, 93.5, 91.38461538],
                [66.37100751, 43.4530444, 0.0, 60.36191831],
            ]
        )
        B = np.array(
            [
                [23.52690518, 17.35459006, 88.209, 20.8021711],
                [16.17165, 0.0, 14.00142857, 6.46866],
                [0.0, 5.76529412, 0.0, 0.0],
                [15.68327304, 40.68156322, 84.00857143, 11.06596804],
            ]
        )
        number_of_potential_supports = len(list(potential_support_pairs(A, B)))
        assert number_of_potential_supports == 225

    def test_potential_supports_with_non_degenerate_flag(self):
        """Test for the enumeration of potential supports when constrained to
        non degenerate games"""
        A = np.array([[1, 0], [-2, 3]])
        B = np.array([[3, 2], [-1, 0]])
        self.assertEqual(
            list(potential_support_pairs(A, B, non_degenerate=True)),
            [
                ((0,), (0,)),
                ((0,), (1,)),
                ((1,), (0,)),
                ((1,), (1,)),
                ((0, 1), (0, 1)),
            ],
        )

        A = np.array([[1, 0, 2], [-2, 3, 9]])
        B = np.array([[3, 2, 1], [-1, 0, 2]])
        self.assertEqual(
            list(potential_support_pairs(A, B, non_degenerate=True)),
            [
                ((0,), (0,)),
                ((0,), (1,)),
                ((0,), (2,)),
                ((1,), (0,)),
                ((1,), (1,)),
                ((1,), (2,)),
                ((0, 1), (0, 1)),
                ((0, 1), (0, 2)),
                ((0, 1), (1, 2)),
            ],
        )

        A = np.array([[1, 0], [-2, 3], [2, 1]])
        B = np.array([[3, 2], [-1, 0], [5, 2]])
        self.assertEqual(
            list(potential_support_pairs(A, B, non_degenerate=True)),
            [
                ((0,), (0,)),
                ((0,), (1,)),
                ((1,), (0,)),
                ((1,), (1,)),
                ((2,), (0,)),
                ((2,), (1,)),
                ((0, 1), (0, 1)),
                ((0, 2), (0, 1)),
                ((1, 2), (0, 1)),
            ],
        )

    def test_indifference_strategies(self):
        """Test for the indifference strategies of potential supports"""
        A = np.array([[2, 1], [0, 2]])
        B = np.array([[2, 0], [1, 2]])
        expected_indifference = [
            (np.array([1, 0]), np.array([1, 0])),
            (np.array([1, 0]), np.array([0, 1])),
            (np.array([0, 1]), np.array([1, 0])),
            (np.array([0, 1]), np.array([0, 1])),
            (np.array([1 / 3, 2 / 3]), np.array([1 / 3, 2 / 3])),
        ]
        obtained_indifference = [out[:2] for out in indifference_strategies(A, B)]
        self.assertEqual(len(obtained_indifference), len(expected_indifference))
        for obtained, expected in zip(obtained_indifference, expected_indifference):
            self.assertTrue(
                np.array_equal(obtained, expected),
                msg="obtained: {} !=expected: {}".format(obtained, expected),
            )

    def test_indifference_strategies_with_non_degenerate(self):
        """Test for the indifference strategies of potential supports"""
        A = np.array([[2, 1], [0, 2]])
        B = np.array([[2, 0], [1, 2]])
        expected_indifference = [
            (np.array([1, 0]), np.array([1, 0])),
            (np.array([1, 0]), np.array([0, 1])),
            (np.array([0, 1]), np.array([1, 0])),
            (np.array([0, 1]), np.array([0, 1])),
            (np.array([1 / 3, 2 / 3]), np.array([1 / 3, 2 / 3])),
        ]
        obtained_indifference = [
            out[:2] for out in indifference_strategies(A, B, non_degenerate=True)
        ]
        self.assertEqual(len(obtained_indifference), len(expected_indifference))
        for obtained, expected in zip(obtained_indifference, expected_indifference):
            self.assertTrue(
                np.array_equal(obtained, expected),
                msg="obtained: {} !=expected: {}".format(obtained, expected),
            )

    def test_indifference_strategies_with_high_tolerance(self):
        """Test for the indifference strategies of potential supports"""
        A = np.array([[2, 1], [0, 2]])
        B = np.array([[2, 0], [1, 2]])
        expected_indifference = [
            (np.array([1, 0]), np.array([1, 0])),
            (np.array([1, 0]), np.array([0, 1])),
            (np.array([0, 1]), np.array([1, 0])),
            (np.array([0, 1]), np.array([0, 1])),
            (np.array([1 / 3, 2 / 3]), np.array([1 / 3, 2 / 3])),
        ]
        obtained_indifference = [
            out[:2] for out in indifference_strategies(A, B, tol=10 ** -2)
        ]
        self.assertEqual(len(obtained_indifference), len(expected_indifference))
        for obtained, expected in zip(obtained_indifference, expected_indifference):
            self.assertTrue(
                np.array_equal(obtained, expected),
                msg="obtained: {} !=expected: {}".format(obtained, expected),
            )

    def test_obey_support(self):
        """Test for obey support"""
        self.assertFalse(obey_support(False, np.array([0, 1])))
        self.assertFalse(obey_support(np.array([1, 0]), np.array([0, 1])))
        self.assertFalse(obey_support(np.array([0, 0.5]), np.array([0])))
        self.assertFalse(obey_support(np.array([0.5, 0]), np.array([1])))

        self.assertTrue(obey_support(np.array([1, 0]), np.array([0])))
        self.assertTrue(obey_support(np.array([0, 0.5]), np.array([1])))
        self.assertTrue(obey_support(np.array([0.5, 0]), np.array([0])))
        self.assertTrue(obey_support(np.array([0.5, 0.5]), np.array([0, 1])))

    def test_obey_support_with_high_tolerance(self):
        """Test for obey support"""
        tol = 1
        self.assertFalse(obey_support(False, np.array([0, 1])))
        self.assertFalse(obey_support(np.array([1, 0]), np.array([0, 1]), tol=tol))
        self.assertFalse(obey_support(np.array([1, 0]), np.array([0]), tol=tol))
        self.assertFalse(obey_support(np.array([0, 0.5]), np.array([1]), tol=tol))
        self.assertFalse(obey_support(np.array([0.5, 0]), np.array([0]), tol=tol))
        self.assertFalse(obey_support(np.array([0.5, 0.5]), np.array([0, 1]), tol=tol))

    def test_is_ne(self):
        """Test if is ne"""
        A = np.array([[2, 1], [0, 2]])
        B = np.array([[2, 0], [1, 2]])

        strategy_pair = np.array([1, 0]), np.array([1, 0])
        support_pair = [0], [0]
        self.assertTrue(is_ne(strategy_pair, support_pair, (A, B)))

        strategy_pair = np.array([1 / 3, 2 / 3]), np.array([1 / 3, 2 / 3])
        support_pair = [0, 1], [0, 1]
        self.assertTrue(is_ne(strategy_pair, support_pair, (A, B)))

        strategy_pair = np.array([0, 1]), np.array([1, 0])
        support_pair = [1], [0]
        self.assertFalse(is_ne(strategy_pair, support_pair, (A, B)))

        strategy_pair = np.array([1, 0]), np.array([0, 1])
        support_pair = [0], [1]
        self.assertFalse(is_ne(strategy_pair, support_pair, (A, B)))

        A = np.array([[1, -1], [-1, 1]])
        strategy_pair = np.array([1 / 2, 1 / 2]), np.array([1 / 2, 1 / 2])
        support_pair = [0, 1], [0, 1]
        self.assertTrue(is_ne(strategy_pair, support_pair, (A, -A)))

        A = np.array([[0, 1, -1], [-1, 0, 1], [1, -1, 0]])
        strategy_pair = (
            np.array([1 / 3, 1 / 3, 1 / 3]),
            np.array([1 / 3, 1 / 3, 1 / 3]),
        )
        support_pair = [0, 1, 2], [0, 1, 2]
        self.assertTrue(is_ne(strategy_pair, support_pair, (A, -A)))

        strategy_pair = (np.array([1, 0, 0]), np.array([1, 0, 0]))
        support_pair = [0], [0]
        self.assertFalse(is_ne(strategy_pair, support_pair, (A, -A)))

        A = np.array([[160, 205, 44], [175, 180, 45], [201, 204, 50], [120, 207, 49]])
        B = np.array([[2, 2, 2], [1, 0, 0], [3, 4, 1], [4, 1, 2]])
        self.assertTrue(
            is_ne(
                (
                    np.array((0, 0, 3 / 4, 1 / 4)),
                    np.array((1 / 28, 27 / 28, 0)),
                ),
                (np.array([2, 3]), np.array([0, 1])),
                (A, B),
            )
        )

    def test_solve_indifference(self):
        """Test solve indifference"""
        A = np.array([[0, 1, -1], [1, 0, 1], [-1, 1, 0]])

        rows = [0, 1]
        columns = [0, 1]
        self.assertTrue(
            np.array_equal(
                solve_indifference(A, rows, columns), np.array([0.5, 0.5, 0.0])
            )
        )

        rows = [1, 2]
        columns = [0, 1]
        self.assertTrue(
            all(
                np.isclose(
                    solve_indifference(A, rows, columns),
                    np.array([1 / 3, 2 / 3, 0.0]),
                )
            )
        )

        rows = [0, 2]
        columns = [0, 1]
        self.assertTrue(
            np.array_equal(
                solve_indifference(A, rows, columns), np.array([0.0, 1.0, 0.0])
            )
        )

        rows = [0, 1, 2]
        columns = [0, 1, 2]
        self.assertTrue(
            all(
                np.isclose(
                    solve_indifference(A, rows, columns),
                    np.array([0.2, 0.6, 0.2]),
                )
            )
        )


class TestUtils(unittest.TestCase):
    def test_powerset(self):
        n = 2
        powerset_ = list(powerset(n))
        self.assertEqual(powerset_, [(), (0,), (1,), (0, 1)])

        n = 3
        powerset_ = list(powerset(n))
        self.assertEqual(
            powerset_, [(), (0,), (1,), (2,), (0, 1), (0, 2), (1, 2), (0, 1, 2)]
        )
