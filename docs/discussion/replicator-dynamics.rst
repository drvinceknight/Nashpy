.. _replicator-dynamics:

Replicator dynamics
===================

.. _motivating-example-replicator-dynamics:

Motivating example: The Hawk Dove Game
--------------------------------------

Consider a population of animals. These animals when they interact will always
share their food. Due to a genetic mutation, some of these animals may act in an
aggressive manner and not share their food. If two aggressive animals meet they
both fight and end up with no food. If an aggressive animal meets a sharing one,
the aggressive one will take most of the food.

These interactions can be represented using the matrix
:math:`A`:

.. math::

   A = \begin{pmatrix}
       2 & 1\\
       3 & 0
   \end{pmatrix}

In this scenario: what is the likely long term effect of the genetic mutation?

Over time will:

- The population reject the mutation and all the animals continue to share their
  food.
- The population get taken over by the mutation and all animals become
  aggressive.
- A mix of animals are present in the population some act aggressively and some
  share.


.. _definition-of-the-replicator-dynamics-equation:

The replicator dynamics equation
--------------------------------

Stability of the replicator dynamics equation
---------------------------------------------

Mutated populations
-------------------

Evolutionary stable strategies
------------------------------

Using Nashpy
------------

See :ref:`how-to-use-replicator-dynamics` for guidance of how to use Nashpy to
obtain numerical solutions of the replicator dynamics equation.
