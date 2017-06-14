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

def vertex_enumeration(A, B):

    if np.min(A) < 0:
        A = A + abs(np.min(A))
    if np.min(B) < 0:
        B = B + abs(np.min(B))

    number_of_row_strategies, row_dimension = A.shape
    max_label = number_of_row_strategies + row_dimension
    full_labels = set(range(max_label))

    row_halfspaces = build_halfspaces(B.transpose())
    col_halfspaces = build_halfspaces(A)

    row_vertices = non_trivial_vertices(row_halfspaces)
    col_vertices = non_trivial_vertices(col_halfspaces)
    for (row_v, row_l), (col_v, col_l)  in product(row_vertices, col_vertices):
        row_l = (row_l + number_of_row_strategies) % (max_label)
        if set(np.append(row_l, col_l)) == full_labels:
            yield row_v / sum(row_v), col_v / sum(col_v)
