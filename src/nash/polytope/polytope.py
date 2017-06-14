"""A class for a normal form game"""
import numpy as np
from scipy.spatial import HalfspaceIntersection
from scipy.optimize import linprog
from itertools import product


def build_halfspaces(M):
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
    b = halfspaces[:,-1]
    M = halfspaces[:,:-1]
    return np.where(np.isclose(np.dot(M, vertex), -b))[0]

def non_trivial_vertices(halfspaces):
    feasible_point = find_feasible_point(halfspaces)
    hs = HalfspaceIntersection(halfspaces, feasible_point)
    hs.close()
    return ((v, labels(v, halfspaces)) for v in hs.intersections if max(v) > 0)
