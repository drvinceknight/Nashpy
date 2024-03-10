.. _support-enumeration-discussion:

Support enumeration
===================

.. _motivating-example-coordination-game-nash-equilibria:

Motivating example: Coordination Game
-------------------------------------

In the :ref:`Coordination game <motivating-example-coordination-game>` in how
many situations do neither player have an incentive to **independently** change
their strategy?

Neither player having a reason to change their strategy implies that both
strategies are :ref:`Best responses<definition-of-best-response>` to each other.

To identify such pairs of strategies, we will use the
:ref:`best_response_condition` by considering all possible non zero valued
elements :math:`\sigma_r` and :math:`\sigma_c`.

Recall that for the Coordination game the matrices :math:`A` and :math:`B` are
given by:

.. math::

   A = \begin{pmatrix}
   3 & 1\\
   0 & 2
   \end{pmatrix}

.. math::

   B = \begin{pmatrix}
   2 & 1\\
   0 & 3
   \end{pmatrix}

If we consider strategies that only play a single action there are two options
for each strategy:

.. math::

    \sigma_r \in \{(1, 0), (0, 1)\}

and:

.. math::

    \sigma_c \in \{(1, 0), (0, 1)\}

We will inspect all four combinations:

- :math:`\sigma_r = (1, 0)` and :math:`\sigma_c = (1, 0)` which corresponds to
  both players playing their first action which gives: :math:`u_r(\sigma_r,
  \sigma_c)=3` and :math:`u_c(\sigma_r, \sigma_c)=2`. If the row player where to
  modify their strategy (while the column player stayed unchanged) to play the second
  action their utility would decrease. Likewise, if the column player were to
  modify their strategy their utility would also decrease.
- :math:`\sigma_r = (1, 0)` and :math:`\sigma_c = (0, 1)` which corresponds to
  the row player playing their first action and the column player playing their
  second action which gives: :math:`u_r(\sigma_r, \sigma_c)=1` and
  :math:`u_c(\sigma_r, \sigma_c)=1`. In this case, if either player were to move
  their utility would increase.
- :math:`\sigma_r = (0, 1)` and :math:`\sigma_c = (1, 0)` which corresponds to
  the row player playing their second action and the column player playing their
  first action which gives: :math:`u_r(\sigma_r, \sigma_c)=0` and
  :math:`u_c(\sigma_r, \sigma_c)=0`. In this case, if either player were to move
  their utility would increase.
- :math:`\sigma_r = (0, 1)` and :math:`\sigma_c = (0, 1)` which corresponds to
  both players playing their second action which gives: :math:`u_r(\sigma_r,
  \sigma_c)=2` and :math:`u_c(\sigma_r, \sigma_c)=3`. If the row player where to
  modify their strategy (while the column player stayed unchanged) to play the second
  action their utility would decrease.  Likewise, if the column player were to
  modify their strategy their utility would also decrease.

If we now consider strategies that play **both** actions there is a single
general form:

.. math::

   \sigma_r = (x, 1 - x)\text{ for } 0<x<1

.. math::

   \sigma_c = (y, 1 - y)\text{ for } 0<y<1

We can apply the :ref:`best_response_condition` here.

If :math:`\sigma_r` is a best response to :math:`\sigma_c` then:

.. math::

   (A\sigma_c^T)_i = \text{max}_{k\in\{1, 2\}} (A\sigma_c^T)_k \text{ for all }i \in \{1, 2\}

which gives:

.. math::

   3y + 1(1-y) &= \text{max}_{k \in\{1, 2\}} (A\sigma_c^T)_k\\
   0y + 2(1-y) &= \text{max}_{k \in\{1, 2\}} (A\sigma_c^T)_k

which in turn corresponds to:

.. math::

   3y + 1(1 - y) & = 2(1-y)\\
               y & = 1 / 4

Thus :math:`\sigma_r = (x, 1 - x)` with :math:`0<x<1` is a best response to
:math:`\sigma_c` if and only if :math:`\sigma_c = (1/4, 3/4)`.

We will now apply the :ref:`best_response_condition` again but to the column
player:

If :math:`\sigma_c` is a best response to :math:`\sigma_r` then:

.. math::

   (\sigma_rB)_j = \text{max}_{k\in\{1, 2\}} (\sigma_rB)_k \text{ for all }j \in \{1, 2\}

which gives:

.. math::

   2x + 0(1-x) &= \text{max}_{k \in\{1, 2\}} (\sigma_rB)_k\\
   1x + 3(1-x) &= \text{max}_{k \in\{1, 2\}} (\sigma_rB)_k

which in turn corresponds to:

.. math::

   2x & = x + 3(1-x)\\
   x & = 3 / 4

Thus :math:`\sigma_c = (y, 1 - y)` with :math:`0<y<1` is a best response to
:math:`\sigma_r` if and only if :math:`\sigma_r = (3/4, 1/4)`.

There are 3 pairs of strategies that are best responses to each other:

- :math:`\sigma_r=(1,0)` and :math:`\sigma_c=(1,0)`.
- :math:`\sigma_r=(0,1)` and :math:`\sigma_c=(0,1)`.
- :math:`\sigma_r=(3/4,1/4)` and :math:`\sigma_c=(1/4,3/4)`.

The support enumeration algorithm
---------------------------------

The approach used in
:ref:`motivating-example-coordination-game-nash-equilibria` is in fact an
application of a formalised algorithm called support enumeration.

The algorithm is as follows:

For a non :ref:`Degenerate <degenerate-games-discussion>` 2 player game
:math:`(A, B)\in{\mathbb{R}^{m\times n}}^2` the following algorithm returns all
pairs of best responses:

