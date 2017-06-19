"""A class for the Lemke Howson algorithm"""
from nash.integer_pivoting import (make_tableau, non_basic_variables,
                                   pivot_tableau)

import numpy as np
from itertools import cycle


def shift_tableau(tableau, shape):
    """
    Shift a tableau to ensure labels of pairs of tableaux coincide
    """
    return np.append(np.roll(tableau[:,:-1], shape[0], axis=1),
                     np.ones((shape[0], 1)), axis=1)

def tableau_to_strategy(tableau, basic_labels, strategy_labels):
    """
    Return a strategy vector from a tableau
    """
    vertex = []
    for column in strategy_labels:
        if column in basic_labels:
            for i, row in enumerate(tableau[:, column]):
                if row != 0:
                    vertex.append(tableau[i, -1] / row)
        else:
            vertex.append(0)
    strategy = np.array(vertex)
    return strategy / sum(strategy)

def lemke_howson(A, B, initial_dropped_label=0):
    """
    Carry out the lemke howson algorithm for a given initial dropped label
    """

    if np.min(A) < 0:
        A = A + abs(np.min(A)) + 1
    if np.min(B) < 0:
        B = B + abs(np.min(B)) + 1

    # build tableax
    col_tableau = make_tableau(A)
    col_tableau = shift_tableau(col_tableau, A.shape)
    row_tableau = make_tableau(B.transpose())
    full_labels = set(range(sum(A.shape)))

    if initial_dropped_label in non_basic_variables(row_tableau):
        tableux = cycle((row_tableau, col_tableau))
    else:
        tableux = cycle((col_tableau, row_tableau))

    # First pivot (to drop a label)
    entering_label = pivot_tableau(next(tableux), initial_dropped_label)
    while non_basic_variables(row_tableau).union(non_basic_variables(col_tableau)) != full_labels:
        entering_label = pivot_tableau(next(tableux), next(iter(entering_label)))

    row_strategy = tableau_to_strategy(row_tableau, non_basic_variables(col_tableau),
                                       range(A.shape[0]))
    col_strategy = tableau_to_strategy(col_tableau, non_basic_variables(row_tableau),
                                       range(A.shape[0], sum(A.shape)))

    return row_strategy, col_strategy
