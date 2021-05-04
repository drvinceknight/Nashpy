"""
Tests for the polytope functionality
"""
import unittest
from types import GeneratorType

import numpy as np
from hypothesis import given
from hypothesis.extra.numpy import arrays
from hypothesis.strategies import integers

from nashpy.polytope.polytope import (
    build_halfspaces,
    find_feasible_point,
    labels,
    non_trivial_vertices,
)


class TestPolytope(unittest.TestCase):
    """
    Tests for the functions for polytopes
    """

    @given(A=arrays(np.int8, (4, 5)))
    def test_creation_of_halfspaces(self, A):
        """Test that can create a bi matrix game"""
        halfspace = build_halfspaces(A)
        number_of_strategies, dimension = A.shape
        self.assertEqual(
            halfspace.shape, (number_of_strategies + dimension, dimension + 1)
        )
        self.assertTrue(
            np.array_equal(halfspace[number_of_strategies:, :-1], -np.eye(dimension))
        )

    def test_creation_of_particular_halfspaces(self):
        """Test that can create a given halfspace array representation"""
        A = np.array([[3, 3], [2, 5], [0, 6]])
        expected_halfspace = np.array(
            [
                [3.0, 3.0, -1.0],
                [2.0, 5.0, -1.0],
                [0.0, 6.0, -1.0],
                [-1.0, -0.0, 0.0],
                [-0.0, -1.0, 0.0],
            ]
        )
        halfspace = build_halfspaces(A)
        self.assertTrue(np.array_equal(halfspace, expected_halfspace))

        B = np.array([[3, 2], [2, 6], [3, 1]])
        expected_halfspace = np.array(
            [
                [3.0, 2.0, 3.0, -1.0],
                [2.0, 6.0, 1.0, -1.0],
                [-1.0, -0.0, -0.0, 0.0],
                [-0.0, -1.0, -0.0, 0.0],
                [-0.0, -0.0, -1.0, 0.0],
            ]
        )
        halfspace = build_halfspaces(B.transpose())
        self.assertTrue(np.array_equal(halfspace, expected_halfspace))

    @given(
        A=arrays(np.int8, (4, 5), elements=integers(0, 10)).filter(
            lambda a: np.min(a) != np.max(a)
        )
    )
    def test_creation_of_feasible_point(self, A):
        halfspaces = build_halfspaces(A)
        feasible_point = find_feasible_point(halfspaces)
        M, b = halfspaces[:, :-1], halfspaces[:, -1]
        self.assertTrue(all(np.dot(M, feasible_point) <= -b))

    def test_creation_of_particular_feasible_point(self):
        A = np.array([[3, 3], [2, 5], [0, 6]])
        halfspaces = build_halfspaces(A)
        feasible_point = find_feasible_point(halfspaces)
        self.assertTrue(
            all(np.isclose(feasible_point, np.array([0.08074176, 0.08074176])))
        )

        B = np.array([[3, 2], [2, 6], [3, 1]])
        halfspaces = build_halfspaces(B.transpose())
        feasible_point = find_feasible_point(halfspaces)
        self.assertTrue(
            all(
                np.isclose(
                    feasible_point,
                    np.array([0.06492189, 0.06492189, 0.06492189]),
                )
            )
        )

    @given(
        A=arrays(np.int8, (4, 5), elements=integers(0, 10)).filter(
            lambda a: np.min(a) != np.max(a)
        )
    )
    def test_creation_of_non_trivial_vertices(self, A):
        """Test that can create a bi matrix game"""
        halfspaces = build_halfspaces(A)
        vertices_generator = non_trivial_vertices(halfspaces)
        number_of_strategies, dimension = A.shape
        self.assertIsInstance(vertices_generator, GeneratorType)
        for vertex, labels_set in vertices_generator:
            self.assertEqual(len(vertex), dimension)
            for label in labels_set:
                self.assertGreaterEqual(label, 0)
                self.assertLessEqual(label, number_of_strategies + dimension)

    def test_creation_of_particular_non_trivial_vertices(self):
        """Test that vertices are obtained"""
        A = np.array([[3, 3], [2, 5], [0, 6]])
        halfspaces = build_halfspaces(A)
        vertices_generator = non_trivial_vertices(halfspaces)
        self.assertIsInstance(vertices_generator, GeneratorType)

        expected_vertices = sorted(
            [
                np.array([1 / 3, 0]),
                np.array([0, 1 / 6]),
                np.array([2 / 9, 1 / 9]),
                np.array([1 / 12, 1 / 6]),
            ],
            key=lambda a: list(np.round(a, 5)),
        )

        vertices = sorted(
            (v for v, l in vertices_generator),
            key=lambda a: list(np.round(a, 5)),
        )

        for vertex, expected_vertex in zip(vertices, expected_vertices):
            self.assertTrue(all(np.isclose(vertex, expected_vertex)))

        B = np.array([[3, 2], [2, 6], [3, 1]])
        halfspaces = build_halfspaces(B.transpose())
        vertices_generator = non_trivial_vertices(halfspaces)
        self.assertIsInstance(vertices_generator, GeneratorType)

        expected_vertices = sorted(
            [
                np.array([0, 0, 1 / 3]),
                np.array([0, 1 / 8, 1 / 4]),
                np.array([0, 1 / 6, 0]),
                np.array([2 / 7, 1 / 14, 0]),
                np.array([1 / 3, 0, 0]),
            ],
            key=lambda a: list(np.round(a, 5)),
        )

        vertices = sorted(
            (v for v, l in vertices_generator),
            key=lambda a: list(np.round(a, 5)),
        )

        for vertex, expected_vertex in zip(vertices, expected_vertices):
            self.assertTrue(
                all(np.isclose(vertex, expected_vertex)),
                msg="{} != {}".format(vertex, expected_vertex),
            )

    def test_labelling_of_particular_vertices(self):
        A = np.array([[3, 3], [2, 5], [0, 6]])
        halfspaces = build_halfspaces(A)
        vertices = non_trivial_vertices(halfspaces)
        expected_labels = sorted(
            [set([0, 1]), set([0, 4]), set([1, 2]), set([2, 3])], key=list
        )
        labels_ = sorted((labels(v, halfspaces) for v, l in vertices), key=list)
        for label, expected_label in zip(labels_, expected_labels):
            self.assertTrue(
                np.array_equal(label, expected_label),
                msg="{} != {}".format(label, expected_label),
            )

        B = np.array([[3, 2], [2, 6], [3, 1]])
        halfspaces = build_halfspaces(B.transpose())
        vertices = non_trivial_vertices(halfspaces)
        expected_labels = sorted(
            [
                set([0, 2, 3]),
                set([0, 3, 4]),
                set([0, 1, 2]),
                set([1, 2, 4]),
                set([0, 1, 4]),
            ],
            key=list,
        )

        labels_ = sorted((labels(v, halfspaces) for v, l in vertices), key=list)
        for label, expected_label in zip(labels_, expected_labels):
            self.assertTrue(
                np.array_equal(label, expected_label),
                msg="{} != {}".format(label, expected_label),
            )
