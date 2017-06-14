"""
Tests for the game class
"""

import unittest
import nash
import numpy as np
from scipy.spatial import HalfspaceIntersection

from hypothesis import given
from hypothesis.extra.numpy import arrays
from hypothesis.strategies import integers

from types import GeneratorType

class TestGame(unittest.TestCase):
    """
    Tests for the game class
    """
    @given(A=arrays(np.int8, (4, 5)))
    def test_creation_of_halfspaces(self, A):
        """Test that can create a bi matrix game"""
        halfspace = nash.build_halfspaces(A)
        number_of_strategies, dimension = A.shape
        self.assertEqual(halfspace.shape,
                         (number_of_strategies + dimension, dimension + 1))
        self.assertTrue(np.array_equal(halfspace[number_of_strategies:,:-1],
                                       -np.eye(dimension)))

    def test_creation_of_particular_halfspaces(self):
        """Test that can create a given halfspace array representation"""
        A = np.array([[3, 3], [2, 5], [0, 6]])
        expected_halfspace = np.array([[ 3.,  3., -1.],
                                       [ 2.,  5., -1.],
                                       [ 0.,  6., -1.],
                                       [-1., -0.,  0.],
                                       [-0., -1.,  0.]])
        halfspace = nash.build_halfspaces(A)
        self.assertTrue(np.array_equal(halfspace, expected_halfspace))

        B = np.array([[3, 2], [2, 6], [3, 1]])
        expected_halfspace = np.array([[ 3.,  2.,  3., -1.],
                                       [ 2.,  6.,  1., -1.],
                                       [-1., -0., -0.,  0.],
                                       [-0., -1., -0.,  0.],
                                       [-0., -0., -1.,  0.]])
        halfspace = nash.build_halfspaces(B.transpose())
        self.assertTrue(np.array_equal(halfspace, expected_halfspace))

    @given(A=arrays(np.int8, (4, 5),
        elements=integers(0, 10)).filter(lambda a:np.min(a) != np.max(a)))
    def test_creation_of_feasible_point(self, A):
        halfspaces = nash.build_halfspaces(A)
        feasible_point = nash.find_feasible_point(halfspaces)
        M, b = halfspaces[:,:-1], halfspaces[:,-1]
        self.assertTrue(all(np.dot(M, feasible_point) <= -b))

    def test_creation_of_particular_feasible_point(self):
        A = np.array([[3, 3], [2, 5], [0, 6]])
        halfspaces = nash.build_halfspaces(A)
        feasible_point = nash.find_feasible_point(halfspaces)
        self.assertTrue(all(np.isclose(feasible_point,
                                       np.array([0.08074176, 0.08074176]))))

        B = np.array([[3, 2], [2, 6], [3, 1]])
        halfspaces = nash.build_halfspaces(B.transpose())
        feasible_point = nash.find_feasible_point(halfspaces)
        self.assertTrue(all(np.isclose(feasible_point,
                                       np.array([0.06492189,
                                                 0.06492189,
                                                 0.06492189]))))
    @given(A=arrays(np.int8, (4, 5),
        elements=integers(0, 10)).filter(lambda a:np.min(a) != np.max(a)))
    def test_creation_of_non_trivial_vertices(self, A):
        """Test that can create a bi matrix game"""
        halfspaces = nash.build_halfspaces(A)
        vertices_generator = nash.non_trivial_vertices(halfspaces)
        number_of_strategies, dimension = A.shape
        self.assertIsInstance(vertices_generator, GeneratorType)
        for vertex, labels in vertices_generator:
            self.assertEqual(len(vertex), dimension)
            for label in labels:
                self.assertGreaterEqual(label, 0)
                self.assertLessEqual(label, number_of_strategies + dimension)


    def test_creation_of_particular_non_trivial_vertices(self):
        """Test that vertices are obtained"""
        A = np.array([[3, 3], [2, 5], [0, 6]])
        halfspaces = nash.build_halfspaces(A)
        vertices_generator = nash.non_trivial_vertices(halfspaces)
        self.assertIsInstance(vertices_generator, GeneratorType)

        expected_vertices = sorted([np.array([1 / 3, 0]),
                                    np.array([0, 1 / 6]),
                                    np.array([2 / 9, 1 / 9]),
                                    np.array([1 / 12, 1 / 6])],
                                   key=lambda a:list(np.round(a, 5)))

        vertices = sorted((v for v, l in vertices_generator),
                          key=lambda a:list(np.round(a, 5)))

        for vertex, expected_vertex in zip(vertices, expected_vertices):
            self.assertTrue(all(np.isclose(vertex, expected_vertex)))

        B = np.array([[3, 2], [2, 6], [3, 1]])
        halfspaces = nash.build_halfspaces(B.transpose())
        vertices_generator = nash.non_trivial_vertices(halfspaces)
        self.assertIsInstance(vertices_generator, GeneratorType)

        expected_vertices = sorted([np.array([0, 0, 1 / 3]),
                                    np.array([0, 1 / 8, 1 / 4]),
                                    np.array([0, 1 / 6, 0]),
                                    np.array([2 / 7, 1 / 14, 0]),
                                    np.array([1 / 3, 0 , 0])],
                                   key=lambda a:list(np.round(a, 5)))

        vertices = sorted((v for v, l in vertices_generator),
                          key=lambda a:list(np.round(a, 5)))

        for vertex, expected_vertex in zip(vertices, expected_vertices):
            self.assertTrue(all(np.isclose(vertex, expected_vertex)),
                            msg="{} != {}".format(vertex, expected_vertex))


    def test_labelling_of_particular_vertices(self):
        A = np.array([[3, 3], [2, 5], [0, 6]])
        halfspaces = nash.build_halfspaces(A)
        vertices = nash.non_trivial_vertices(halfspaces)
        expected_labels = sorted([np.array([0, 1]), np.array([0, 4]),
                                  np.array([1, 2]), np.array([2, 3])],
                                 key=list)
        labels = sorted((nash.labels(v, halfspaces) for v, l in vertices),
                        key=list)
        for label, expected_label in zip(labels, expected_labels):
            self.assertTrue(np.array_equal(label, expected_label),
                            msg="{} != {}".format(label, expected_label))

        B = np.array([[3, 2], [2, 6], [3, 1]])
        halfspaces = nash.build_halfspaces(B.transpose())
        vertices = nash.non_trivial_vertices(halfspaces)
        expected_labels = sorted([np.array([0, 2, 3]), np.array([0, 3, 4]),
                                  np.array([0, 1, 2]), np.array([1, 2, 4]),
                                  np.array([0, 1, 4])],
                                 key=list)

        labels = sorted((nash.labels(v, halfspaces) for v, l in vertices),
                        key=list)
        for label, expected_label in zip(labels, expected_labels):
            self.assertTrue(np.array_equal(label, expected_label),
                            msg="{} != {}".format(label, expected_label))

    def test_particular_vertex_enumeration(self):
        A = np.array([[3, 3], [2, 5], [0, 6]])
        B = np.array([[3, 2], [2, 6], [3, 1]])

        expected_equilibria = sorted([(np.array([1, 0, 0]), np.array([1,  0])),
                                      (np.array([0, 1 / 3, 2 / 3]),
                                       np.array([1 / 3, 2 / 3])),
                                      (np.array([4 / 5, 1 / 5, 0]),
                                       np.array([2 / 3, 1 / 3]))],
                                      key=lambda a: list(np.round(a[0], 4)))

        equilibria = sorted(nash.vertex_enumeration(A, B),
                            key=lambda a: list(np.round(a[0], 4)))
        for equilibrium, expected_equilibrium in zip(equilibria,
                                                     expected_equilibria):
            for strategy, expected_strategy in zip(equilibrium,
                                                   expected_equilibrium):
                self.assertTrue(all(np.isclose(strategy, expected_strategy)),
                                msg="{} != {}".format(strategy,
                                    expected_strategy))
