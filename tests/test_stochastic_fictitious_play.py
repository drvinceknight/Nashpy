"""
Tests for stochastic fictitious learning
"""
import types

import numpy as np
from hypothesis import given
from hypothesis.extra.numpy import arrays
from hypothesis.strategies import integers

import nashpy as nash
from nashpy.learning.stochastic_fictitious_play import (
    get_distribution_response_to_play_count,
)


def test_first():
    x = 4 + 5
    assert x == 9


@given(M=arrays(np.int8, (2, 2)))
def test_property_get_distribution_response_to_play_count(M):
    play_count = np.zeros(M.shape[1])
    distribution_response = get_distribution_response_to_play_count(M, play_count)
    assert len(distribution_response) == len(play_count)
    assert np.all(distribution_response) >= 0
    # assert distribution_response <= M.shape[1] - 1
