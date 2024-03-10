.. _normal-form-games-discussion:

Normal Form Games
=================

.. _motivating-example-coordination-game:

Motivating example: Coordination Game
-------------------------------------

Game theory is the study of interactive decision making. One example of this is
the following situation:

    Two friends must decide what movie to watch at the cinema. Alice would like
    to watch a sport movie and Bob would like to watch a comedy. Importantly,
    they would both rather spend their evening together than apart.

To quantify this mathematically, numeric values are associated to the 4
possible outcomes:

1. Alice watches a sport movie, Bob watches a comedy: Alice receives a utility
   of 1 and Bob a utility of 1.
2. Alice watches a comedy, Bob watches a sport movie: Alice receives a utility
   of 0 and Bob a utility of 0.
3. Alice and Bob both watch a sport movie: Alice receives a utility of 3 and Bob
   a utility of 2.
4. Alice and Bob both watch a comedy: Alice receives a utility of 2 and Bob
   a utility of 3.

This particular example will be
represented using two matrices.

:math:`A` will represent the utilities of Alice:

.. math::

   A = \begin{pmatrix}
   3 & 1\\
   0 & 2
   \end{pmatrix}

:math:`B` will represent the utilities of Bob

.. math::

   B = \begin{pmatrix}
   2 & 1\\
   0 & 3
   \end{pmatrix}

Alice is referred to as the row player and Bob as the column player:

- The row player chooses which row of the matrices the player will gain their
  utilities.
- The column player chooses which column of the matrices the player will gain
  their utilities.

This representation of the strategic interaction between Alice and Bob is called
a :ref:`Normal Form Game <definition-of-normal-form-game>`

.. _definition-of-normal-form-game:

Definition of Normal Form Game
------------------------------

An :math:`N` player normal form game consists of:

- A finite set of :math:`N` players.
- Action set for the players: :math:`\{\mathcal{A}_1, \mathcal{A}_2, \dots \mathcal{A}_N\}`
- Payoff functions for the players: :math:`u_i : \mathcal{A}_1 \times \mathcal{A}_2 \dots \times \mathcal{A}_N \to \mathbb{R}`

.. admonition:: Question
   :class: note

   For the :ref:`Coordination game <motivating-example-coordination-game>`:

   1. What is the finite set of players?
   2. What are the action sets?
   3. What are the payoff functions?

.. admonition:: Answer
   :class: caution, dropdown

   1. The two players are Alice and Bob (:math:`N=2`).
   2. The action sets are: :math:`\mathcal{A}_1=\mathcal{A}_2=\{\text{Sport}, \text{Comedy}\}`
   3. The payoff functions are given by the matrices :math:`A, B` where the
      first row or column corresponds to :math:`\text{Sport}` and the second
      row or column corresponds to :math:`\text{Comedy}`.

      ..  math::

          u_1(\mathcal{a}_1, \mathcal{a}_2) = A_{\mathcal{a}_1, \mathcal{a}_2} \qquad
          u_2(\mathcal{a}_1, \mathcal{a}_2) = B_{\mathcal{a}_1, \mathcal{a}_2}

      where :math:`\mathcal{a}_1\in \mathcal{A}_1` and :math:`\mathcal{a}_2\in
      \mathcal{A}_2`.

.. _definition-of-zero-sum-game:

Definition of a Zero Sum Game
-----------------------------

A two player normal form game with payoff matrices :math:`A, B` is called zero
sum if and only if:

.. math::

   A = -B

.. admonition:: Question
   :class: note

   Is the :ref:`Coordination game <motivating-example-coordination-game>` zero sum?

.. admonition:: Answer
   :class: caution, dropdown

   :math:`A\ne -B` so the Coordination game is not Zero sum.


Examples of other Normal Form Games
-----------------------------------

.. _prisoners-dilemma:

Prisoners Dilemma
*****************

Assume two thieves have been caught by the police and separated for questioning.
If both thieves cooperate and do not divulge any information they will each get
a short sentence (with a utility value of 3). If one defects they are offered a
deal (utility value of 5) while the other thief will get a long sentence
(utility value of 0). If they both defect they both get a medium length sentence
(utility value of 1).

.. admonition:: Question
   :class: note

   For the Prisoners Dilemma

   1. What is the finite set of players?
   2. What are the action sets?
   3. What are the payoff functions?
   4. Is the game zero sum?

