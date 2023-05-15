import unittest

import numpy as np

from nashpy.algorithms.lemke_howson import lemke_howson
from nashpy.algorithms.lemke_howson_lex import lemke_howson_lex
class TestLemkeHowsonLex(unittest.TestCase):
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
            eqs = lemke_howson_lex(A, B, label)
            for eq, expected_eq in zip(eqs, output):
                self.assertTrue(all(np.isclose(eq, expected_eq)))

        A = np.array([[1, -1], [-1, 1]])
        B = -A
        for label in range(4):
            for eq in lemke_howson(A, B, label, "lex"):
                self.assertTrue(
                    all(np.isclose(eq, np.array([1 / 2, 1 / 2]))), msg=str(eq)
                )

    def test_particular_lemke_howson_with_lexicographic_ratio_test_with_degenerate_games(
        self,
    ):
        A = np.array([[1, 3, 3], [3, 1, 3], [1, 3, 3]])
        B = np.array([[3, 3, 1], [1, 1, 3], [3, 1, 3]])
        for label in range(6):
            eqs = lemke_howson(A, B, label, "lex")
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
                lemke_howson(A, B, label, "lex"),
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
        hits = 0
        for label in range(sum(A.shape)):
            with self.subTest(label=label):
                eq = lemke_howson_lex(A, B, label)
                print("EQ!: ", eq)
                #self.assertFalse(
                #    np.isnan(eq[0]).any() or np.isnan(eq[1]).any(),
                #    "strategy is not nan",
                #)
                if not (np.isnan(eq[0]).any() or np.isnan(eq[1]).any()):
                    hits += 1
                else:
                    continue
                reward = eq[0].dot(A).dot(eq[1].transpose())
                self.assertAlmostEqual(reward, expected_reward, delta=1e-7)
        self.assertEqual(hits, sum(A.shape))
