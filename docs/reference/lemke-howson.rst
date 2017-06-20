.. _lemke-howson:

The Lemke Howson Algorithm
==========================

The Lemke Howson algorithm implemented in :code:`Nashpy` is based on the
one described in [Nisan2007]_.

The algorithm is as follows:

For a nondegenerate 2 player game :math:`(A, B)\in{\mathbb{R}^{m\times n}}^2`
the following algorithm returns a single Nash equilibria:

1. Obtain the best response Polytopes :math:`P` and :math:`Q`.
2. Choose a starting label to drop, this will correspond to a vertex of
   :math:`P` or :math:`Q`.
3. In that polytope, remove the label from the corresponding vertex and move to
   the vertex that shared that label. A new label will be picked up and
   duplicated in the other polytope.
4. In the other polytope drop the duplicate label and move to the vertex that
   shared that label.

Repeat steps 3 and 4 until there are no duplicate labels.

Discussion
----------

This algorithm is implemented using integer pivoting.

1. Step 1, the best response polytopes :math:`P` and :math:`Q` are represented
   by a tableau. For example for:

   .. math::

      A =
      \begin{pmatrix}
          3 & 1\\
          1 & 3
      \end{pmatrix}

   This is represented as a tableau:

   .. math::

      T =
      \begin{pmatrix}
          3 & 1 & 1 & 0 & 1\\
          1 & 3 & 0 & 1 & 1
      \end{pmatrix}

2. Step 2, choosing a starting label is choosing an integer from 0 to :math:`m +
   n`.
3. Step 3, removing a label and moving from one vertex corresponds to integer
   pivoting [Dantzig2016]_. This is a manipulation of :math:`T` and is done
   using :code:`numpy`. In this case, the labels of the corresponding vertex
   correspond to the non basic variables to the tableau.
4. Step 4, we keep repeating the previous steps using integer pivoting.
