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

.. image:: /_static/discussion/extensive-form-games_with_imperfect_information/main.png

This indicates that Bob makes a decision at both nodes in :math:`\{B_1, B_2\}`
without knowing at which of the two vertices they are. The set :math:`\{B_1,
B_2\}` is called an information set.

Definition of an information set
--------------------------------

Given a game in extensive form: 
:math:`(\mathcal{N}, G, (V_i)_{i\in \mathcal{N}}, O, u)`

Definition of a strategy in an extensive form game
--------------------------------------------------

Equivalence of Extensive and Normal Form Games
----------------------------------------------

Consider the game given by the tree in the following image:

.. admonition:: Question
   :class: note

   Obtain the Normal Form Game representation corresponding to this game and
   find the Nash equilibria.

.. admonition:: Answer
   :class: caution, dropdown


   Well....


Using Nashpy
------------

See :ref:`how-to-use-support-enumeration` for guidance of how to use Nashpy to
use support enumeration to find Nash equilibria once a Normal Form game
representation has been obtained.
