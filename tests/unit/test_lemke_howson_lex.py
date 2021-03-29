import unittest

import numpy as np

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
            for eq, expected_eq in zip(lemke_howson_lex(A, B, label), output):
                self.assertTrue(all(np.isclose(eq, expected_eq)))

        A = np.array([[1, -1], [-1, 1]])
        B = -A
        for label in range(4):
            for eq in lemke_howson_lex(A, B, label):
                self.assertTrue(
                    all(np.isclose(eq, np.array([1 / 2, 1 / 2]))), msg=str(eq)
                )

    def test_particular_lemke_howson_with_lexicographic_ratio_test_with_degenerate_games(
        self,
    ):
        A = np.array([[1, 3, 3], [3, 1, 3], [1, 3, 3]])
        B = np.array([[3, 3, 1], [1, 1, 3], [3, 1, 3]])
        for label in range(6):
            for eq, expected_eq in zip(
                lemke_howson_lex(A, B, label),
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
                lemke_howson_lex(A, B, label),
                (np.array([0, 1, 0]), np.array([1, 0, 0])),
            ):
                self.assertTrue(all(np.isclose(eq, expected_eq)))