.. admonition:: Answer
   :class: caution, dropdown

   1. The two players are the two thiefs (:math:`N=2`).
   2. The action sets are: :math:`\mathcal{A}_1=\mathcal{A}_2=\{\text{Cooperate}, \text{Defect}\}`
   3. The payoff functions are given by the matrices :math:`A, B` where the
      first row or column corresponds to :math:`\text{Cooperate}` and the second
      row or column corresponds to :math:`\text{Defect}`.

      ..  math::

          A = \begin{pmatrix}
          3 & 0\\
          5 & 1
          \end{pmatrix}
          \qquad
          B = \begin{pmatrix}
          3 & 5\\
          0 & 1
          \end{pmatrix}

      ..  math::

          u_1(\mathcal{a}_1, \mathcal{a}_2) = A_{\mathcal{a}_1, \mathcal{a}_2} \qquad
          u_2(\mathcal{a}_1, \mathcal{a}_2) = B_{\mathcal{a}_1, \mathcal{a}_2}

      where :math:`\mathcal{a}_1\in \mathcal{A}_1` and :math:`\mathcal{a}_2\in
      \mathcal{A}_2`.

   4. The game is not Zero sum as :math:`A \ne -B`.

Hawk Dove Game
**************

Suppose two birds of prey must share a limited resource. The birds can act like
a hawk or a dove. Hawks always act aggressively over the resource to the point of
exterminating another hawk (both hawks get a utility value of 0) and/or take a
majority of the resource from a dove (the hawk gets a utility value of 3 and the
dove a utility value of 1). Two doves can share the resource (both getting a
utility value of 2).

.. admonition:: Question
   :class: note

   For the Hawk Dove Game

   1. What is the finite set of players?
   2. What are the action sets?
   3. What are the payoff functions?
   4. Is the game zero sum?

.. admonition:: Answer
   :class: caution, dropdown

   1. The two players are two birds :math:`N=2`.
   2. The action sets are: :math:`\mathcal{A}_1=\mathcal{A}_2=\{\text{Hawk}, \text{Dove}\}`
   3. The payoff functions are given by the matrices :math:`A, B` where the
      first row or column corresponds to :math:`\text{Hawk}` and the second
      row or column corresponds to :math:`\text{Dove}`.

      ..  math::

          A = \begin{pmatrix}
          0 & 3\\
          1 & 2
          \end{pmatrix}
          \qquad
          B = \begin{pmatrix}
          0 & 1\\
          3 & 2
          \end{pmatrix}

      ..  math::

          u_1(\mathcal{a}_1, \mathcal{a}_2) = A_{\mathcal{a}_1, \mathcal{a}_2} \qquad
          u_2(\mathcal{a}_1, \mathcal{a}_2) = B_{\mathcal{a}_1, \mathcal{a}_2}

      where :math:`\mathcal{a}_1\in \mathcal{A}_1` and :math:`\mathcal{a}_2\in
      \mathcal{A}_2`.

   4. The game is not Zero sum as :math:`A \ne -B`.

Pigs
****

Consider two pigs. One dominant pig and one subservient pig. These pigs share a
pen. There is a lever in the pen that delivers food but if either pig pushes the
lever it will take them a little while to get to the food.

- If the dominant pig pushes the lever, the subservient pig has some time to eat
  most of the food before being pushed out of the way. The dominant pig gets a
  utility value of 2 and the subservient pig gets a utility value of 3.
- If the subservient pig pushes the lever, the dominant pig will eat all the
  food. The dominant pig gets a utility value of 6 and the subservient pig gets
  a utility value of -1.
- If both pigs push the lever, the subservient pig will a small amount of the
  food. The dominant pig gets a utility value of 4 and the subservient pig gets
  a utility value of 2.
- If both pigs do not push the lever they both get a utility value of 0.

.. admonition:: Question
   :class: note

   For the Pigs Game

   1. What is the finite set of players?
   2. What are the action sets?
   3. What are the payoff functions?
   4. Is the game zero sum?

