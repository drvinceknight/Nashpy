.. _lemke-howson:

The Lemke Howson Algorithm
==========================

The Lemke Howson algorithm implemented in :code:`Nashpy` is based on the
one described in [Nisan2007]_ originally introduced in [Lemke1964]_.

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

   .. math::
      B =
      \begin{pmatrix}
          1 & 3\\
          2 & 1
      \end{pmatrix}

   This is represented as a pair of tableau:

   .. math::

      T_c =
      \begin{pmatrix}
          3 & 1 & 1 & 0 & 1\\
          1 & 3 & 0 & 1 & 1
      \end{pmatrix}

   For reasons that will become clear, we infact shift this tableau so
   that the labelling is coherent across both polytopes:

   .. math::

      T_c =
      \begin{pmatrix}
          1 & 0 & 3 & 1 & 1\\
          0 & 1 & 1 & 3 & 1
      \end{pmatrix}

   Here it is as a :code:`numpy` array::

       >>> import numpy as np
       >>> col_tableau = np.array([[1, 0, 3, 1, 1],
       ...                         [0, 1, 1, 3, 1]])

   Here is the tableau that corresponds to :math:`B`:

   .. math::

      T_r =
      \begin{pmatrix}
          1 & 2 & 1 & 0 & 1\\
          3 & 1 & 0 & 1 & 1
      \end{pmatrix}

   Here it is as a :code:`numpy` array::

       >>> row_tableau = np.array([[1, 2, 1, 0, 1],
       ...                         [3, 1, 0, 1, 1]])

2. Step 2, choosing a starting label is choosing an integer from :math:`0 \leq k
   < m + n` (we start our indices at 0). As an example, let us choose the label
   :math:`1`.

   First we need to identify which vertex has that label. The labels of a
   tableau correspond to the non basic variables: these are the columns with
   more than a single non zero variable:

   - The labels of :math:`T_c` are thus :math:`\{2, 3\}`::

         >>> from nashpy.linalg.tableau import Tableau
         >>> ctableau = Tableau(col_tableau)
         >>> ctableau.non_basic_variables
         {2, 3}


   - The labels of :math:`T_r` are thus :math:`\{0, 1\}`::

         >>> rtableau = Tableau(row_tableau)
         >>> rtableau.non_basic_variables
         {0, 1}

   So we are going to drop label :math:`1` from :math:`T_r`.


3. Step 3, removing a label and moving from one vertex to another corresponds
   to integer pivoting [Dantzig2016]_. This is a manipulation of :math:`T`,
   dropping label :math:`1` corresponds to pivoting the second column.

   To do this we need to identify which row will not change (the "pivot row"),
   this is done by finding the smallest ratio of value in that column over the
   value in the last column: :math:`(T_{r})_{i4}/(T_{r})_{ik}`.

   In our case the first row has corresponding ratio: :math:`1/2` and the second
   ratio :math:`1/1`. So our pivot row is the first row::

       >>> rtableau._find_pivot_row(column_index=1)
       0

   What we now do is row operations so as to make the second column correspond
   to a basic variable. We will do this by multiplying the second row by 2 and
   then subtracting the first row by it:

   .. math::

      T_r =
      \begin{pmatrix}
          1  & 2 & 1 & 0 & 1\\
          5 & 0 & -1 & 2 & 1
      \end{pmatrix}


   Our resulting tableau has labels: :math:`\{0, 2\}` so it has "picked up"
   label :math:`2`::

       >>> rtableau.pivot_and_drop_label(column_index=1)
       2
       >>> rtableau._tableau
       array([[ 1,  2,  1,  0,  1],
              [ 5,  0, -1,  2,  1]])


4. Step 4, we will now repeat the previous manipulation on :math:`T_c` where we
   now need to drop the duplicate label :math:`2`. We do this by pivoting the
   third column.

   The ratios are: :math:`1/3` for the first row and :math:`1/1` for the
   second, thus the pivot row is the first row::

       >>> ctableau._find_pivot_row(column_index=2)
       0

   Using similar row operations we obtain:

   .. math::

      T_c =
      \begin{pmatrix}
           1 & 0 & 3 & 1 & 1\\
          -1 & 3 & 0 & 8 & 2
      \end{pmatrix}

   Our resulting tableau has labels: :math:`\{0, 3\}`, so it has picked up
   label :math:`0`::

       >>> ctableau.pivot_and_drop_label(column_index=2)
       0
       >>> ctableau._tableau
       array([[ 1,  0,  3,  1,  1],
              [-1,  3,  0,  8,  2]])

   We now need to drop :math:`0` from :math:`T_r`, we do this by pivoting the
   first column. The ratio test: :math:`1/1 > 1/5` implies that the second row
   is the pivot row. Using similar algebraic manipulations we obtain:

   .. math::

      T_r =
      \begin{pmatrix}
          0 & 10 & 6 & -2 & 4\\
          5 & 0 & -1 & 2 & 1
      \end{pmatrix}

   Our resulting tableau has labels: :math:`\{2, 3\}`, so it has picked up
   label :math:`3`::

       >>> rtableau.pivot_and_drop_label(column_index=0)
       3
       >>> rtableau._tableau
       array([[ 0, 10,  6, -2,  4],
              [ 5,  0, -1,  2,  1]])

   We now need to drop :math:`3` from :math:`T_c`, we do this by pivoting the
   fourth column. The ratio test: :math:`1/1>2/8` indicates that we pivot on the
   second row which gives:

   .. math::

      T_c =
      \begin{pmatrix}
           9 & -1& 24 & 0 & 6\\
          -1 &  3& 0  & 8 & 2
      \end{pmatrix}

   Our resulting tableau has labels: :math:`\{0, 1\}`::

       >>> ctableau.pivot_and_drop_label(column_index=3)
       1
       >>> ctableau._tableau
       array([[ 9, -3, 24,  0,  6],
              [-1,  3,  0,  8,  2]])

   The union of the labels of :math:`T_r` and :math:`T_c` is: :math:`\{0, 1, 2,
   3\}` which implies that we have a fully labeled vertx pair.

   The vertex corresponding to :math:`T_r` are obtained by setting the non basic
   variables to 0 and looking at the corresponding values of the first two
   columns:

   .. math::

      v_r = (1/5, 4/10) = (1/5, 2/5)

   The vertex corresponding to :math:`T_c` are obtained from the last 2 columns:

   .. math::

      v_c = (6/24, 2/8) = (1/4, 1/4)

The final step of the algorithm is to return the normalised probabilities that
correspond to these vertices:

.. math::

   ((1/3, 2/3), (1/2, 1/2))
