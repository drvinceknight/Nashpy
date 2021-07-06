"""
Tests for the game class
"""

import unittest
import warnings

import numpy as np
from hypothesis import given
from hypothesis.extra.numpy import arrays
from hypothesis.strategies import integers
import pytest

import nashpy as nash
import nashpy.learning


class TestGame(unittest.TestCase):
    """
    Tests for the game class
    """

    @given(A=arrays(np.int8, (4, 5)), B=arrays(np.int8, (4, 5)))
    def test_bi_matrix_init(self, A, B):
        """Test that can create a bi matrix game"""
        g = nash.Game(A, B)
        self.assertEqual(g.payoff_matrices, (A, B))
        if np.array_equal(A, -B):  # Check if A or B are non zero
            self.assertTrue(g.zero_sum)
        else:
            self.assertFalse(g.zero_sum)

        # Can also init with lists
        A = A.tolist()
        B = B.tolist()
        g = nash.Game(A, B)
        self.assertTrue(np.array_equal(g.payoff_matrices[0], np.asarray(A)))
        self.assertTrue(np.array_equal(g.payoff_matrices[1], np.asarray(B)))

    def test_incorrect_dimensions_init(self):
        """Tests that ValueError is raised for unequal dimensions"""
        A = np.array([[1, 2, 3], [4, 5, 6]])
        B = np.array([[1, 2], [3, 4]])

        with pytest.raises(ValueError):
            nash.Game(A, B)

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
        self.assertTrue(np.array_equal(g.payoff_matrices[0], -g.payoff_matrices[1]))
        self.assertTrue(g.zero_sum)

        # Can also init with lists
        A = A.tolist()
        g = nash.Game(A)
        self.assertTrue(np.array_equal(g.payoff_matrices[0], np.asarray(A)))
        self.assertTrue(np.array_equal(g.payoff_matrices[0], -g.payoff_matrices[1]))
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
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
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
        A = np.array([[160, 205, 44], [175, 180, 45], [201, 204, 50], [120, 207, 49]])
        B = np.array([[2, 2, 2], [1, 0, 0], [3, 4, 1], [4, 1, 2]])
        g = nash.Game(A, B)
        expected_equilibria = [
            (np.array([0, 0, 3 / 4, 1 / 4]), np.array([1 / 28, 27 / 28, 0]))
        ]
        for obtained, expected in zip(g.support_enumeration(), expected_equilibria):
            for s1, s2 in zip(obtained, expected):
                self.assertTrue(
                    np.array_equal(s1, s2),
                    msg="obtained: {} !=expected: {}".format(obtained, expected),
                )

        A = np.array([[1, 0], [-2, 3]])
        B = np.array([[3, 2], [-1, 0]])
        g = nash.Game(A, B)
        expected_equilibria = [
            (np.array([1, 0]), np.array([1, 0])),
            (np.array([0, 1]), np.array([0, 1])),
            (np.array([1 / 2, 1 / 2]), np.array([1 / 2, 1 / 2])),
        ]
        for obtained, expected in zip(g.support_enumeration(), expected_equilibria):
            for s1, s2 in zip(obtained, expected):
                self.assertTrue(
                    np.array_equal(s1, s2),
                    msg="obtained: {} !=expected: {}".format(obtained, expected),
                )

        A = np.array([[2, 1], [0, 2]])
        B = np.array([[2, 0], [1, 2]])
        g = nash.Game(A, B)
        expected_equilibria = [
            (np.array([1, 0]), np.array([1, 0])),
            (np.array([0, 1]), np.array([0, 1])),
            (np.array([1 / 3, 2 / 3]), np.array([1 / 3, 2 / 3])),
        ]
        for obtained, expected in zip(g.support_enumeration(), expected_equilibria):
            for s1, s2 in zip(obtained, expected):
                self.assertTrue(
                    np.array_equal(s1, s2),
                    msg="obtained: {} !=expected: {}".format(obtained, expected),
                )

    def test_support_enumeration_for_degenerate_bi_matrix_game(self):
        """Test for the equilibria calculation support enumeration with a
        degenerate game"""
        A = np.array([[-1, 0], [-1, 1]])
        B = np.array([[1, 0], [1, -1]])
        g = nash.Game(A, B)
        expected_equilibria = [
            (np.array([1, 0]), np.array([1, 0])),
            (np.array([0, 1]), np.array([1, 0])),
        ]
        with warnings.catch_warnings(record=True) as w:
            obtained_equilibria = list(g.support_enumeration())
            for obtained, expected in zip(obtained_equilibria, expected_equilibria):
                for s1, s2 in zip(obtained, expected):
                    self.assertTrue(
                        np.array_equal(s1, s2),
                        msg="obtained: {} !=expected: {}".format(obtained, expected),
                    )
            self.assertGreater(len(w), 0)
            self.assertEqual(w[-1].category, RuntimeWarning)

        A = np.array([[3, 3], [2, 5], [0, 6]])
        B = np.array([[3, 3], [2, 6], [3, 1]])
        g = nash.Game(A, B)
        expected_equilibria = [
            (np.array([1, 0, 0]), np.array([1, 0])),
            (np.array([0, 1 / 3, 2 / 3]), np.array([1 / 3, 2 / 3])),
        ]
        with warnings.catch_warnings(record=True) as w:
            obtained_equilibria = list(g.support_enumeration())
            for obtained, expected in zip(obtained_equilibria, expected_equilibria):
                for s1, s2 in zip(obtained, expected):
                    self.assertTrue(
                        np.allclose(s1, s2),
                        msg="obtained: {} !=expected: {}".format(obtained, expected),
                    )
            self.assertGreater(len(w), 0)
            self.assertEqual(w[-1].category, RuntimeWarning)

        A = np.array([[0, 0], [0, 0]])
        B = np.array([[0, 0], [0, 0]])
        g = nash.Game(A, B)
        expected_equilibria = [
            (np.array([1, 0]), np.array([1, 0])),
            (np.array([1, 0]), np.array([0, 1])),
            (np.array([0, 1]), np.array([1, 0])),
            (np.array([0, 1]), np.array([0, 1])),
        ]
        with warnings.catch_warnings(record=True) as w:
            obtained_equilibria = list(g.support_enumeration())
            for obtained, expected in zip(obtained_equilibria, expected_equilibria):
                for s1, s2 in zip(obtained, expected):
                    self.assertTrue(
                        np.allclose(s1, s2),
                        msg="obtained: {} !=expected: {}".format(obtained, expected),
                    )
            self.assertGreater(len(w), 0)
            self.assertEqual(w[-1].category, RuntimeWarning)

    def test_support_enumeration_for_deg_bi_matrix_game_with_non_deg(self):

        A = np.array([[0, 0], [0, 0]])
        g = nash.Game(A)
        with warnings.catch_warnings(record=True) as w:
            obtained_equilibria = list(g.support_enumeration(non_degenerate=True))
            self.assertEqual(len(obtained_equilibria), 4)
            self.assertGreater(len(w), 0)
            self.assertEqual(w[-1].category, RuntimeWarning)

    def test_support_enumeration_for_deg_bi_matrix_game_with_low_tol(self):

        A = np.array([[0, 0], [0, 0]])
        g = nash.Game(A)
        with warnings.catch_warnings(record=True) as w:
            obtained_equilibria = list(g.support_enumeration(tol=0))
            self.assertEqual(len(obtained_equilibria), 4)
            self.assertGreater(len(w), 0)
            self.assertEqual(w[-1].category, RuntimeWarning)

    def test_support_enumeration_for_particular_game(self):
        """
        This particular game was raised in
        https://github.com/drvinceknight/Nashpy/issues/67. Two users reported
        that it
        did not return any equilibria under support enumeration. I was unable to
        reproduce this error locally as I was using a pre compiled install of
        numpy. However when using a pip installed version I was able to
        reproduce the error.

        Rounding the particular input matrices to 5 decimal places however fixes
        the error. This is an underlying precision error related to numpy (I
        think).
        """
        A = [
            [52.46337363, 69.47195938, 0.0, 54.14372075],
            [77.0, 88.0, 84.85714286, 92.4],
            [77.78571429, 87.35294118, 93.5, 91.38461538],
            [66.37100751, 43.4530444, 0.0, 60.36191831],
        ]
        B = [
            [23.52690518, 17.35459006, 88.209, 20.8021711],
            [16.17165, 0.0, 14.00142857, 6.46866],
            [0.0, 5.76529412, 0.0, 0.0],
            [15.68327304, 40.68156322, 84.00857143, 11.06596804],
        ]
        A = np.round(A, 5)
        B = np.round(B, 5)
        game = nash.Game(A, B)
        eqs = list(game.support_enumeration())
        assert len(eqs) == 1
        row_strategy, col_strategy = eqs[0]
        expected_row_strategy, expected_column_strategy = (
            np.array([7.33134761e-17, 2.62812089e-01, 7.37187911e-01, 0.00000000e00]),
            np.array([0.4516129, 0.5483871, 0.0, 0.0]),
        )
        assert np.all(np.isclose(row_strategy, expected_row_strategy))
        assert np.all(np.isclose(col_strategy, expected_column_strategy))

    def test_vertex_enumeration_for_bi_matrix(self):
        """Test for the equilibria calculation using vertex enumeration"""
        A = np.array([[160, 205, 44], [175, 180, 45], [201, 204, 50], [120, 207, 49]])
        B = np.array([[2, 2, 2], [1, 0, 0], [3, 4, 1], [4, 1, 2]])
        g = nash.Game(A, B)
        expected_equilibria = [
            (np.array([0, 0, 3 / 4, 1 / 4]), np.array([1 / 28, 27 / 28, 0]))
        ]
        for obtained, expected in zip(g.vertex_enumeration(), expected_equilibria):
            for s1, s2 in zip(obtained, expected):
                self.assertTrue(
                    all(np.isclose(s1, s2)),
                    msg="obtained: {} !=expected: {}".format(obtained, expected),
                )

        A = np.array([[1, 0], [-2, 3]])
        B = np.array([[3, 2], [-1, 0]])
        g = nash.Game(A, B)
        expected_equilibria = [
            (np.array([1, 0]), np.array([1, 0])),
            (np.array([0, 1]), np.array([0, 1])),
            (np.array([1 / 2, 1 / 2]), np.array([1 / 2, 1 / 2])),
        ]
        for obtained, expected in zip(g.vertex_enumeration(), expected_equilibria):
            for s1, s2 in zip(obtained, expected):
                self.assertTrue(
                    all(np.isclose(s1, s2)),
                    msg="obtained: {} !=expected: {}".format(obtained, expected),
                )

        A = np.array([[2, 1], [0, 2]])
        B = np.array([[2, 0], [1, 2]])
        g = nash.Game(A, B)
        expected_equilibria = [
            (np.array([1, 0]), np.array([1, 0])),
            (np.array([0, 1]), np.array([0, 1])),
            (np.array([1 / 3, 2 / 3]), np.array([1 / 3, 2 / 3])),
        ]
        for obtained, expected in zip(g.vertex_enumeration(), expected_equilibria):
            for s1, s2 in zip(obtained, expected):
                self.assertTrue(
                    all(np.isclose(s1, s2)),
                    msg="obtained: {} !=expected: {}".format(obtained, expected),
                )

    def test_lemke_howson_for_bi_matrix(self):
        """Test for the equilibria calculation using lemke howson"""
        A = np.array([[160, 205, 44], [175, 180, 45], [201, 204, 50], [120, 207, 49]])
        B = np.array([[2, 2, 2], [1, 0, 0], [3, 4, 1], [4, 1, 2]])
        g = nash.Game(A, B)
        expected_equilibria = (
            np.array([0, 0, 3 / 4, 1 / 4]),
            np.array([1 / 28, 27 / 28, 0]),
        )
        equilibria = g.lemke_howson(initial_dropped_label=4)
        for eq, expected in zip(equilibria, expected_equilibria):
            self.assertTrue(all(np.isclose(eq, expected)))

    def test_particular_lemke_howson_raises_warning(self):
        """
        This is a degenerate game so the algorithm fails.
        This was raised in
        https://github.com/drvinceknight/Nashpy/issues/35
        """
        A = np.array([[-1, -1, -1], [0, 0, 0], [-1, -1, -10000]])
        B = np.array([[-1, -1, -1], [0, 0, 0], [-1, -1, -10000]])
        game = nash.Game(A, B)
        with warnings.catch_warnings(record=True) as w:
            eqs = game.lemke_howson(initial_dropped_label=0)
            self.assertEqual(len(eqs[0]), 2)
            self.assertEqual(len(eqs[1]), 4)
            self.assertGreater(len(w), 0)
            self.assertEqual(w[-1].category, RuntimeWarning)

    def test_lemke_howson_enumeration(self):
        """Test for the enumeration of equilibrium using Lemke Howson"""
        A = np.array([[3, 1], [0, 2]])
        B = np.array([[2, 1], [0, 3]])
        g = nash.Game(A, B)
        expected_equilibria = [
            (np.array([1, 0]), np.array([1, 0])),
            (np.array([0, 1]), np.array([0, 1])),
        ] * 2
        equilibria = g.lemke_howson_enumeration()
        for equilibrium, expected_equilibrium in zip(equilibria, expected_equilibria):
            for strategy, expected_strategy in zip(equilibrium, expected_equilibrium):
                self.assertTrue(all(np.isclose(strategy, expected_strategy)))

        A = np.array([[3, 1], [1, 3]])
        B = np.array([[1, 3], [3, 1]])
        g = nash.Game(A, B)
        expected_equilibria = [(np.array([1 / 2, 1 / 2]), np.array([1 / 2, 1 / 2]))] * 4
        equilibria = g.lemke_howson_enumeration()
        for equilibrium, expected_equilibrium in zip(equilibria, expected_equilibria):
            for strategy, expected_strategy in zip(equilibrium, expected_equilibrium):
                self.assertTrue(all(np.isclose(strategy, expected_strategy)))

    def test_get_item(self):
        """Test solve indifference"""
        A = np.array([[1, -1], [-1, 1]])
        g = nash.Game(A)

        row_strategy = [0, 1]
        column_strategy = [1, 0]
        self.assertTrue(
            np.array_equal(g[row_strategy, column_strategy], np.array((-1, 1)))
        )

        row_strategy = [1 / 2, 1 / 2]
        column_strategy = [1 / 2, 1 / 2]
        self.assertTrue(
            np.array_equal(g[row_strategy, column_strategy], np.array((0, 0)))
        )

    @given(
        A=arrays(np.int8, (4, 5)),
        B=arrays(np.int8, (4, 5)),
        seed=integers(min_value=0, max_value=2 ** 32 - 1),
    )
    def test_fictitious_play(self, A, B, seed):
        """Test for the fictitious play algorithm"""
        g = nash.Game(A, B)
        iterations = 25
        np.random.seed(seed)
        expected_outcome = tuple(
            nashpy.learning.fictitious_play.fictitious_play(
                *g.payoff_matrices, iterations=iterations
            )
        )
        np.random.seed(seed)
        outcome = tuple(g.fictitious_play(iterations=iterations))
        assert len(outcome) == iterations + 1
        assert len(expected_outcome) == iterations + 1
        for plays, expected_plays in zip(outcome, expected_outcome):
            row_play, column_play = plays
            expected_row_play, expected_column_play = expected_plays
            assert np.array_equal(row_play, expected_row_play)
            assert np.array_equal(column_play, expected_column_play)
        # assert expected_outcome == outcome

    @given(
        A=arrays(np.int8, (4, 3), elements=integers(1, 20)),
        B=arrays(np.int8, (4, 3), elements=integers(1, 20)),
        seed=integers(min_value=0, max_value=2 ** 32 - 1),
    )
    def test_stochastic_fictitious_play(self, A, B, seed):
        """Test for the stochastic fictitious play algorithm"""
        np.random.seed(seed)
        iterations = 10
        g = nash.Game(A, B)

        expected_outcome = tuple(
            nashpy.learning.stochastic_fictitious_play.stochastic_fictitious_play(
                *g.payoff_matrices, iterations=iterations
            )
        )
        np.random.seed(seed)
        outcome = tuple(g.stochastic_fictitious_play(iterations=iterations))
        assert len(outcome) == iterations + 1
        assert len(expected_outcome) == iterations + 1
        for (plays, distributions), (
            expected_plays,
            expected_distributions,
        ) in zip(outcome, expected_outcome):
            row_play, column_play = plays
            expected_row_play, expected_column_play = expected_plays
            row_dist, column_dist = distributions
            expected_row_dist, expected_column_dist = expected_distributions
        assert np.allclose(column_dist, expected_column_dist)
        assert np.allclose(row_dist, expected_row_dist)
        assert np.allclose(column_play, expected_column_play)
        assert np.allclose(row_play, expected_row_play)

    def test_replicator_dynamics(self):
        """Test for the replicator dynamics algorithm"""
        A = np.array([[3, 2], [4, 1]])
        game = nash.Game(A)
        y0 = np.array([0.9, 0.1])
        timepoints = np.linspace(0, 10, 100)
        xs = game.replicator_dynamics(y0, timepoints)
        expected_xs = np.array([[0.50449178, 0.49550822]])
        assert np.allclose(xs[-1], expected_xs)

    def test_replicator_dynamics_5x5(self):
        """Test for the replicator dynamics algorithm with a 5x5 matrix"""
        A = np.array(
            [
                [3, 2, 4, 2, 3],
                [5, 1, 1, 3, 2],
                [6, 2, 3, 2, 1],
                [1, 3, 4, 7, 2],
                [1, 4, 4, 1, 3],
            ]
        )
        game = nash.Game(A)
        y0 = np.array([0.1, 0.1, 0.3, 0.2, 0.3])
        timepoints = np.linspace(0, 10, 100)
        xs = game.replicator_dynamics(y0, timepoints)
        expected_xs = np.array(
            [
                [
                    -5.35867454e-13,
                    -2.93213324e-11,
                    -9.66651436e-13,
                    1.00000000e00,
                    -1.78136715e-14,
                ]
            ]
        )
        assert np.allclose(xs[-1], expected_xs)

    def test_asymmetric_replicator_dynamics(self):
        """Test for asymmetric replicator dynamics algorithm"""
        A = np.array([[5, 1], [4, 2]])
        B = np.array([[3, 5], [2, 1]])
        game = nash.Game(A, B)

        x0 = np.array([0.6, 0.4])
        y0 = np.array([0.5, 0.5])
        timepoints = np.linspace(0, 100, 100)
        xs_A, xs_B = game.asymmetric_replicator_dynamics(
            x0=x0, y0=y0, timepoints=timepoints
        )

        expected_A_xs = np.array([0.17404745, 0.82595255])
        expected_B_xs = np.array([0.28121086, 0.71878914])
        assert np.allclose(xs_A[-1], expected_A_xs)
        assert np.allclose(xs_B[-1], expected_B_xs)

    def test_is_best_response(self):
        """Test for the best response check"""
        A = np.array([[3, 0], [5, 1]])
        B = np.array([[3, 5], [0, 1]])
        game = nash.Game(A, B)

        sigma_r = np.array([0, 1])
        sigma_c = np.array([1, 0])

        row_check, column_check = game.is_best_response(sigma_r, sigma_c)
        assert row_check is True
        assert column_check is False
