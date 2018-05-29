"""A class for a normal form game"""
import numpy as np
from scipy.spatial import HalfspaceIntersection
from scipy.optimize import linprog
from itertools import product


def build_halfspaces(M):
    """
    Build a matrix representation for a halfspace corresponding to:

        Mx <= 1 and x >= 0

    This is of the form:

       [M: -1]
       [-1: 0]

    As specified in
    https://docs.scipy.org/doc/scipy-0.19.0/reference/generated/scipy.spatial.HalfspaceIntersection.html

    Parameters
    ----------

        M: a numpy array

    Returns:
    --------

        Numpy array
    """
    number_of_strategies, dimension = M.shape
    b = np.append(-np.ones(number_of_strategies), np.zeros(dimension))
    M = np.append(M, - np.eye(dimension), axis=0)
    halfspaces = np.column_stack((M, b.transpose()))
    return halfspaces

def find_feasible_point(halfspaces):
    """
    Use linear programming to find a point inside the halfspaces (needed to
    define it).

    Code taken from scipy documentation:
    https://docs.scipy.org/doc/scipy-0.19.0/reference/generated/scipy.spatial.HalfspaceIntersection.html

    Parameters
    ----------

        halfspaces: a matrix representation of halfspaces

    Returns:
    --------

        numpy array
    """
    norm_vector = np.reshape(np.linalg.norm(halfspaces[:, :-1], axis=1),
                             (halfspaces.shape[0], 1))
    c = np.zeros((halfspaces.shape[1],))
    c[-1] = -1
    A = np.hstack((halfspaces[:, :-1], norm_vector))
    b = - halfspaces[:, -1:]
    res = linprog(c, A_ub=A, b_ub=b)
    return res.x[:-1]

def labels(vertex, halfspaces):
    """
    Return the labels of the facets on which lie a given vertex. This is
    calculated by carrying out the matrix multiplictation.

    Parameters
    ----------

        vertex: a numpy array
        halfspaces: a numpy array

    Returns
    -------

       set
    """
    b = halfspaces[:,-1]
    M = halfspaces[:,:-1]
    return set(np.where(np.isclose(np.dot(M, vertex), -b))[0])

def non_trivial_vertices(halfspaces):
    """
    Returns all vertex, label pairs (ignoring the origin).

    Parameters:

        halfspaces: a numpy array

    Returns:

        generator
    """
    feasible_point = find_feasible_point(halfspaces)
    hs = HalfspaceIntersection(halfspaces, feasible_point)
    hs.close()
    return ((v, labels(v, halfspaces)) for v in hs.intersections if max(v) > 0)
