"""A class for the vertex enumeration algorithm"""
from nash.polytope import build_halfspaces, non_trivial_vertices

import numpy as np
from itertools import product

def vertex_enumeration(A, B):
    """
    Obtain the Nash equilibria using enumeration of the vertices of the best
    response polytopes.

    Algorithm implemented here is Algorithm 3.5 of Nisan, Noam, et al., eds.
    Algorithmic game theory. Cambridge University Press, 2007.

    1. Build best responses polytopes of both players
    2. For each vertex pair of both polytopes
    3. Check if pair is fully labelled
    4. Return the normalised pair

    Returns
    -------

        A generator.
    """

    if np.min(A) < 0:
        A = A + abs(np.min(A))
    if np.min(B) < 0:
        B = B + abs(np.min(B))

    number_of_row_strategies, row_dimension = A.shape
    max_label = number_of_row_strategies + row_dimension
    full_labels = set(range(max_label))

    row_halfspaces = build_halfspaces(B.transpose())
    col_halfspaces = build_halfspaces(A)

    for row_v, row_l in non_trivial_vertices(row_halfspaces):
        adjusted_row_l = set((label + number_of_row_strategies) % (max_label)
                             for label in row_l)

        for col_v, col_l in non_trivial_vertices(col_halfspaces):
            if adjusted_row_l.union(col_l) == full_labels:
                yield row_v / sum(row_v), col_v / sum(col_v)
