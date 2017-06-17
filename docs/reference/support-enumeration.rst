.. _support-enumeration:

Support enumeration
===================

The support enumeration algorithm implemented in :code:`Nashpy` is based on the
one described in [Nisan2007]_.

The algorithm is as follows:

For a nondegenerate 2 player game :math:`(A, B)\in{\mathbb{R}^{m\times n}}^2`
the following algorithm returns all nash equilibria:

1. For all :math:`1\leq k\leq \min(m, n)`;
2. For all pairs of support :math:`(I, J)` with :math:`|I|=|J|=k`
3. Solve the following equations (this ensures we have best responses):

   .. math::

	  \sum_{i\in I}{\sigma_{r}}_iB_{ij}=v\text{ for all }j\in J

      \sum_{j\in J}A_{ij}{\sigma_{c}}_j=u\text{ for all }i\in I

4. Solve

   - :math:`\sum_{i=1}^{m}{\sigma_{r}}_i=1` and :math:`{\sigma_{r}}_i\geq 0`
     for all :math:`i`
   - :math:`\sum_{j=1}^{n}{\sigma_{c}}_i=1` and :math:`{\sigma_{c}}_j\geq 0`
     for all :math:`j`

5. Check the best response condition.

Repeat steps 3,4 and 5 for all potential support pairs.

Discussion
----------

1. Step 1 is a complete enumeration of all possible strategies that the
   equilibria could be.
2. Step 2 is based on the definition of a non degenerate game which ensures that
   equilibria will be on supports of the same size.
3. Step 3 are the linear equations that are to be solved, for a given pair of
   supports these ensure that neither player has an incentive to move to another
   strategy on that support.
4. Step 4 is to ensure we have mixed strategies.
5. Step 5 is a final check that there is no better utility outside of the
   supports.

In :code:`Nashpy` this is all implemented algebraically using :code:`Numpy` to
solve the linear equations.
