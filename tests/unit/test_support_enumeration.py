"""
Tests for the game class
"""

import unittest
import warnings

import numpy as np

from nashpy.algorithms.support_enumeration import (
    _already_seen,
    indifference_strategies,
    is_ne,
    obey_support,
    potential_support_pairs,
    powerset,
    solve_indifference,
    support_enumeration,
    support_ne_vertices,
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
            out[:2] for out in indifference_strategies(A, B, tol=10**-2)
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

    def test_already_seen(self):
        """Test duplicate detection for strategy pairs"""
        pair = (np.array([1.0, 0.0]), np.array([0.0, 1.0]))
        self.assertFalse(_already_seen(pair, []))
        self.assertTrue(_already_seen(pair, [pair]))

        near = (np.array([1.0 + 1e-10, 0.0]), np.array([0.0, 1.0]))
        self.assertTrue(_already_seen(near, [pair]))

        different_row = (np.array([0.0, 1.0]), np.array([0.0, 1.0]))
        self.assertFalse(_already_seen(different_row, [pair]))

        different_column = (np.array([1.0, 0.0]), np.array([1.0, 0.0]))
        self.assertFalse(_already_seen(different_column, [pair]))

        slightly_off = (np.array([0.9, 0.1]), np.array([0.0, 1.0]))
        self.assertTrue(_already_seen(slightly_off, [pair], atol=0.2))
        self.assertFalse(_already_seen(slightly_off, [pair], atol=1e-8))

    def _close_to_vertex(self, vertices, expected):
        return any(
            np.allclose(got[0], expected[0]) and np.allclose(got[1], expected[1])
            for got in vertices
        )

    def test_support_ne_vertices_issue_222(self):
        """Vertices of the NE segment from https://github.com/drvinceknight/Nashpy/issues/222"""
        A = np.array([[-3.0, 3.0], [-3.0, 5.0]])
        B = np.array([[2.0, 7.0], [4.0, 2.0]])

        vertices = support_ne_vertices(A, B, (0, 1), (0,))
        expected_limit_points = [
            (np.array([0.0, 1.0]), np.array([1.0, 0.0])),
            (np.array([2 / 7, 5 / 7]), np.array([1.0, 0.0])),
        ]
        self.assertEqual(len(vertices), 2)
        for expected in expected_limit_points:
            self.assertTrue(
                self._close_to_vertex(vertices, expected),
                msg="missing vertex {}: got {}".format(expected, vertices),
            )

        pure = support_ne_vertices(A, B, (1,), (0,))
        self.assertEqual(len(pure), 1)
        self.assertTrue(
            self._close_to_vertex(pure, expected_limit_points[0]),
            msg="missing pure vertex: got {}".format(pure),
        )

        self.assertEqual(support_ne_vertices(A, B, (0,), (0,)), [])

    def test_recovered_vertices_are_dropped_by_a_coarse_tolerance(self):
        """A recovered vertex with no mass above `tol` is not an equilibrium"""
        A = np.array([[-3.0, 3.0], [-3.0, 5.0]])
        B = np.array([[2.0, 7.0], [4.0, 2.0]])

        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            default = list(support_enumeration(A, B))
            coarse = list(support_enumeration(A, B, tol=0.8))

        # ([2/7, 5/7], [1, 0]) has no entry above 0.8 for the row player.
        self.assertEqual(len(default), 2)
        self.assertEqual(len(coarse), 1)
        self.assertTrue(np.allclose(coarse[0][0], np.array([0.0, 1.0])))

    def test_support_ne_vertices_on_empty_support(self):
        """An empty support has no vertices to enumerate"""
        A = np.array([[-3.0, 3.0], [-3.0, 5.0]])
        B = np.array([[2.0, 7.0], [4.0, 2.0]])
        self.assertEqual(support_ne_vertices(A, B, (), ()), [])
        self.assertEqual(support_ne_vertices(A, B, (0,), ()), [])
        self.assertEqual(support_ne_vertices(A, B, (), (0,)), [])

    def test_support_ne_vertices_skips_large_support_pairs(self):
        """Support pairs needing too many vertex solves are skipped"""
        A = np.zeros((6, 6))
        self.assertEqual(
            support_ne_vertices(A, A.copy(), (0, 1, 2, 3, 4, 5), (0, 1, 2, 3, 4, 5)),
            [],
        )

    def test_support_ne_vertices_row_pure_continuum(self):
        """Vertices of the row-pure continuum in the 3x2 degenerate example"""
        A = np.array([[3.0, 3.0], [2.0, 5.0], [0.0, 6.0]])
        B = np.array([[3.0, 3.0], [2.0, 6.0], [3.0, 1.0]])
        vertices = support_ne_vertices(A, B, (0,), (0, 1))
        expected_limit_points = [
            (np.array([1.0, 0.0, 0.0]), np.array([1.0, 0.0])),
            (np.array([1.0, 0.0, 0.0]), np.array([2 / 3, 1 / 3])),
        ]
        self.assertEqual(len(vertices), 2)
        for expected in expected_limit_points:
            self.assertTrue(
                self._close_to_vertex(vertices, expected),
                msg="missing vertex {}: got {}".format(expected, vertices),
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
