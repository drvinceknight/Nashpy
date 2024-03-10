.. _repeated-games-discussion:

Repeated Games
==============

.. _motivating-example-repeated-game:

Motivating example: Repeated Coordination Game
----------------------------------------------

Consider the :ref:`Coordination game <motivating-example-coordination-game>` but
in this instance Alice and Bob repeat their play of this game. In other words,
they aim to meet (both making their decision at the same time) and after this
first meeting they repeat the process, with full knowledge of the outcome of the
first play.

This can be represented pictorially as follows:

.. image:: /_static/discussion/repeated-coordination-game/main.png

To show this as an equivalent :ref:`extensive form game
<extensive-form-games-discussion>`, the tree is the same but we take care
to label the vertices correctly:

.. image:: /_static/discussion/repeated-coordination-game-as-extensive-form-game/main.png

.. _definition-of-repeated-games:

Definition of a repeated games
------------------------------

Given a two player game :math:`(A,B)\in\mathbb{R}^{{m\times n}^2}`, referred to
as a stage game, a :math:`T`-stage repeated game is a game in which players play that
stage game for :math:`T>0` repetitions. Players make decisions based on the full history of
play over all the repetitions.


.. admonition:: Question
   :class: note

   For the following values of :math:`T` and the following stage games, how many
   leaves would the extensive form representation of the repeated game have:

   1.

      .. math::

          A = \begin{pmatrix}1 & 2 \\ 2 & 3\end{pmatrix}
          \qquad
          B = \begin{pmatrix}2 & 3 \\ 1 & -1\end{pmatrix}
          \qquad
          T = 2

   2.

      .. math::

          A = \begin{pmatrix}0 & 1 \\ -1 & 3\end{pmatrix}
          \qquad
          B = -A
          \qquad
          T = 2

   3.

      .. math::

          A = \begin{pmatrix}0 & 1 \\ -1 & 3\end{pmatrix}
          \qquad
          B = -A
          \qquad
          T = 3

   4.

      .. math::

          A = \begin{pmatrix}0 & 1 & 4\\1 &-1 & 3\end{pmatrix}
          \qquad
          B = -A
          \qquad
          T = 2

.. admonition:: Answer
   :class: caution, dropdown

   1. The initial play of the game will have 4 leaves (corresponding to the
      2 choices by each player), each leave will in turn
      have 4 leaves. Thus, the total number of leaves will be 16.
   2. The initial play of the game will have 4 leaves (corresponding to the
      2 choices by each player), each leave will in turn
      have 4 leaves. Thus, the total number of leaves will be 16.
   3. The initial play of the game will have 4 leaves (corresponding to the
      2 choices by each player), each leave will in turn
      have 4 leaves in the second repetition. In the final repetition each of
      those leaves will have 4 leaves. Thus, the total number of leaves will be
      64.
   4. The initial play of the game will have 6 leaves (corresponding to the
      2 choices by the row player and 3 by the column player), each leave will
      in turn have 6 leaves in the second repetition. Thus, the total number of
      leaves will be 36.


.. _definition-of-strategies-in-repeated-games:

Strategies in a repeated game
-----------------------------

A strategy for a player in a repeated game is a mapping from all possible
histories of play to a probability
distribution over the action set of the stage game.


.. admonition:: Question
   :class: note

   For the :ref:`repeated coordination game <motivating-example-repeated-game>`
   which of the following are valid strategies, and in the case of valid
   strategies what is the outcome.

   1. For the row player:

      .. math::

         \begin{align*}
             (\emptyset, \emptyset) &\to C\\
             (S, S) &\to C\\
             (S, C) &\to C\\
             (C, S) &\to S\\
             (C, C) &\to S\\
         \end{align*}

      For the column player:

      .. math::

         \begin{align*}
             (\emptyset, \emptyset) &\to S\\
             (S, S) &\to C\\
             (S, C) &\to C\\
             (C, S) &\to S\\
             (C, C) &\to S\\
         \end{align*}

   2. For the row player:

      .. math::

         \begin{align*}
             (\emptyset, \emptyset) &\to C\\
             (S, S) &\to C\\
             (C, S) &\to S\\
             (C, C) &\to S\\
         \end{align*}

      For the column player:

      .. math::

         \begin{align*}
             (\emptyset, \emptyset) &\to S\\
             (S, S) &\to C\\
             (S, C) &\to C\\
             (C, S) &\to S\\
             (C, C) &\to S\\
         \end{align*}

   3. For the row player:

      .. math::

         \begin{align*}
             (\emptyset, \emptyset) &\to C\\
             (S, S) &\to C\\
             (C, S) &\to S\\
             (S, C) &\to S\\
             (C, C) &\to S\\
         \end{align*}

      For the column player:

      .. math::

         \begin{align*}
             (\emptyset, \emptyset) &\to S\\
             (S, S) &\to C\\
             (S, C) &\to C\\
             (C, S) &\to \alpha\\
             (C, C) &\to S\\
         \end{align*}

   4. For the row player:

      .. math::

         \begin{align*}
             (\emptyset, \emptyset) &\to S\\
             (S, S) &\to C\\
             (C, S) &\to S\\
             (S, C) &\to C\\
             (C, C) &\to S\\
         \end{align*}

      For the column player:

      .. math::

         \begin{align*}
             (\emptyset, \emptyset) &\to S\\
             (S, S) &\to C\\
             (S, C) &\to C\\
             (C, S) &\to S\\
             (C, C) &\to S\\
         \end{align*}

