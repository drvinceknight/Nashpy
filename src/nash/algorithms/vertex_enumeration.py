"""A class for the vertex enumeration algorithm"""
from nash.polytope import build_halfspaces, non_trivial_vertices

import numpy as np
from itertools import product

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
