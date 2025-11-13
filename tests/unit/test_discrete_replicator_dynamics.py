"""
tests for discrete replicator dynamics
"""

import numpy as np

from nashpy.learning.discrete_replicator_dynamics import (
    discrete_replicator_dynamics,
    type_1_discrete_step,
    type_2_discrete_step,
    greenwood_quantize,
)
from hypothesis import given
from hypothesis.extra.numpy import arrays
from hypothesis.strategies import floats


def test_type_2_discrete_step_size_2():

    x = np.array((0.2, 0.8))
    A = np.array(
        (
            (4, 3),
            (2, 5),
        )
    )
    expected_next_x = np.array((2 / 13, 11 / 13))
    next_x = type_2_discrete_step(
        x=x,
        A=A,
    )
    assert np.allclose(expected_next_x, next_x)


def test_type_2_discrete_step_size_3():
    x = np.array((0.2, 0.3, 0.5))
    A = np.array(
        (
            (4, 3, 1),
            (2, 5, 2),
            (6, 5, 3),
        )
    )
    expected_next_x = np.array((0.12903226, 0.25513196, 0.61583578))
    next_x = type_2_discrete_step(
        x=x,
        A=A,
    )
    assert np.allclose(expected_next_x, next_x)


def test_type_2_discrete_step_size_4():
    x = np.array((0.2, 0.3, 0.2, 0.3))
    A = np.array(((4, 3, 1, 5), (2, 5, 2, 2), (6, 5, 3, 9), (2, 2, 1, 5)))
    expected_next_x = np.array((0.19101124, 0.24438202, 0.33707865, 0.22752809))
    next_x = type_2_discrete_step(
        x=x,
        A=A,
    )
    assert np.allclose(expected_next_x, next_x)


def test_type_1_discrete_step_size_2():

    x = np.array((0.2, 0.8))
    A = np.array(
        (
            (4, 3),
            (2, 5),
        )
    )
    expected_next_x = np.array((1 / 125, 124 / 125))
    next_x = type_1_discrete_step(
        x=x,
        A=A,
    )
    assert np.allclose(expected_next_x, next_x)


def test_type_1_discrete_step_size_3():
    x = np.array((0.2, 0.3, 0.5))
    A = np.array(
        (
            (4, 3, 1),
            (2, 5, 2),
            (6, 5, 3),
        )
    )
    expected_next_x = np.array((-0.042, 0.147, 0.895))
    next_x = type_1_discrete_step(
        x=x,
        A=A,
    )
    assert np.allclose(expected_next_x, next_x)


def test_type_1_discrete_step_size_4():
    x = np.array((0.2, 0.3, 0.2, 0.3))
    A = np.array(((4, 3, 1, 5), (2, 5, 2, 2), (6, 5, 3, 9), (2, 2, 1, 5)))
    expected_next_x = np.array((0.168, 0.102, 0.688, 0.042))
    next_x = type_1_discrete_step(
        x=x,
        A=A,
    )
    assert np.allclose(expected_next_x, next_x)


@given(
    k=arrays(
        np.float32,
        shape=100,
        elements=floats(
            min_value=0, max_value=1000, allow_infinity=False, allow_nan=False
        ),
    )
)
def test_greenwood_quantize_sum_consistent(k):

    N = np.round(np.sum(k) + 0.5, 0)
    assert np.sum(greenwood_quantize(k, N)) == N


@given(
    k=arrays(
        np.float32,
        shape=100,
        elements=floats(
            min_value=0, max_value=1000, allow_infinity=False, allow_nan=False
        ),
    )
)
def test_greenwood_quantize(k):

    N = np.round(np.sum(k) + 0.5, 0)
    k[-1] = k[-1] + (N - (np.sum(k) + 0.5))

    greenwoods_output = greenwood_quantize(k, N)
    assert all(item.is_integer() for item in greenwoods_output)


def test_greenwood_d_less_than_zero():

    k = np.array([0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2])
    N = 2
    assert np.array_equal(
        np.sort(greenwood_quantize(k, N), axis=None),
        np.array([0, 0, 0, 0, 0, 0, 0, 0, 1, 1]),
    )


def test_greenwood_d_greater_than_zero():

    k = np.array([0.8, 0.8, 0.8, 0.8, 0.8, 0.8, 0.8, 0.8, 0.8, 0.8])
    N = 8
    assert np.array_equal(
        np.sort(greenwood_quantize(k, N), axis=None),
        np.array([0, 0, 1, 1, 1, 1, 1, 1, 1, 1]),
    )


def test_discrete_replicator_dynamics_1_generation():

    x = np.array((20, 80))
    A = np.array(
        (
            (4, 3),
            (2, 5),
        )
    )
    expected_next_x = np.array([15, 85])
    next_x = discrete_replicator_dynamics(
        A=A,
        x=x,
        steps=1,
        quantize=True,
    )
    assert np.allclose(expected_next_x, next_x)


def test_discrete_replicator_dynamics_20_generations_size_2():
    x = np.array((500, 500))
    A = np.array(
        (
            (60, 10),
            (26, 43),
        )
    )
    expected_next_x = np.array(
        [
            [5.03597122e02, 4.96402878e02],
            [5.08918337e02, 4.91081663e02],
            [5.16776225e02, 4.83223775e02],
            [5.28345350e02, 4.71654650e02],
            [5.45288671e02, 4.54711329e02],
            [5.69865276e02, 4.30134724e02],
            [6.04884250e02, 3.95115750e02],
            [6.53153699e02, 3.46846301e02],
            [7.15784304e02, 2.84215696e02],
            [7.89040538e02, 2.10959462e02],
            [8.62100057e02, 1.37899943e02],
            [9.21339553e02, 7.86604473e01],
            [9.60035771e02, 3.99642286e01],
            [9.81211964e02, 1.87880365e01],
            [9.91539295e02, 8.46070548e00],
            [9.96269523e02, 3.73047697e00],
            [9.98371035e02, 1.62896525e00],
            [9.99291750e02, 7.08249874e-01],
            [9.99692645e02, 3.07354990e-01],
            [9.99866729e02, 1.33271260e-01],
        ]
    )
    next_x = discrete_replicator_dynamics(
        A=A,
        x=x,
        steps=20,
        quantize=False,
    )
    assert np.allclose(expected_next_x, next_x)


def test_discrete_replicator_dynamics_20_generations_size_2_quantized():
    x = np.array((500, 500))
    A = np.array(
        (
            (60, 10),
            (26, 43),
        )
    )
    expected_next_x = np.array(
        [
            [504.0, 496.0],
            [510.0, 490.0],
            [518.0, 482.0],
            [530.0, 470.0],
            [548.0, 452.0],
            [574.0, 426.0],
            [611.0, 389.0],
            [661.0, 339.0],
            [725.0, 275.0],
            [799.0, 201.0],
            [871.0, 129.0],
            [928.0, 72.0],
            [964.0, 36.0],
            [983.0, 17.0],
            [992.0, 8.0],
            [996.0, 4.0],
            [998.0, 2.0],
            [999.0, 1.0],
            [1000.0, 0.0],
            [1000.0, 0.0],
        ]
    )
    next_x = discrete_replicator_dynamics(
        A=A,
        x=x,
        steps=20,
        quantize=True,
    )
    assert np.allclose(expected_next_x, next_x)
