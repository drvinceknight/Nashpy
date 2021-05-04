"""
Tests for the game class
"""
import unittest

import numpy as np

from nashpy.algorithms.vertex_enumeration import vertex_enumeration


class TestVertexEnumeration(unittest.TestCase):
    """
    Tests for the vertex enumeration algorithm
    """

    def test_three_by_two_vertex_enumeration(self):
        A = np.array([[3, 3], [2, 5], [0, 6]])
        B = np.array([[3, 2], [2, 6], [3, 1]])

        expected_equilibria = sorted(
            [
                (np.array([1, 0, 0]), np.array([1, 0])),
                (np.array([0, 1 / 3, 2 / 3]), np.array([1 / 3, 2 / 3])),
                (np.array([4 / 5, 1 / 5, 0]), np.array([2 / 3, 1 / 3])),
            ],
            key=lambda a: list(np.round(a[0], 4)),
        )

        equilibria = sorted(
            vertex_enumeration(A, B), key=lambda a: list(np.round(a[0], 4))
        )
        for equilibrium, expected_equilibrium in zip(equilibria, expected_equilibria):
            for strategy, expected_strategy in zip(equilibrium, expected_equilibrium):
                self.assertTrue(all(np.isclose(strategy, expected_strategy)))

    def test_with_negative_utilities(self):
        A = np.array([[1, -1], [-1, 1]])
        B = -A

        expected_equilibrium = (np.array([0.5, 0.5]), np.array([0.5, 0.5]))
        equilibrium = next(vertex_enumeration(A, B))
        for strategy, expected_strategy in zip(equilibrium, expected_equilibrium):
            assert all(np.isclose(strategy, expected_strategy)), strategy