1. For all :math:`1\leq k\leq \min(m, n)`:
2. For all pairs of :ref:`support <definition-of-support-of-a-strategy>`
   :math:`(I, J)` with :math:`|I|=|J|=k`.
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

.. admonition:: Question
   :class: note

   Use support enumeration to find all Nash equilibria for the game given by
   :math:`A=\begin{pmatrix} 1 & 1 & -1 \\ 2 & -1 & 0 \end{pmatrix}` and
   :math:`B=\begin{pmatrix} 1/2 & -1 & -1/2 \\-1 & 3 & 2 \end{pmatrix}`.

.. admonition:: Answer
   :class: caution, dropdown

   1. It is immediate to note that there are no pairs of pure best responses.
   2. All possible support pairs are:

      - :math:`I=\{1, 2\}` and :math:`J=\{1,2\}`
      - :math:`I=\{1, 2\}` and :math:`J=\{1,3\}`
      - :math:`I=\{1, 2\}` and :math:`J=\{2,3\}`

   3. Let us solve the corresponding linear equations:

      - :math:`I=\{1, 2\}` and :math:`J=\{1, 2\}`:

        .. math::

           1/2{\sigma_{r}}_1-{\sigma_{r}}_2=-{\sigma_{r}}_1+3{\sigma_{r}}_2

        .. math::

           {\sigma_{r}}_1=8/3{\sigma_{r}}_2

        .. math::

           {\sigma_{c}}_1+{\sigma_{c}}_2=2{\sigma_{c}}_1-{\sigma_{c}}_2

        .. math::

           {\sigma_{c}}_1=2{\sigma_{c}}_2

      - :math:`I=\{1, 2\}` and :math:`J=\{1,3\}`:

        .. math::

           1/2{\sigma_{r}}_1-{\sigma_{r}}_2=-1/2{\sigma_{r}}_1+2{\sigma_{r}}_2

        .. math::

           {\sigma_{r}}_1=3{\sigma_{r}}_2

        .. math::

           {\sigma_{c}}_1-{\sigma_{c}}_3=2{\sigma_{c}}_1+0{\sigma_{c}}_3

        .. math::

           {\sigma_{c}}_1=-{\sigma_{c}}_3

      - :math:`I=\{1, 2\}` and :math:`J=\{2,3\}`:

        .. math::

           -{\sigma_{r}}_1+3{\sigma_{r}}_2=-1/2{\sigma_{r}}_1+2{\sigma_{r}}_2

        .. math::

           {\sigma_{r}}_1=2{\sigma_{r}}_2

        .. math::

           {\sigma_{c}}_2-{\sigma_{c}}_3=-{\sigma_{c}}_2+0{\sigma_{c}}_3

        .. math::

           2{\sigma_{c}}_2={\sigma_{c}}_3

   4. We check which supports give valid strategies:

      - :math:`I=\{1, 2\}` and :math:`J=\{1, 2\}`:

        .. math::

           \sigma_r=(8/11, 3/11)

        .. math::

           \sigma_c=(2/3, 1/3, 0)

      - :math:`I=\{1, 2\}` and :math:`J=\{1, 3\}`:

        .. math::

           \sigma_r=(3/4, 1/4)

        .. math::

           \sigma_c=(k, 0, -k)

        **which is not a valid strategy.**

      - :math:`I=\{1, 2\}` and :math:`J=\{2, 3\}`:

        .. math::

           \sigma_r=(2/3, 1/3)

        .. math::

           \sigma_c=(0, 1/3, 2/3)

   5. Let us verify the best response condition:

      - :math:`I=\{1, 2\}` and :math:`J=\{1, 2\}`:

        .. math::

           \sigma_c=(2/3, 1/3, 0)

        .. math::

           A\sigma_c^T=
           \begin{pmatrix}
           1\\
           1
           \end{pmatrix}

        Thus :math:`\sigma_r` is a best response to :math:`\sigma_c`

        .. math::

           \sigma_r=(8/11, 3/11)

        .. math::

           \sigma_r B=(1/11, 1/11, 2/11)

        Thus :math:`\sigma_c` is not a best response to :math:`\sigma_r`
        (because there is a better response outside of the support of
        :math:`\sigma_c`).


      - :math:`I=\{1, 2\}` and :math:`J=\{2, 3\}`:

        .. math::

           \sigma_c=(0, 1/3, 2/3)

        .. math::

           A\sigma_c^T=
           \begin{pmatrix}
           -1/3\\
           -1/3
           \end{pmatrix}

        Thus :math:`\sigma_r` is a best response to :math:`\sigma_c`

        .. math::

           \sigma_r=(2/3, 1/3)

        .. math::

           \sigma_r B=(0, 1/3, 1/3)

        Thus :math:`\sigma_c` is a best response to :math:`\sigma_r`.

       Thus the (unique) Nash equilibrium for this game is:

       .. math::

          ((2/3, 1/3), (0, 1/3, 2/3))

Exercises
---------


Use support enumeration to find Nash equilibria for the following
games:

1. 

.. math::

   A =
   \begin{pmatrix}
   3  & 3 & 2 \\
   2  & 1 & 3 
   \end{pmatrix}
   \qquad
   B =
   \begin{pmatrix}
   2  & 1 & 3 \\
   2  & 3 & 2 
   \end{pmatrix}
2. 

.. math:: 

   A =
   \begin{pmatrix}
   3 & -1\\
   2 & 7\end{pmatrix}
   \qquad
   B =
   \begin{pmatrix}
   -3 & 1\\
   1 & -6\end{pmatrix}


Using Nashpy
------------

See :ref:`how-to-use-support-enumeration` for guidance of how to use Nashpy to
use support enumeration.
