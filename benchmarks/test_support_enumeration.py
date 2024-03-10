"""
Benchmarks for support enumeration
"""

import unittest

import numpy as np

from nashpy.algorithms.support_enumeration import support_enumeration


def test_support_enumeration_on_two_by_two_game(benchmark):
    A = np.array(((1, -1), (-1, 1)))
    eqs = support_enumeration(A, -A)
    benchmark(tuple, eqs)


def test_support_enumeration_on_three_by_three_game(benchmark):
    A = np.array(((0, 1, -1), (-1, 0, 1), (1, -1, 0)))
    eqs = support_enumeration(A, -A)
    benchmark(tuple, eqs)


def test_support_enumeration_on_four_by_four_game(benchmark):
    A = np.array(
        (
            (0, 1, -1, 1 / 4),
            (-1, 0, 1, 1 / 4),
            (1, -1, 0, 1 / 4),
            (1 / 4, 1 / 4, 1 / 4, 1 / 4),
        )
    )
    eqs = support_enumeration(A, -A)
    benchmark(tuple, eqs)
