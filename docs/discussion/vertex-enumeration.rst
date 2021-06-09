.. _vertex-enumeration:

Vertex enumeration
==================

The vertex enumeration algorithm implemented in :code:`Nashpy` is based on the
one described in [Nisan2007]_.

The algorithm is as follows:

For a nondegenerate 2 player game :math:`(A, B)\in{\mathbb{R}^{m\times n}}^2`
the following algorithm returns all nash equilibria:

1. Obtain the best response Polytopes :math:`P` and :math:`Q`.
2. For all pairs of vertices of :math:`P` and :math:`Q`.
3. Check if the pair is fully labeled and return the normalised probability
   vectors.

Repeat steps 2 and 3 for all pairs of vertices.

Discussion
----------

1. Before creating the best response Polytope we need to consider the best
   response Polyhedron. For the row player, this corresponds to the set of all
   the mixed strategies available to the row player as well as an upper bound on
   the utilities to the column player. Analogously for the column player:

   .. math::

      \bar P = \{(x, v) \in \mathbb{R}^m \times \mathbb{R}\;|\; x\geq 0,
                                                         \mathbb{1}x=1,
                                                         B^Tx\leq\mathbb{1}v\}

      \bar Q = \{(y, u) \in \mathbb{R}^n \times \mathbb{R}\;|\; y\geq 0,
                                                         \mathbb{1}y=1,
                                                         Ay\leq\mathbb{1}u\}


   Note that in both definitions above we have a total of :math:`m + n`
   inequalities in the constraints.

   For :math:`P`, the first :math:`m` of those
   constraints correspond to the elements of :math:`x` being greater or equal to
   0. For a given :math:`x`, if :math:`x_i=0`, we say that :math:`x` has label
   :math`i`. This corresponds to strategy :math:`i` not being in the support of
   :math:`x`.

   For the last :math:`n` of these inequalities, when they are equalities they
   correspond to whether or not strategy :math:`1\leq j \leq n` of the other
   player is a best response to :math:`x`. Similarly, if strategy :math:`j` is a
   best response to :math:`x` then we say that :math:`x` has label :math:`m +
   j`.

   This all holds analogously for the column player. If the labels of a pair of
   elements of :math:`\bar P` and :math:`\bar Q` give the full set of integers
   from :math:`1` to :math:`m + n` then they represent strategies that are best
   responses to each other. Since, this would imply that either a pure stragey
   is not played or it is a best response to the other players strategy.

   The difficulty with using the best response Polyhedron is that the upper
   bound on the utilities of both players (:math:`u, v`) is not known.
   Importantly, we do not need to know it. Thus, we assume that in both cases:
   :math:`u=v=1` (this corresponds to a scaling of our strategy vectors).

   This allows us to define the best response Polytopes:

   .. math::

      P = \{(x, v) \in \mathbb{R}^m \times \mathbb{R}\;|\; x\geq 0,
                                                    B^Tx\leq 1\}

      Q = \{(y, u) \in \mathbb{R}^n \times \mathbb{R}\;|\; y\geq 0,
                                                         Ay\leq 1\}


2. Step 2: The vertices of these polytopes are the points that will have labels
   (they are the points that are at the intersection of the underlying
   halfspaces [Ziegler2012]_).

   To find these vertices, :code:`nashpy` uses :code:`scipy` which has a handy
   class for creating Polytopes using the inequality definitions and being able
   to return the vertices. Here is the wrapper written in :code:`nashpy` that is
   used by the vertex enumeration algorithm to give the vertices and
   corresponding labels::

       >>> import nashpy as nash
       >>> import numpy as np
       >>> A = np.array([[3, 1], [1, 3]])
       >>> halfspaces = nash.polytope.build_halfspaces(A)
       >>> vertices = nash.polytope.non_trivial_vertices(halfspaces)
       >>> for vertex in vertices:  # doctest: +SKIP
       ...     print(vertex)
       (array([0.333..., 0...]), {0, 3})
       (array([0..., 0.333...]), {1, 2})
       (array([0.25, 0.25]), {0, 1})

3. Step 3, we iterate over all pairs of the vertices of both polytopes and pick
   out the ones that are fully labeled. Because of the scaling that took place
   to create the Polytope from the Polyhedron, we will need to return a
   normalisation of both vertices.
