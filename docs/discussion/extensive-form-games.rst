.. _extensive-form-games-discussion:

Extensive Form Games
====================

.. _motivating-example-modified-coordination-game:

Motivating example: A modification of the Coordination Game
-----------------------------------------------------------

Consider the :ref:`Coordination game <motivating-example-coordination-game>`
with the modification that Alice and Bob have more information available to
them: Alice decides where they are going and then lets Bob know before Bob makes
their own choice.

This can be represented pictorially as follows:

.. image:: /_static/discussion/extensive-form-games/main.png

.. _definition-of-extensive-form-game:

Definition of an Extensive Form Game
------------------------------------

An extensive form game consists of:

- A finite set of players :math:`\mathcal{N}`.
- A tree: :math:`G = (V, E, x ^ 0)` where: :math:`V` is the set of vertices,
  :math:`E` the set of edges and :math:`x ^ 0 \in V` is the root of the tree.
- :math:`(V_i)_{i \in \mathcal{N}}` is a partition of the set of vertices that
  are not leaves.
- :math:`O` is the set of possible game outcomes.
- :math:`u` is a function mapping every leaf of :math:`G` to an element of
  :math:`0`.

.. admonition:: Question
   :class: note

   For the :ref:`modified coordination game <motivating-example-modified-coordination-game>`:

   1. What is the finite set of players :math:`\mathcal{N}`?
   2. What the elements :math:`G = (V, E, x ^ 0)`?
   3. What is the partition :math:`(V_i)_{i \in \mathcal{N}}`?
   4. What is the set of possible game outcomes :math:`O`?
   5. What is the mapping :math:`u` from every leaf of :math:`G` to an element
      of :math:`O`?

.. admonition:: Answer
   :class: caution, dropdown

   1. The set :math:`\mathcal{N}` has two players: Alice and Bob.
   2. The tree is given by:

      .. math::

         V = \{A, B_1, B_2, O_1, O_2, O_3, O_4\}

      .. math::

         E = \{(A, B_1), (A, B_2), (B_1, O_1), (B_1, O_2), (B_2, O_3), (B_2, O_4)\}

      .. math::

         x ^ 0 = A

   3. The partition of of non leaf vertices is given by:

      ..  math::

          V_{\text{Alice}} = \{A_1\} \qquad V_{\text{Bob}} = \{B_1, B_2\}

    4. The set of possible game ouctomes :math:`O = \{(3,2), (1, 1), (0, 0), (2, 3)\}`.
    5. The mapping :math:`u` is given by:

      ..  math::

          u(O_1) = (3, 2) \qquad u(O_2) = (1, 1) \qquad u(O_3) = (0, 0) \qquad u(O_4) = (2, 3)

.. _equivalence-of-extensive-and-normal-form-games:

Imperfect information
---------------------

The modified coordination game described :ref:`here
<motivating-example-modified-coordination-game>` differs from the example given
in the :ref:`normal for game chapter <motivating-example-coordination-game>` in
that Bob knows what action is chosen by Alice.

To represent imperfect information we can partition the vertices of a game tree
to indicate which vertices have the same information.

This can be represented pictorially as follows:

.. image:: /_static/discussion/extensive-form-games-with-imperfect-information/main.png

This indicates that Bob makes a decision at both nodes in :math:`\{B_1, B_2\}`
without knowing at which of the two vertices they are. The set :math:`\{B_1,
B_2\}` is called an information set.

Definition of an information set
--------------------------------

Given a game in extensive form:
:math:`(\mathcal{N}, G, (V_i)_{i\in \mathcal{N}}, O, u)`
the set of information sets :math:`v_i` of player :math:`i \in \mathcal{N}` is a partition of
:math:`V_{i}`.
Each element of :math:`v_i`
denotes a set of nodes at which a player is unable to distinguish when
choosing an action.

This implies that:

- Every information set contains vertices for a single player.
- All vertices in an information set must have the same number of successors
  (with the same action labels).

.. admonition:: Question
   :class: note

   For the following games with :math:`\mathcal{N} = \{\text{Alice},
   \text{Bob}\}`, assume that decision nodes :math:`A_i` are Alice's and
   :math:`B_i` are Bob's. Obtain all information sets:

   1. .. image:: /_static/discussion/extensive-form-games/main.png
   2. .. image:: /_static/discussion/extensive-form-games-with-imperfect-information/main.png
   3. .. image:: /_static/discussion/extensive-form-game-example-with-perfect-information/main.png
   4. .. image:: /_static/discussion/extensive-form-game-example-with-imperfect-information/main.png
   5. .. image:: /_static/discussion/extensive-form-game-incoherent-example-with-imperfect-information/main.png

