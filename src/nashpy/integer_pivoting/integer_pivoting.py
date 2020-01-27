"""
A class for integer pivoting. Used for an implementation of the Lemke Howson
algorithm.
"""
import numpy as np


def make_tableau(M):
    """
    Make a tableau for the given matrix M.

    This tableau corresponds to the polytope of the form:

       Mx <= 1 and x >= 0
    """
    return np.append(
        np.append(M, np.eye(M.shape[0]), axis=1),
        np.ones((M.shape[0], 1)),
        axis=1,
    )


def find_pivot_row(tableau, column_index):
    """
    Find the index of the row to pivot.

    Identifies the row to pivot by performing a minimum ratio test. (In fact
    implemented to calculate the maximum ratio test to avoid divide by zero
    errors).
    """
    return np.argmax(tableau[:, column_index] / tableau[:, -1])

#+==========
def find_pivot_row_lex(tableau, column_index, slack_variables):

    C = tableau[:,slack_variables]
    lex_order_reversed = np.lexsort(np.rot90(C))
    lex_order = -lex_order_reversed + lex_order_reversed.shape[0]

    pivot_column = tableau[:, column_index]
    Cq = tableau[:, -1]

    #filter out column coefficient == 0 (avoid /0 error)
    #ratio = np.where(pivot_column==0,np.full(Cq.shape,np.inf),np.divide(Cq,pivot_column))
    ratio = np.divide(Cq,pivot_column)

    #filter out column coefficient <0 (doesn't preserve feasibility)
    filtered_ratio = np.where(pivot_column<=0,np.full(ratio.shape,np.inf),ratio)
    
    return np.lexsort(np.rot90(np.transpose((filtered_ratio,lex_order))))[0]


def non_basic_variables(tableau):
    """
    Identifies the non basic variables of a tableau,
    these correspond to the labels.
    """
    columns = tableau[:, :-1].transpose()
    return set(np.where([np.count_nonzero(col) != 1 for col in columns])[0])

def zero_basic_variables(tableau):
    Cq = tableau[:,-1]
    zero_rows = set(np.asarray(Cq==0).nonzero()[0])

    basic_variables = set(range(tableau.shape[1]-1)) - non_basic_variables(tableau)
    #return set of basic variables such that non-zero row of each variable has 0 for Cq
    #gives list of pairs (basic_col_index, non-zero row index)
    basic_variable_rows = [(col,np.where(tableau[:,col]!=0)[0][0]) for col in basic_variables]
    return set(map(lambda x: x[0], filter(lambda x: x[1] in zero_rows,basic_variable_rows)))


def pivot_tableau(tableau, column_index):
    """
    Pivots the tableau and returns the dropped label
    """
    original_labels = non_basic_variables(tableau)
    pivot_row_index = find_pivot_row(tableau, column_index)
    pivot_element = tableau[pivot_row_index, column_index]

    
    print('pivot row: ', pivot_row_index)
    print(tableau)

    for i, _ in enumerate(tableau):
        if i != pivot_row_index:
            tableau[i, :] = (
                tableau[i, :] * pivot_element
                - tableau[pivot_row_index, :] * tableau[i, column_index]
            )

    print('original_labels: ', original_labels)
    print('pivot column: ', column_index)
    print('new_labels: ', non_basic_variables(tableau))

    print(tableau)

    print('=================')

    return non_basic_variables(tableau) - original_labels

def pivot_tableau_lex(tableau, column_index, slack_variables):
    """
    Pivots the tableau and returns the dropped label
    """
    original_labels = non_basic_variables(tableau)
    pivot_row_index = find_pivot_row_lex(tableau, column_index, slack_variables)
    pivot_element = tableau[pivot_row_index, column_index]

    print('pivot row: ', pivot_row_index)
    print(tableau)

    for i, _ in enumerate(tableau):
        if i != pivot_row_index:
            tableau[i, :] = (
                tableau[i, :] * pivot_element
                - tableau[pivot_row_index, :] * tableau[i, column_index]
            )

    

    print('original_labels: ', original_labels)
    print('pivot column: ', column_index)
    print('new_labels: ', non_basic_variables(tableau))


    print(tableau)

    print('=================')

    return non_basic_variables(tableau) - original_labels
