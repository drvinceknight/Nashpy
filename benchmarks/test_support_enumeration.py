"""
Benchmarks for support enumeration
"""

import unittest

import numpy as np

from nashpy.algorithms.support_enumeration import support_enumeration


def test_support_enumeration_on_two_by_two_game(benchmark):
    A = np.array(((1, -1), (-1, 1)))
    benchmark(lambda: tuple(support_enumeration(A, -A)))


def test_support_enumeration_on_three_by_three_game(benchmark):
    A = np.array(((0, 1, -1), (-1, 0, 1), (1, -1, 0)))
    benchmark(lambda: tuple(support_enumeration(A, -A)))


def test_support_enumeration_on_four_by_four_game(benchmark):
    A = np.array(
        (
            (0, 1, -1, 1 / 4),
            (-1, 0, 1, 1 / 4),
            (1, -1, 0, 1 / 4),
            (1 / 4, 1 / 4, 1 / 4, 1 / 4),
        )
    )
    benchmark(lambda: tuple(support_enumeration(A, -A)))


def test_support_enumeration_on_five_by_five_game(benchmark):
    A = np.array(
        (
            (0, 1, -1, 1 / 4, 1 / 4),
            (-1, 0, 1, 1 / 4, 1 / 4),
            (1, -1, 0, 1 / 4, 1 / 4),
            (1 / 4, 1 / 4, 1 / 4, 1 / 4, 1 / 4),
            (1 / 4, 1 / 4, 1 / 4, 1 / 4, 1 / 4),
        )
    )
    benchmark(lambda: tuple(support_enumeration(A, -A)))


def test_support_enumeration_on_six_by_six_game(benchmark):
    A = np.array(
        (
            (0, 1, -1, 1 / 4, 1 / 4, 1 / 4),
            (-1, 0, 1, 1 / 4, 1 / 4, 1 / 4),
            (1, -1, 0, 1 / 4, 1 / 4, 1 / 4),
            (1 / 4, 1 / 4, 1 / 4, 1 / 4, 1 / 4, 1 / 4),
            (1 / 4, 1 / 4, 1 / 4, 1 / 4, 1 / 4, 1 / 4),
            (1 / 4, 1 / 4, 1 / 4, 1 / 4, 1 / 4, 1 / 4),
        )
    )
    benchmark(lambda: tuple(support_enumeration(A, -A)))


def test_support_enumeration_on_seven_by_seven_game(benchmark):
    A = np.array(
        (
            (0, 1, -1, 1 / 4, 1 / 4, 1 / 4, 1 / 4),
            (-1, 0, 1, 1 / 4, 1 / 4, 1 / 4, 1 / 4),
            (1, -1, 0, 1 / 4, 1 / 4, 1 / 4, 1 / 4),
            (1 / 4, 1 / 4, 1 / 4, 1 / 4, 1 / 4, 1 / 4, 1 / 4),
            (1 / 4, 1 / 4, 1 / 4, 1 / 4, 1 / 4, 1 / 4, 1 / 4),
            (1 / 4, 1 / 4, 1 / 4, 1 / 4, 1 / 4, 1 / 4, 1 / 4),
            (1 / 4, 1 / 4, 1 / 4, 1 / 4, 1 / 4, 1 / 4, 1 / 4),
        )
    )
    benchmark(lambda: tuple(support_enumeration(A, -A)))
