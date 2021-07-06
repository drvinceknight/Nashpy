.. _strategies-discussion:

Strategies
==========

.. _motivating-example-strategy-for-rps:

Motivating example: Strategy for Rock Paper Scissors
----------------------------------------------------

The game of Rock Paper Scissors is a common parlour game between two players who
pick 1 of 3 options simultaneously:

1. Rock which beats Scissors;
2. Paper which beats Rock;
3. Scissors which beats Paper

Thus, this corresponds to a Normal Form Game with:

1. Two players (:math:`N=2`).
2. The action sets are: :math:`\mathcal{A}_1=\mathcal{A}_2=\{\text{Rock}, \text{Paper}, \text{Scissors}\}`
3. The payoff functions are given by the matrices :math:`A, B` where the
   first row or column corresponds to :math:`\text{Rock}`, the second to
   :math:`\text{Paper}` and the third to :math:`\text{Scissors}`.

.. math::

   A = \begin{pmatrix}
   0  & -1 & 1 \\
   1  & 0  & -1\\
   -1 & 1  & 0\\
   \end{pmatrix}

.. math::

   B = - A = \begin{pmatrix}
   0  & 1 & -1 \\
   -1  & 0  & 1\\
   1 & -1  & 0\\
   \end{pmatrix}

If we consider two players, assume the row player always chooses
:math:`\text{Paper}` and the column player randomly chooses from
:math:`\text{Rock}` and :math:`\text{Paper}` (with equal probability) what is
the expected outcome of any one game between them?

- The expected score of the row player will be: :math:`-1 \times 1/2 + 0 \times 1/2 = -1/2`.
- The expected score of the column player will be: :math:`1 \times 1/2 + 0 \times 1/2 = 1/2`.

In Game theoretic terms, the behaviours described above are referred to as
**strategies**. **Strategies map information to actions.** In this particular case,
the only available information is the game itself and the actions are
:math:`\mathcal{A}_1=\mathcal{A}_2`.

Definition of a strategy in a normal form game
----------------------------------------------

A strategy for a player with action set :math:`\mathcal{A}` is a probability
distribution over elements of :math:`\mathcal{A}`.

Typically a strategy is denoted by :math:`\sigma \in [0, 1]^{|\mathcal{A}|}_{\mathbb{R}}` so that:

.. math::

   \sum_{i=1}^{\mathcal{S}}\sigma_i = 1

.. admonition:: Question
   :class: note

   For :ref:`Rock Papoer Scissors <motivating-example-strategy-for-rps>`:

   1. What is the strategy :math:`\sigma_r` that corresponds to the row player's
      behaviour of always choosing :math:`\text{Paper}`?
   2. What is the strategy :math:`\sigma_c` that corresponds to the column
      player's behaviour of always randomly choosing between
      :math:`\text{Rock}` and :math:`\text{Paper}`?

.. admonition:: Answer
   :class: caution, dropdown

   1. :math:`\sigma_r = (0, 1, 0)`
   2. :math:`\sigma_c = (1 / 2, 1 / 2, 0)`

Calculation of expected utilities
---------------------------------

Considering a game :math:`(A, B) \in \mathbb{R} ^{(m\times n) ^ 2}`, if
:math:`\sigma_r` and :math:`\sigma_c` are the strategies for the row/column
player, the expected utilities are:

- For the row player: :math:`u_{r}(\sigma_r, \sigma_c) = \sum_{i=1}^m\sum_{j=1}^nA_{ij}\sigma_{r_i}\sigma_{c_j}`
- For the column player: :math:`u_{c}(\sigma_r, \sigma_c) = \sum_{i=1}^m\sum_{j=1}^nB_{ij}\sigma_{r_i}\sigma_{c_j}`

This corresponds to taking the expectation over the probability distributions
:math:`\sigma_r` and :math:`\sigma_c`.

.. admonition:: Question
   :class: note

   For the :ref:`Rock Papoer Scissors <motivating-example-strategy-for-rps>`:

   What are the expected utilities to both players if :math:`\sigma_r=(1/3, 0, 2/3)` and :math:`\sigma_c=(1/3, 1/3, 1/3)`.

.. admonition:: Answer
   :class: caution, dropdown

   .. math::

      \begin{align}
      u_r(\sigma_r, \sigma_c) = & 1/3(1/3 \times 0 + 1/3 \times -1 + 1/3 \times 1) \\
                                & + 0(1/3 \times 1 + 1/3 \times 0 + 1/3 \times -1) \\
                                & + 2/3(1/3 \times -1 + 1/3 \times 1 + 1/3 \times 0) \\
                              = & 0
      \end{align}

   .. math::

      \begin{align}
      u_c(\sigma_r, \sigma_c) = & 1/3(1/3 \times 0 + 1/3 \times 1 + 1/3 \times -1) \\
                                & + 0(1/3 \times -1 + 1/3 \times 0 + 1/3 \times 1) \\
                                & + 2/3(1/3 \times 1 + 1/3 \times -1 + 1/3 \times 0) \\
                              = & 0
      \end{align}

Linear algebraic calculation of expected utilities
--------------------------------------------------

Given a game :math:`(A, B) \in \mathbb{R} ^{(m\times n) ^ 2}`, considering
:math:`\sigma_r` and :math:`\sigma_c` as vectors in :math:`\mathbb{R}^m` and
:math:`\mathbb{R}^n`. The expected utilities can be written as the matrix vector
product:

- For the row player: :math:`u_{r}(\sigma_r, \sigma_c) = \sigma_r A \sigma_c^T`
- For the column player: :math:`u_{c}(\sigma_r, \sigma_c)  = \sigma_r B \sigma_c^T`

.. admonition:: Question
   :class: note

   For :ref:`Rock Paper Scissors <motivating-example-strategy-for-rps>`:

   Calculate the expected utilities to both players if :math:`\sigma_r=(1/3, 0, 2/3)`
   and :math:`\sigma_c=(1/3, 1/3, 1/3)` using a linear algebraic approach.

.. admonition:: Answer
   :class: caution, dropdown

   .. math::

      u_r(\sigma_r, \sigma_c) = (1/3, 0, 2/3) A \begin{pmatrix}1/3 \\ 1/3 \\ 1/3\end{pmatrix} = (-2/3, 1/3, 1/3)\begin{pmatrix}1/3 \\ 1/3 \\ 1/3\end{pmatrix} = 0

   .. math::

      u_c(\sigma_r, \sigma_c) = (1/3, 0, 2/3) B \begin{pmatrix}1/3 \\ 1/3 \\ 1/3\end{pmatrix} = (2/3, -1/3, -1/3)\begin{pmatrix}1/3 \\ 1/3 \\ 1/3\end{pmatrix} = 0

Strategy spaces for Normal form Games
-------------------------------------

.. TODO

Using Nashpy
------------

See :ref:`how-to-calculate-utilities` for guidance of how to use Nashpy to
calculate utilities.
