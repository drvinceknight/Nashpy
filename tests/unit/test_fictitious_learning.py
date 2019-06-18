"""
Tests for fictitious learning
"""
import numpy as np
from hypothesis import given
from hypothesis.extra.numpy import arrays
from hypothesis.strategies import integers

import nashpy as nash
from nashpy.learning.fictitious_learning import (
    get_best_response_to_belief,
)



@given(M=arrays(np.int8, (4, 5)))
def test_find_best_response_to_belief(M):
    belief = np.zeros(M.shape[1])
    best_response = get_best_response_to_belief(M, belief)
    assert best_response >= 0
    assert best_response <= M.shape[1] - 1
    assert type(best_response) is np.int64
