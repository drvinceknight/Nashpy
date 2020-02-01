import sys, os

sys.path.append(os.path.join(os.path.dirname(__file__), "..", "src"))
from nashpy import *

import numpy as np

"""
Demo for lemke_howson_lex vs lemke_howson
-----------------------------------------

Demonstrates an additional game that lemke_howson_lex can solve 
as well as a game it cannot solve. (which normal lemke_howson also 
cannot solve)

All payoff matrices and games are in test_variables.py
"""


def strategies_match(A, B):
    return np.array_equal(A[0], B[0]) and np.array_equal(A[1], B[1])


def test(A, B, test_name, answer):
    print("\n+++++++++++++++", test_name, "++++++++++++++++")
    lemke_howson_answer = lemke_howson(A, B)
    lemke_howson_lex_answer = lemke_howson_lex(A, B)
    print(
        "LEMKE_HOWSON PASSED: ", strategies_match(lemke_howson_answer, answer)
    )
    print("LEMKE_HOWSON RESULT: ", lemke_howson_answer)
    print(
        "LEMKE_HOWSON_LEX PASSED: ",
        strategies_match(lemke_howson_lex_answer, answer),
    )
    print("LEMKE_HOWSON_LEX RESULT: ", lemke_howson_lex_answer)
    return strategies_match(lemke_howson_lex_answer, answer)


"""
Normal game solvable by both
----------------------------
"""
prisoner_A = np.array([[3, 0], [5, 1]])
prisoner_B = np.array([[3, 5], [0, 1]])
prisoner_test_1 = (
    prisoner_A,
    prisoner_B,
    "prisoner_test_1",
    (np.array([0, 1]), np.array([0, 1])),
)

test(*prisoner_test_1)

"""
Degenerate game solvable by lemke_howson_lex but not lemke_howson
-----------------------------------------------------------------
"""

degen_A_3 = np.array([[1, 3, 3], [3, 1, 3], [1, 3, 3]])
degen_B_3 = np.array([[3, 3, 1], [1, 1, 3], [3, 1, 3]])
degen_test_3 = (
    degen_A_3,
    degen_B_3,
    "degen_test_3",
    (np.array([0.5, 0.5, 0]), np.array([0, 0, 1])),
)

test(*degen_test_3)


"""
Degenerate game not solveable by both (Don't understand why)
-------------------------------------

prisoner_degen_B = np.array([[3, 3], [1, 1]])
prisoner_degen_test_1 = (
    prisoner_A,
    prisoner_degen_B,
    "prisoner_degen_test_1",
    (np.array([0, 1]), np.array([1, 0])),
)
"""

# test(*prisoner_degen_test_1)
