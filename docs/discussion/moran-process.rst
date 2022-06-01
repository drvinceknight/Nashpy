.. _moran-process:

Moran Processes
===============

.. _motivating-example-moran-process:

Motivating example: The Hawk Dove Game
--------------------------------------

Consider a **finite** population of :math:`N` animals. Similarly to :ref:`the
motivating example for replicator dynamics
<motivating-example-replicator-dynamics>`, these animals when they interact will
always share their food. Due to a genetic mutation, some of these animals may
act in an aggressive manner and not share their food. If two aggressive animals
meet they both compete and end up with no food. If an aggressive animal meets a
sharing one, the aggressive one will take most of the food.

The difference with a replicator dynamics model is that it will be assumed that
the size of the population is finite and stays constant.

These interactions can be represented using the matrix
:math:`A`:

.. math::

   A = \begin{pmatrix}
       2 & 1\\
       3 & 0
   \end{pmatrix}

In this scenario: what is the probability that the mutation takes over the
entire population?

To answer this question we will assume a vector :math:`v` represents the
population. In this case:

- :math:`v_1` represents the number of individuals of the population that share.
- :math:`v_2` represents the number of individuals of the population that act aggressively.

Note that as the size of the population is assumed to be constant this implies
that:

.. math::

   \sum_i x_i = N

Where :math:`N` is the number of individuals in the population.

The overall fitness of an individual of a given type in a population :math:`v`
is then given by the expected utility (as given by :math:`A`) of individuals of
that type as they interact with the population:

.. math::

   \begin{align}
       f_1 = & \frac{2 (v_1 - 1) + 1 v_2}{N - 1}\\
       f_2 = & \frac{3 v_1 + 1 (v_2 - 1)}{N - 1}
   \end{align}

The evolutionary process defined in this chapter will assume an individual will
be selected for copy proportional to their fitness. The probability of picking
an individual of a given type :math:`i` is thus given by:

.. math::

   \frac{v_i f_i}{v_1 f_1 + v_2 f_2}

To ensure the population stays constant this requires that an individual is
chosen to be removed. This is done uniformly randomly. The probability of
picking an individual of a given type :math:`i` for removal is then given by:

.. math::

   \frac{v_i}{v_1 + v_2}

These probabilities allow us to define a Markov process that describes
the evolution of the system. Here is a diagram showing the different states in
the process for :math:`N=5`.

.. mermaid::

   stateDiagram-v2
       direction LR
       s1: (1, 4)
       s2: (2, 3)
       s3: (3, 2)
       s4: (4, 1)

       s1 --> s2
       s2 --> s1

       s2 --> s3
       s3 --> s2

       s3 --> s4
       s4 --> s3

       note left of s1
           (0, 5)
       end note

       note right of s4
           (5, 0)
       end note

The answer to our question corresponds to the probability that starting in state
:math:`v=(4, 1)`, we arrive at state :math:`v=(0, 5)`.

The following plot shows 4 possible outcomes. In 2 of them the sharing animals
resist the invasion of the aggressive one.

.. plot::

   import matplotlib.pyplot as plt
   import nashpy as nash
   import numpy as np

   A = np.array([[2, 1], [3, .0]])
   game = nash.Game(A)
   initial_population = [0, 0, 0, 0, 1]
   plt.figure()
   for seed in (0, 2, 4, 6):
       np.random.seed(seed)
       generations = game.moran_process(initial_population=initial_population)
       plt.plot(list(map(sum, generations)), label=f"Random seed={seed}")
   plt.ylabel("Count of aggressive animals")
   plt.xlabel("Generations")
   plt.legend()

.. _definition-of-the-moran-process:

The Moran process
-----------------

The Moran process with mutation
-------------------------------


The Moran process with 2 types of individuals
---------------------------------------------

Using Nashpy
------------

See :ref:`how-to-use-moran_process` for guidance of how to use Nashpy to obtain
numerical simulations of the Moran process. See
:ref:`how-to-obtain-fixation-probabilities` for guidance of how to use Nashpy to
obtain approximations of the fixation probabilities. This is what is used to
obtain all the plots above.
