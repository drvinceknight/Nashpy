"""
Tests for the linear programming implementation for Zero sum games
"""
import types

import numpy as np
from hypothesis import given
from hypothesis.extra.numpy import arrays
from hypothesis.strategies import integers

from nashpy.linalg.minimax import (
    get_c,
    get_b_ub,
    get_A_ub,
    get_A_eq,
)


@given(number_of_rows=integers(min_value=1))
def test_property_get_c(number_of_rows):
    c = get_c(number_of_rows=number_of_rows)
    assert c.shape == (number_of_rows + 1,)
    assert np.array_equal(c[:-1], np.ones(shape=number_of_rows))
    assert c[-1] == 0


def test_get_A_ub():
    M = np.array([[-2, -3, 2], [3, -4, -1], [3, -1, -1]])
    expected_A_ub = np.array(
        [[2.0, -3.0, -3.0, 1.0], [3.0, 4.0, 1.0, 1.0], [-2.0, 1.0, 1.0, 1.0]]
    )
    A_ub = get_A_ub(row_player_payoff_matrix=M)
    assert np.array_equal(a1=expected_A_ub, a2=A_ub)


@given(number_of_columns=integers(min_value=1))
def test_property_get_b_ub(number_of_columns):
    b_ub = get_b_ub(number_of_columns=number_of_columns)
    assert np.array_equal(b_ub, np.zeros(shape=(number_of_columns, 1)))


@given(number_of_rows=integers(min_value=1))
def test_property_get_A_eq(number_of_rows):
    A_eq = get_A_eq(number_of_rows=number_of_rows)
    assert A_eq.shape == (1, number_of_rows + 1)
    assert np.array_equal(A_eq[:-1], np.ones(shape=(1, number_of_rows)))
    assert A_eq[0, -1] == 0
