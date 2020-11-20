import nashpy as nash
import numpy as np
from nashpy.learning.replicator_dynamics import get_derivative_of_fitness


def test_get_derivative_of_fitness():
    M = np.array([[3, 2, 3], [4, 1, 1], [2, 3, 1]])
    x_values = (
        np.array([1, 0, 0]),
        np.array([1 / 2, 1 / 2, 0]),
        np.array([0, 1 / 4, 3 / 4]),
    )
    derivative_values = (
        np.array([0, 0, 0]),
        np.array([0, 0, 0]),
        np.array([0.0, -0.09375, 0.09375]),
    )
    for x_value, expected_derivative in zip(x_values, derivative_values):
        derivative = get_derivative_of_fitness(x=x_value, t=0, A=M)
        assert np.array_equal(derivative, expected_derivative), x_value