.. admonition:: Answer
   :class: caution, dropdown

   1. This is a valid strategy pair: all possible histories are mapped to
      correct actions. The outcome would be: :math:`(3,2)` (corresponding to
      :math:`O_9` of the extensive form representation).
   2. This is not a valid strategy pair: the row player strategy does not have a
      mapping from :math:`(S, C)`.
   3. This is not a valid strategy pair: the column player strategy maps from
      :math:`(C, S)` to an action (:math:`\alpha`) that is not in the action
      space of the stage game.
   4. This is a valid strategy pair: all possible histories are mapped to
      correct actions. The outcome would be: :math:`(5,5)` (corresponding to
      :math:`O_4` of the extensive form representation).

Equilibria in repeated games
----------------------------

In a repeated game it is possible for players to encode reputation and trust in
their strategies.

Consider as an example the following stage game with :math:`T=2`:

.. math::

   A =
       \begin{pmatrix}
           0 & 6 & 1\\
           1 & 7 & 5
       \end{pmatrix}
   \qquad
   B =
       \begin{pmatrix}
           0 & 3 & 1\\
           1 & 0 & 1
       \end{pmatrix}

Through inspection it is possible to verify that the following strategy pair is
a Nash equilibrium:

For the row player:

.. math::

   \begin{align*}
       (\emptyset, \emptyset) &\to r_1\\
       (r_1, c_1) &\to r_2\\
       (r_1, c_2) &\to r_2\\
       (r_1, c_3) &\to r_2\\
       (r_2, c_1) &\to r_2\\
       (r_2, c_2) &\to r_2\\
       (r_2, c_3) &\to r_2\\
   \end{align*}

For the column player:

.. math::

   \begin{align*}
       (\emptyset, \emptyset) &\to c_2\\
       (r_1, c_1) &\to c_3\\
       (r_2, c_1) &\to c_1\\
       (r_1, c_2) &\to c_3\\
       (r_2, c_2) &\to c_1\\
       (r_1, c_3) &\to c_3\\
       (r_2, c_3) &\to c_1\\
   \end{align*}

This pair of strategies correspond to the following scenario:

The row player plays :math:`r_1` and the column player plays :math:`c_2` in the
first state. The row player plays :math:`r_2` and the column player plays
:math:`c_3` in the second stage.

Note that if the row player deviates and plays :math:`r_2` in the first stage
then the column player will play :math:`c_1`.

If both players play these strategies their utilities are: :math:`(11, 4)` which is
better **for both players** then the utilities at any sequence of pure stage
Nash equilibria. **But** is this a Nash equilibrium? To find out we investigate
if either player has an incentive to deviate.

1. If the row player deviates, they would only be rational to do so in the first
   stage, if they did they would gain 1 in that stage but lose 4 in the second
   stage. Thus they have no incentive to deviate.
2. If the column player deviates, they would only do so in the first stage and
   gain no utility.

Thus this strategy pair **is a Nash equilibrium** and evidences how a reputation
can be built and cooperation can emerge from complex dynamics.

Exercises
---------

1. Write the full potential history :math:`\bigcup_{t=0}^{T-1}H(t)` for
   repeated games with :math:`T` periods in the following cases:

   1. :math:`\mathcal{A}_1=\mathcal{A}_2=\{0, 1\}` and :math:`T=2`
   2. :math:`\mathcal{A}_1=\{r_1, r_2\}\;\mathcal{A}_2=\{c_1, c_2\}` and :math:`T=3`

2. Obtain a formula for :math:`\left|\bigcup_{t=0}^{T-1}H(t)\right|` in
   terms of :math:`A_1, A_2` and :math:`T`.
3. Prove that a sequence of stage Nash equilibria is a Nash equilibria for the
   repeated game.
4. Obtain all sequence of stage Nash equilibria as well as another Nash
   equilibrium for the following repeated games:

   1. 

   .. math::
      
      A =
      \begin{pmatrix}
      3 & -1\\
      2 & 4\\
      3 & 1
      \end{pmatrix}
      \qquad
      B =
      \begin{pmatrix}
      13 & -1\\
      6 & 2\\
      3 & 1
      \end{pmatrix}
      \qquad
      T=2

   2.

   .. math::

      A =
      \begin{pmatrix}
      2 & -1 & 8\\
      4 & 2 & 9
      \end{pmatrix}
      \qquad
      B =
      \begin{pmatrix}
      13 & 14 & -1\\
      6 & 2 & 6
      \end{pmatrix}
      \qquad
      T=2

Using Nashpy
------------

Repeated games are a particularly compact way of representing a given subset of
:ref:`extensive-form-games-discussion`. Thus, it is possible to study them as an
equivalent :ref:`normal form game <equivalence-of-extensive-and-normal-form-games>`.
See :ref:`how-to-obtain-a-repeated-game` for guidance of how to use Nashpy to
generate a normal form game by repeating a stage game.