.. admonition:: Answer
   :class: caution, dropdown

   1. :math:`v_{\text{Alice}}=\{\{A\}\}` :math:`v_{\text{Bob}}=\{\{B_1\}, \{B_2\}\}`
   2. :math:`v_{\text{Alice}}=\{\{A\}\}` :math:`v_{\text{Bob}}=\{\{B_1, B_2\}\}`
   3. :math:`v_{\text{Alice}}=\{\{A_1\}, \{A_2\}\}` :math:`v_{\text{Bob}}=\{\{B_1\}, \{B_2\}\}`
   4. :math:`v_{\text{Alice}}=\{\{A_1\}, \{A_2\}\}` :math:`v_{\text{Bob}}=\{\{B_1, B_2\}\}`
   5. This game has incoherent information sets: the two vertices :math:`B_1` and
      :math:`B_2` have different actions.

Definition of a strategy in an extensive form game
--------------------------------------------------

A strategy for a player in an extensive form is collection of probability
distribution over the action set of each information set.

Equivalence of Extensive and Normal Form Games
----------------------------------------------

A game in extensive form can be mapped to a game in normal form by enumerating
all possible strategies that indicate single actions at each information set.
This set of possible strategies corresponds to the actions in the normal form
game.

These strategies can be thought of as vectors in the space of the cross product
of the sets of actions available at every information set.
For player :math:`i\in \mathcal{N}` with information sets :math:`v_i=((v_i)_1,
(v_i)_2, \dots, (v_i)_n)` a strategy :math:`s=(s_1, s_2, \dots, s_n` indicates
what action to take at each information set. So :math:`s_2` will prescribe which
action to take at all vertices contained in :math:`(v_i)_2`.


As an example consider the
:ref:`modified coordination game <motivating-example-modified-coordination-game>`.
The full enumeration of strategies that indicate single actions for Alice is:

.. math::

   \mathcal{A}_1 = \{(\text{Sports}), (\text{Comedy})\}

The full enumeration of strategies that indicate single actions for Bob is:

.. math::

   \mathcal{A}_2 = \{(\text{Sports}, \text{Sports}), (\text{Sports}, \text{Comedy}), (\text{Comedy}, \text{Sports}), (\text{Comedy}, \text{Comedy})\}

So :math:`(\text{Sports}, \text{Comedy})` indicates to choose Sports at
:math:`B_1` and Comedy at :math:`B_2`.

Using this enumeration the payoff functions can be given by the matrices
:math:`A, B`:

.. math::

   A = \begin{pmatrix}
   3  & 3 & 1 & 1\\
   0  & 2 & 0 & 2\\
   \end{pmatrix}

.. math::

   B = \begin{pmatrix}
   2  & 2 & 1 & 1\\
   0  & 3 & 0 & 3\\
   \end{pmatrix}

.. admonition:: Question
   :class: note

   Obtain the Normal Form Game representation corresponding to

   .. image:: /_static/discussion/extensive-form-games-with-imperfect-information/main.png

.. admonition:: Answer
   :class: caution, dropdown

   The full enumeration of strategies that indicate single actions for Alice is:

   .. math::

      \mathcal{A}_1 = \{(\text{Sports}), (\text{Comedy})\}

   The full enumeration of strategies that indicate single actions for Bob is:

   .. math::

      \mathcal{A}_2 = \{(\text{Sports}), (\text{Comedy})\}

   This is because there is a single information set for Bob.

   Using this enumeration the payoff functions can be given by the matrices
   :math:`A, B`:

   .. math::

      A = \begin{pmatrix}
      3 & 1\\
      0 & 2\\
      \end{pmatrix}

   .. math::

      B = \begin{pmatrix}
      2 & 1\\
      0 & 3\\
      \end{pmatrix}

Using Nashpy
------------

See :ref:`how-to-use-support-enumeration` for guidance of how to use Nashpy to
use support enumeration to find Nash equilibria once a Normal Form game
representation has been obtained.
