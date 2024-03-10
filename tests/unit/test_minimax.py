"""
Tests for the linear programming implementation for Zero sum games
"""

import numpy as np

from nashpy.linalg.minimax import (
    get_A_eq,
    get_A_ub,
    get_b_ub,
    get_bounds,
    get_c,
    linear_program,
)


def test_get_c():
    for number_of_rows in range(2, 10):
        c = get_c(number_of_rows=number_of_rows)
        assert c.shape == (number_of_rows + 1,)
        assert np.array_equal(c[:-1], np.zeros(shape=number_of_rows))
        assert c[-1] == -1


def test_get_c_for_matching_pennies():
    """
    This is an explicit test for the exercise in the docs.
    """
    c = get_c(number_of_rows=2)
    assert np.array_equal(c, np.array((0, 0, -1)))


def test_get_c_for_modified_rock_paper_scissors():
    """
    This is an explicit test for the example in the docs.
    """
    c = get_c(number_of_rows=4)
    assert np.array_equal(c, np.array((0, 0, 0, 0, -1)))


def test_get_A_ub():
    M = np.array([[-2, -3, 2], [3, -4, -1], [3, -1, -1]])
    expected_A_ub = np.array(
        [[2.0, -3.0, -3.0, 1.0], [3.0, 4.0, 1.0, 1.0], [-2.0, 1.0, 1.0, 1.0]]
    )
    A_ub = get_A_ub(row_player_payoff_matrix=M)
    assert np.array_equal(a1=expected_A_ub, a2=A_ub)


def test_get_A_ub_for_matching_pennies():
    """
    This is an explicit test for the exercise in the docs.
    """
    M = np.array([[1, -1], [-1, 1]])
    A_ub = get_A_ub(row_player_payoff_matrix=M)
    expected_A_ub = np.array([[-1.0, 1.0, 1.0], [1.0, -1.0, 1.0]])
    assert np.array_equal(A_ub, expected_A_ub)


def test_get_A_ub_for_modified_rock_paper_scissors():
    """
    This is an explicit test for the example in the docs.
    """
    M = np.array([[0, -1, 1], [1, 0, -1], [-1, 1, 0], [1, -1, 1]])
    A_ub = get_A_ub(row_player_payoff_matrix=M)
    expected_A_ub = np.array(
        [
            [0.0, -1.0, 1.0, -1.0, 1.0],
            [1.0, 0.0, -1.0, 1.0, 1.0],
            [-1.0, 1.0, 0.0, -1.0, 1.0],
        ]
    )
    assert np.array_equal(A_ub, expected_A_ub)


def test_get_b_ub():
    for number_of_columns in range(2, 10):
        b_ub = get_b_ub(number_of_columns=number_of_columns)
        assert np.array_equal(b_ub, np.zeros(shape=(number_of_columns, 1)))


def test_get_b_ub_for_matching_pennies():
    """
    This is an explicit test for the exercise in the docs.
    """
    b_ub = get_b_ub(number_of_columns=2)
    expected_b_ub = np.array([[0.0], [0.0]])
    assert np.array_equal(b_ub, expected_b_ub)


def test_get_b_ub_for_modified_rock_paper_scissors():
    """
    This is an explicit test for the example in the docs.
    """
    b_ub = get_b_ub(number_of_columns=3)
    expected_b_ub = np.array([[0.0], [0.0], [0.0]])
    assert np.array_equal(b_ub, expected_b_ub)


def test_get_A_eq_for_matching_pennies():
    """
    This is an explicit test for the exercise in the docs.
    """
    A_eq = get_A_eq(number_of_rows=2)
    expected_A_eq = np.array([[1, 1, 0]])
    assert np.array_equal(A_eq, expected_A_eq)


def test_get_A_eq_for_modified_rock_paper_scissors():
    """
    This is an explicit test for the example in the docs.
    """
    A_eq = get_A_eq(number_of_rows=4)
    expected_A_eq = np.array([[1, 1, 1, 1, 0]])
    assert np.array_equal(A_eq, expected_A_eq)


def test_get_A_eq():
    for number_of_rows in range(2, 10):
        A_eq = get_A_eq(number_of_rows=number_of_rows)
        assert A_eq.shape == (1, number_of_rows + 1)
        assert np.array_equal(A_eq[0][:-1], np.ones(shape=number_of_rows))
        assert A_eq[0, -1] == 0


def test_get_bounds():
    for number_of_rows in range(2, 10):
        bounds = get_bounds(number_of_rows)
        assert bounds == [(0, None) for _ in range(number_of_rows)] + [(None, None)]


def test_linear_program_for_matrix_in_docs_for_row_player():
    M = np.array(
        [
            [0, 1, -1],
            [-1, 0, 1],
            [1, -1, 0],
            [1, -1, 1],
        ]
    )
    x = linear_program(row_player_payoff_matrix=M)
    expected_x = np.array([0.44444444, 0.22222222, 0.0, 0.33333333])
    assert np.allclose(x, expected_x)


def test_linear_program_for_matrix_in_docs_for_column_player():
    M = np.array(
        [
            [0, 1, -1],
            [-1, 0, 1],
            [1, -1, 0],
            [1, -1, 1],
        ]
    )
    x = linear_program(row_player_payoff_matrix=-M.T)
    expected_x = np.array([0.22222222, 0.44444444, 0.33333333])
    assert np.allclose(x, expected_x)
