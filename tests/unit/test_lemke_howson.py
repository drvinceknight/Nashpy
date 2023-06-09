import unittest
import warnings

import numpy as np

from nashpy.algorithms.lemke_howson import lemke_howson


class TestLemkeHowson(unittest.TestCase):
    """
    Tests for the Lemke Howson algorithm
    """

    def test_particular_lemke_howson_non_lex(self):
        A = np.array([[3, 3], [2, 5], [0, 6]])
        B = np.array([[3, 2], [2, 6], [3, 1]])
        for label, output in [
            (0, (np.array([1, 0, 0]), np.array([1, 0]))),
            (1, (np.array([0, 1 / 3, 2 / 3]), np.array([1 / 3, 2 / 3]))),
            (2, (np.array([1, 0, 0]), np.array([1, 0]))),
            (3, (np.array([1, 0, 0]), np.array([1, 0]))),
            (4, (np.array([0, 1 / 3, 2 / 3]), np.array([1 / 3, 2 / 3]))),
        ]:
            for eq, expected_eq in zip(lemke_howson(A, B, label, False), output):
                self.assertTrue(all(np.isclose(eq, expected_eq)))

        A = np.array([[1, -1], [-1, 1]])
        B = -A
        for label in range(4):
            for eq in lemke_howson(A, B, label):
                self.assertTrue(
                    all(np.isclose(eq, np.array([1 / 2, 1 / 2]))), msg=str(eq)
                )

    def test_degenerate_lemke_howson_non_lex_raises_warning(self):
        """
        This is a degenerate game so the algorithm fails.
        This was raised in
        https://github.com/drvinceknight/Nashpy/issues/35
        """
        A = np.array([[-1, -1, -1], [0, 0, 0], [-1, -1, -10000]])
        B = np.array([[-1, -1, -1], [0, 0, 0], [-1, -1, -10000]])
        with warnings.catch_warnings(record=True) as w:
            eqs = lemke_howson(A, B, initial_dropped_label=0, lexicographic=False)
            self.assertEqual(len(eqs[0]), 2)
            self.assertEqual(len(eqs[1]), 4)
            self.assertGreater(len(w), 0)
            self.assertEqual(w[-1].category, RuntimeWarning)

    def test_particular_lemke_howson_with_lexicographic_ratio_test(self):
        """
        Tests for Lemke Howson with lexographical ordering in a non-degenerate case
        """

        A = np.array([[3, 3], [2, 5], [0, 6]])
        B = np.array([[3, 2], [2, 6], [3, 1]])
        for label, output in [
            (0, (np.array([1, 0, 0]), np.array([1, 0]))),
            (1, (np.array([0, 1 / 3, 2 / 3]), np.array([1 / 3, 2 / 3]))),
            (2, (np.array([1, 0, 0]), np.array([1, 0]))),
            (3, (np.array([1, 0, 0]), np.array([1, 0]))),
            (4, (np.array([0, 1 / 3, 2 / 3]), np.array([1 / 3, 2 / 3]))),
        ]:
            eqs = lemke_howson(A, B, label)
            for eq, expected_eq in zip(eqs, output):
                self.assertTrue(all(np.isclose(eq, expected_eq)))

        A = np.array([[1, -1], [-1, 1]])
        B = -A
        for label in range(4):
            for eq in lemke_howson(A, B, label, lexicographic=True):
                self.assertTrue(
                    all(np.isclose(eq, np.array([1 / 2, 1 / 2]))), msg=str(eq)
                )

    def test_particular_lemke_howson_with_lexicographic_ratio_test_with_degenerate_games(
        self,
    ):
        A = np.array([[1, 3, 3], [3, 1, 3], [1, 3, 3]])
        B = np.array([[3, 3, 1], [1, 1, 3], [3, 1, 3]])
        for label in range(6):
            eqs = lemke_howson(A, B, label, lexicographic=True)
            for eq, expected_eq in zip(
                eqs,
                (np.array([0.5, 0.5, 0]), np.array([0, 0, 1])),
            ):
                self.assertTrue(all(np.isclose(eq, expected_eq)))
        """
        Tests for Lemke Howson with lexographical ordering in a degenerate case
        Test is taken from
        https://github.com/drvinceknight/Nashpy/issues/65
        """

        A = np.array([[-1, -1, -1], [0, 0, 0], [-1, -1, -10000]])
        B = np.array([[-1, -1, -1], [0, 0, 0], [-1, -1, -10000]])
        for label in range(6):
            for eq, expected_eq in zip(
                lemke_howson(A, B, label, lexicographic=True),
                (np.array([0, 1, 0]), np.array([1, 0, 0])),
            ):
                self.assertTrue(all(np.isclose(eq, expected_eq)))

    def test_lemke_howson_lex_degenerate_tie_breaking_looping(
        self,
    ):
        A = np.array(
            [
                [0.0, 0.5, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0],
                [0.711, 0.0, 0.0, 0.5, 1.0, 1.0, 1.0, 1.0, 1.0],
                [1.0, 0.672, 0.0, 0.0, 0.5, 1.0, 1.0, 1.0, 1.0],
                [1.0, 1.0, 0.667, 0.0, 0.0, 0.5, 1.0, 1.0, 1.0],
                [1.0, 1.0, 1.0, 0.579, 0.0, 0.0, 0.5, 1.0, 1.0],
                [1.0, 1.0, 1.0, 1.0, 0.5, 0.0, 0.0, 0.5, 1.0],
                [1.0, 1.0, 1.0, 1.0, 1.0, 0.5, 0.0, 0.0, 1.0],
                [1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 0.333, 0.0, 0.5],
                [1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 0.0],
            ]
        )
        B = 1 - A
        expected_reward = 0.75872890672  # from support vector calc
        nonnans = 0
        for label in range(sum(A.shape)):
            with self.subTest(label=label):
                eq = lemke_howson(A, B, label)
                if not (np.isnan(eq[0]).any() or np.isnan(eq[1]).any()):
                    nonnans += 1
                else:
                    continue
                reward = eq[0].dot(A).dot(eq[1].transpose())
                self.assertAlmostEqual(reward, expected_reward, delta=1e-7)
        self.assertGreaterEqual(
            nonnans, 14, msg="at least 14 eqs without nan values produced"
        )
