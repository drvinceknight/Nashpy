import unittest
import numpy as np

from nash.algorithms.lemke_howson import shift_tableau, lemke_howson


class TestLemkeHowson(unittest.TestCase):
    """
    Tests for the Lemke Howson algorithm
    """
    def test_particular_shift_tableau(self):
        tableau = np.array([[ 3.,  3.,  1.,  0.,  0.,  1.],
                            [ 2.,  5.,  0.,  1.,  0.,  1.],
                            [ 0.,  6.,  0.,  0.,  1.,  1.]])
        expected_shift = np.array([[1.,  0.,  0.,  3.,  3.,  1.],
                                   [0.,  1.,  0.,  2.,  5.,  1.],
                                   [0.,  0.,  1.,  0.,  6.,  1.]])
        shift = shift_tableau(tableau, (3, 2))
        self.assertTrue(np.array_equal(shift, expected_shift),
                        msg="{} != {}".format(shift, expected_shift))

    def test_particular_lemke_howson(self):
        A = np.array([[3, 3], [2, 5], [0, 6]])
        B = np.array([[3, 2], [2, 6], [3, 1]])
        for label, output in [
          (0, (np.array([1, 0, 0]), np.array([1, 0]))),
          (1, (np.array([0, 1 / 3,  2 / 3]), np.array([1 / 3, 2 / 3]))),
          (2, (np.array([1, 0, 0]), np.array([1, 0]))),
          (3, (np.array([1, 0, 0]), np.array([1, 0]))),
          (4, (np.array([0, 1 / 3,  2 / 3]), np.array([1 / 3, 2 / 3])))]:
            for eq, expected_eq in zip(lemke_howson(A, B, label), output):
                self.assertTrue(all(np.isclose(eq, expected_eq)))

        A = np.array([[1, -1], [-1, 1]])
        B = - A
        for label in range(4):
            for eq in lemke_howson(A, B, label):
                self.assertTrue(all(np.isclose(eq, np.array([1 / 2, 1 / 2]))),
                                msg=str(eq))
