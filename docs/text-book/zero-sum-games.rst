.. _zero-sum-games:

Zero Sum Games
==============

.. _motivating-example-zero-sum-games:

Motivating example: changing Rock Paper Scissors
------------------------------------------------

If we modify the game of :ref:`Rock Paper Scissora
<motivating-example-strategy-for-rps>` to add a single new strategy "Spock":

- Spock smashes Scissors and Rock.
- Paper disproves Spock.

The other modification is that the game is no longer symmetric: only the row
player can use the Well.

The mathematical representation of this game is given by:

.. math::

   A = \begin{pmatrix}
   0  & -1 & 1 \\
   1  & 0  & -1\\
   -1 & 1  & 0\\
   1  & -1 & 1
   \end{pmatrix}

Is there a way that the Row player can play that guarantees a particular
expected proportion of wins?

Optimising worst case outcomes
------------------------------

The value of a game
-------------------

Formulation of the linear program
---------------------------------

In a :ref:`Zero Sum Game <definition-of-zero-sum-game>`, given a row player
payoff matrix :math:`A` with :math:`m` rows and :math:`n` columns, the following
linear programme will give a strategy for the row player that ensures the best
possible utility as well as the value of the game:

.. math::

   \max_{x\in\mathbb{R}^{(m + 1)\times 1}} cx

Subject to:

.. math::

   \begin{align}
        M_{\text{ub}}x &\leq b_{\text{ub}} \\
        M_{\text{eq}}x &= b_{\text{eq}} \\
        x_i            &\geq 0&&\text{ for }i\leq m
   \end{align}

Where the parameters of the linear programme are defined by:

.. math::

   \begin{align}
       c &= (\underbrace{0, \dots, 0}_{m}, 1) && c\in\{0, 1\}^{1 \times (m + 1)}\\
       M_{\text{ub}} &= \begin{pmatrix}(-A^T)_{11}&\dots&(-A^T)_{1m}&1\\
                                       \vdots     &\ddots&\vdots           &1\\
                                       (-A^T)_{n1}&\dots&(-A^T)_{nm}&1\end{pmatrix} && M\in\mathbb{R}^{n\times (m + 1)}\\
       b_{\text{ub}} &= (\underbrace{0, \dots, 0}_{n})^T && b_{\text{ub}}\in\{0\}^{n\times 1}\\
       M_{\text{eq}} &= (\underbrace{1, \dots, 1}_{m}, 0) && M_{\text{eq}}\in\{0, 1\}^{1\times(m + 1)}\\
       b_{\text{eq}} &= 1 \\
   \end{align}

The minimax theorem
-------------------

Using Nashpy
------------

See :ref:`how-to-use-minimax` for guidance of how to use Nashpy to
find the Nash equilibria of Zero sum games using the mini max theorem.