.. admonition:: Answer
   :class: caution, dropdown

   1. The two players are dominant and a subservient pig :math:`N=2`.
   2. The action sets are: :math:`\mathcal{A}_1=\mathcal{A}_2=\{\text{Push}, \text{Do not push}\}`
   3. The payoff functions are given by the matrices :math:`A, B` where the
      first row or column corresponds to :math:`\text{Push}` and the second
      row or column corresponds to :math:`\text{Do not push}`.

      ..  math::

          A = \begin{pmatrix}
          4 & 2\\
          6 & 0
          \end{pmatrix}
          \qquad
          B = \begin{pmatrix}
          2 & 3\\
          -1 & 0
          \end{pmatrix}

      ..  math::

          u_1(\mathcal{a}_1, \mathcal{a}_2) = A_{\mathcal{a}_1, \mathcal{a}_2} \qquad
          u_2(\mathcal{a}_1, \mathcal{a}_2) = B_{\mathcal{a}_1, \mathcal{a}_2}

      where :math:`\mathcal{a}_1\in \mathcal{A}_1` and :math:`\mathcal{a}_2\in
      \mathcal{A}_2`.

   4. The game is not Zero sum as :math:`A \ne -B`.

.. _matching-pennies:

Matching Pennies
****************

Consider two players who can choose to display a coin either Heads facing up or
Tails facing up. If both players show the same face then player 1 wins, if not
then player 2 wins. Winning corresponds to a numeric value of 1 and losing a
numeric value of -1.

.. admonition:: Question
   :class: note

   For the Matching Pennies game:

   1. What is the finite set of players?
   2. What are the action sets?
   3. What are the payoff functions?
   4. Is the game zero sum?

.. admonition:: Answer
   :class: caution, dropdown

   1. There are two players :math:`N=2`.
   2. The action sets are: :math:`\mathcal{A}_1=\mathcal{A}_2=\{\text{Heads}, \text{Tails}\}`
   3. The payoff functions are given by the matrices :math:`A, B` where the
      first row or column corresponds to :math:`\text{Heads}` and the second
      row or column corresponds to :math:`\text{Tails}`.

      ..  math::

          A = \begin{pmatrix}
          1 & -1\\
          -1 & 1
          \end{pmatrix}
          \qquad
          B = \begin{pmatrix}
          -1 & 1\\
          1 & -1
          \end{pmatrix}

      ..  math::

          u_1(\mathcal{a}_1, \mathcal{a}_2) = A_{\mathcal{a}_1, \mathcal{a}_2} \qquad
          u_2(\mathcal{a}_1, \mathcal{a}_2) = B_{\mathcal{a}_1, \mathcal{a}_2}

      where :math:`\mathcal{a}_1\in \mathcal{A}_1` and :math:`\mathcal{a}_2\in
      \mathcal{A}_2`.

   4. The game is Zero sum as :math:`A = -B`.

Exercises
---------

1. Represent the following game in normal form:

       Alice, Bob and Celine are childhood friends that would like to communicate
       online. They have a choice between 3 social networks: facebook, twitter and
       G+.

   Clearly state the players, strategy sets and interpretations of the utilities.

2. Obtain the full game
   representations :math:`(A, B)` for the zero sum games with row play
   payoff matrix given by:

   1. :math:`A =\begin{pmatrix}1 & 3\\ -1 & 4\end{pmatrix}`
   2. :math:`A =\begin{pmatrix}1 & -2\\ -1 & 2\end{pmatrix}`
   3. :math:`A =\begin{pmatrix}1 & -2 & 4\\ 2 & -1 & 2\\ 7 & -7 & 6\end{pmatrix}`

3. Consider the game described as follows:

       An airline loses two suitcases belonging to two different
       travelers. Both suitcases have the same value. An airline manager
       tasked to settle the claims of both travelers explains that the
       airline is liable for a maximum of £5 per suitcase.

   
   To determine an honest appraised value of the suitcases, the
   manager separates both travelers and asks them to write down the
   amount of their value at no less than £2 and no larger than £5 (to
   the single dollar):

   -  If both write down the same number, that number as the true
      dollar value of both suitcases and reimburse both travelers
      that amount.
   -  However, if one writes down a smaller number than the other,
      this smaller number will be taken as the true dollar value, and
      both travelers will receive that amount along with a
      bonus/malus: £2 extra will be paid to the traveler who wrote
      down the lower value and a £2 deduction will be taken from the
      person who wrote down the higher amount.

   Represent this as a Normal Form Game.


Using Nashpy
------------

See :ref:`how-to-create-a-normal-form-game` for guidance of how to use Nashpy to
create a Normal form game.
