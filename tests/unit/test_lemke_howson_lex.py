import unittest
import warnings

import numpy as np

# from deprecated import DeprecationWarning

from nashpy.algorithms.lemke_howson_lex import lemke_howson_lex


class TestLemkeHowsonLex(unittest.TestCase):
    """
    Consice test example to keep coverage up
    """

    def test_deprecated_lex(self):
        A = np.array([[-1, -1, -1], [0, 0, 0], [-1, -1, -10000]])
        B = np.array([[-1, -1, -1], [0, 0, 0], [-1, -1, -10000]])
        with warnings.catch_warnings(record=True) as w:
            eqs = lemke_howson_lex(A, B, initial_dropped_label=0)
            self.assertAlmostEqual(eqs[0].dot(A).dot(eqs[1].transpose()), 0)
            self.assertAlmostEqual(eqs[0].dot(B).dot(eqs[1].transpose()), 0)
            self.assertGreater(len(w), 0)
            self.assertEqual(w[0].category, DeprecationWarning)
