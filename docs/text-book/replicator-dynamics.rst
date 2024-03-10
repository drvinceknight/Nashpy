.. _replicator-dynamics-discussion:

Replicator dynamics
===================

.. _motivating-example-replicator-dynamics:

Motivating example: The Hawk Dove Game
--------------------------------------

Consider a population of animals. These animals when they interact will always
share their food. Due to a genetic mutation, some of these animals may act in an
aggressive manner and not share their food. If two aggressive animals meet they
both compete and end up with no food. If an aggressive animal meets a sharing one,
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

- The population resist the mutation and all the animals continue to share their
  food.
- The population get taken over by the mutation and all animals become
  aggressive.
- A mix of animals are present in the population some act aggressively and some
  share.

To answer this question we will assume a vector :math:`x` represents the
population. In this case:

- :math:`x_1` represents the proportion of the population that shares.
- :math:`x_2` represents the proportion of the population that acts aggressively.

Note that as the components of :math:`x` are proportions of the population this
implies:

.. math::

   \sum_i x_i = 1

We will also assume that any given individual in the population is playing a
:ref:`strategy <strategies-discussion>` :math:`\chi`, which:

- shares :math:`\chi_1` proportion of the time.
- acts aggressively :math:`\chi_2` proportion of the time.

The overall fitness of an individual in the population is then given by their
expected utility (as given by :math:`A`) as they interact with the population:

.. math::

   \chi A x

We can in fact write down the fitness corresponding to each action (sharing or
being aggressive):

.. math::

   f = A x

The average fitness in the population is then given by:

.. math::

   \phi = x ^ T f

To understand how the population will evolve relative to their fitness the
following differential equation will be used:

.. math::

   \frac{dx_i}{dt} = x_i(f_i - \phi)\text{ for all }i

In our case the differential equations are:

.. math::

   \begin{align*}
       \frac{dx_1}{dt} &= x_1(2x_1 + x_2 - \phi)\\
       \frac{dx_2}{dt} &= x_2(3x_1 - \phi)
   \end{align*}

where:

.. math::

   \phi=x_1(2x_1 + x_2) + x_2(3x_1)

This differential equation can then be :ref:`solved numerically
<how-to-use-replicator-dynamics>` to show the evolution of the population over
time. We can see that it looks like in our particular situation the mutation
stays within the population and a mix of both sharing and aggressive animals
will coexist.

.. plot::

   import matplotlib.pyplot as plt
   import nashpy as nash
   import numpy as np

   A = np.array([[2, 1], [3, 0]])
   game = nash.Game(A)
   y0 = np.array([0.95, 0.05])
   timepoints = np.linspace(0, 10, 1500)
   sharing_population, aggressive_population = game.replicator_dynamics(y0=y0, timepoints=timepoints).T
   plt.plot(sharing_population, label="$x_1$")
   plt.plot(aggressive_population, label="$x_2$")
   plt.ylim(0, 1)
   plt.ylabel("Population proportion")
   plt.xlabel("Time")
   plt.legend()

.. _definition-of-the-replicator-dynamics-equation:

The replicator dynamics equation
--------------------------------

Given a population with :math:`N` types of individuals. Where the fitness of an
individual of type :math:`i` when interacting with an individual of type
:math:`j` is given by :math:`A_{ij}` where :math:`A\in\mathbb{R}^{N \times N}`.
The replicator dynamics equation is given by:

.. math::

   \frac{dx_i}{dt} = x_i(f_i - \phi)\text{ for all }i

where:

.. math::

   \phi = \sum_{i=1} ^ N x_i f_i(x)

where :math:`f_i` is the population dependent fitness of individuals of type
:math:`i`:

.. math::

   f_i(x) = (Ax)_i

Note that there are equivalent linear algebraic definitions to the above:

.. math::

   f = Ax \qquad \phi=x^TAx


.. admonition:: Question
   :class: note

   For :ref:`Rock Paper Scissors <motivating-example-strategy-for-rps>`, what is
   the replicator dynamics equation?

.. admonition:: Answer
   :class: caution, dropdown

   Recalling that rock paper scissors has a payoff matrix :math:`A` given by:

   .. math::

      A = \begin{pmatrix}
          0  & -1 & 1 \\
          1  & 0  & -1\\
          -1 & 1  & 0\\
      \end{pmatrix}

   For a general population vector :math:`x` the population dependent fitness
   :math:`f` is given by:

   .. math::

      f = Ax = \begin{pmatrix}
                   -x_2 + x_3\\
                   x_1 - x_3\\
                   -x_1 + x_2\\
               \end{pmatrix}

   The average fitness is given by:

    .. math::

       \phi = x^T f = x_1(x_3 - x_2) + x_2(x_1 - x_3) + x_3(x_2 - x_1)

   The replicator dynamics equation is then given by:

   .. math::

      \begin{align*}
          \frac{dx_1}{dt} &= x_1(x_3 - x_2 - \phi)\\
          \frac{dx_2}{dt} &= x_2(x_1 - x_3 - \phi)\\
          \frac{dx_3}{dt} &= x_3(x_2 - x_1 - \phi)
      \end{align*}

   Closer inspection of :math:`\phi` gives: :math:`\phi=0` thus:

   .. math::

      \begin{align*}
          \frac{dx_1}{dt} &= x_1(x_3 - x_2)\\
          \frac{dx_2}{dt} &= x_2(x_1 - x_3)\\
          \frac{dx_3}{dt} &= x_3(x_2 - x_1)
      \end{align*}


Stability of the replicator dynamics equation
---------------------------------------------

Stability of the replicator dynamics equation is achieved when
:math:`\frac{dx_i}{dt} = 0` for all :math:`i`.

For a population vector :math:`x^*` for which :math:`\frac{dx^*_i}{dt} = 0` for all
:math:`i` the population will not change without some other effect. This is
referred to as a **stable population**.

.. admonition:: Question
   :class: note

   For the following games, what are the stable populations?

   1. :ref:`Rock Paper Scissors <motivating-example-strategy-for-rps>`

   .. math::

      A = \begin{pmatrix}
          0  & -1 & 1 \\
          1  & 0  & -1\\
          -1 & 1  & 0\\
      \end{pmatrix}

   2. :ref:`Hawk Dove Game <motivating-example-replicator-dynamics>`

   .. math::

      A = \begin{pmatrix}
       2 & 1\\
       3 & 0
      \end{pmatrix}

.. admonition:: Answer
   :class: caution, dropdown

   1. The replicator dynamics equation for this game are:


   .. math::

      \begin{align*}
          \frac{dx_1}{dt} &= x_1(x_3 - x_2)\\
          \frac{dx_2}{dt} &= x_2(x_1 - x_3)\\
          \frac{dx_3}{dt} &= x_3(x_2 - x_1)
      \end{align*}

   For them all to be 0, this requires:

   - :math:`x_1=0` or :math:`x_2=x_3`
   - :math:`x_2=0` or :math:`x_1=x_3`
   - :math:`x_3=0` or :math:`x_1=x_2`

   Which, through inspection in turn requires:

   - :math:`x_1\ne 0` and :math:`x_2=x_3=0` or
   - :math:`x_2\ne 0` and :math:`x_1=x_3=0` or
   - :math:`x_3\ne 0` and :math:`x_1=x_2=0` or
   - :math:`x_1=x_2=x_3`.

   Given that :math:`x_1+x_2+x_3=1` this leaves us with 4 possible stable
   populations:

   1. :math:`x=(1, 0, 0)`
   2. :math:`x=(0, 1, 0)`
   3. :math:`x=(0, 0, 1)`
   4. :math:`x=(1 / 3, 1 / 3, 1 / 3)`

   The following plot shows each of the above populations which no longer change
   over time:

   .. plot::

      import matplotlib.pyplot as plt
      import nashpy as nash
      import numpy as np

      A = np.array([[0, -1, 1], [1, 0, -1], [-1, 1, 0]])
      game = nash.Game(A)
      timepoints = np.linspace(0, 10, 1500)
      fig, axarr = plt.subplots(nrows=2, ncols=2)

      initial_populations = (
          np.array((1, 0, 0)),
          np.array((0, 1, 0)),
          np.array((0, 0, 1)),
          np.array((1/3, 1/3, 1/3)),
      )
      for i, y0 in enumerate(initial_populations):
          rock_populations, paper_populations, scissors_populations = game.replicator_dynamics(y0=y0, timepoints=timepoints).T

          ax = axarr[i % 2, int(i / 2)]
          ax.plot(rock_populations, label="$x_1$")
          ax.plot(paper_populations, label="$x_2$")
          ax.plot(scissors_populations, label="$x_3$")
          ax.set_ylim(-.1, 1.1)
          ax.set_ylabel("Population proportion")
          ax.set_xlabel("Time")
          ax.legend()
      plt.tight_layout()

   2. The replicator dynamics equation for this game are:


    .. math::

       \begin{align*}
           \frac{dx_1}{dt} &= x_1(2x_1 + x_2 - \phi)\\
           \frac{dx_2}{dt} &= x_2(3x_1 - \phi)
       \end{align*}

    where:

    .. math::

       \phi=x_1(2x_1 + x_2) + x_2(3x_1)

    substituting :math:`x_2 = 1 - x_1` here gives:

    .. math::

       \begin{align*}
           \frac{dx_1}{dt} &= x_1(x_1 - 1)(2x_1-1)\\
           \frac{dx_2}{dt} &= -x_1(x_1 - 1)(2x_1-1)
       \end{align*}

   For them both to be 0, this requires:

   - :math:`x_1=0` or
   - :math:`x_1=1` or
   - :math:`x_1=1/2`

   Recalling the substition that :math:`x_2=1 - x_1` this leaves us with 3 possible stable
   populations:

   1. :math:`x=(1, 0)`
   2. :math:`x=(0, 1)`
   3. :math:`x=(1/2, 1/2)`

   The following plot shows each of the above populations which no longer change
   over time:

   .. plot::

      import matplotlib.pyplot as plt
      import nashpy as nash
      import numpy as np

      A = np.array([[2, 1], [3, 0]])
      game = nash.Game(A)
      timepoints = np.linspace(0, 10, 1500)
      fig, axarr = plt.subplots(nrows=1, ncols=3, figsize=(8, 3))

      initial_populations = (
          np.array((1, 0)),
          np.array((0, 1)),
          np.array((1 / 2, 1 / 2)),
      )
      for i, y0 in enumerate(initial_populations):
          sharing_populations, aggressive_populations = game.replicator_dynamics(y0=y0, timepoints=timepoints).T

          ax = axarr[i]
          ax.plot(sharing_populations, label="$x_1$")
          ax.plot(aggressive_populations, label="$x_2$")
          ax.set_ylim(-.1, 1.1)
          ax.set_ylabel("Population proportion")
          ax.set_xlabel("Time")
          ax.legend()
      plt.tight_layout()

Evolutionary stable strategies
------------------------------

Evolutionary stable strategies are strategies that when adopted by an entire
population are resistant to an alternative strategy that is initially rare.

By definition an evolutionary stable strategy corresponds to a stable
population.

For the :ref:`hawk dove game <motivating-example-replicator-dynamics>` there are
3 stable populations:

- :math:`x=(1, 0)`
- :math:`x=(0, 1)`
- :math:`x=(1 / 2, 1 / 2)`

However, if a small deviation is made from the first two populations then the
population does not "resist". For example, we consider the initial population
:math:`x=(1, 0)` and introduce a small population aggressive behaviours to have:
:math:`x = (1 - \epsilon, \epsilon)` where :math:`\epsilon>0`. The plot below
shows this with :math:`\epsilon=10 ^ -5`:

.. plot::

   import matplotlib.pyplot as plt
   import nashpy as nash
   import numpy as np

   A = np.array([[2, 1], [3, 0]])
   game = nash.Game(A)
   epsilon = 10 ** -5
   y0 = np.array([1 - epsilon, epsilon])
   timepoints = np.linspace(0, 10, 10_000)
   sharing_population, aggressive_population = game.replicator_dynamics(y0=y0, timepoints=timepoints).T
   plt.plot(sharing_population, label="$x_1$")
   plt.plot(aggressive_population, label="$x_2$")
   plt.ylim(0, 1)
   plt.ylabel("Population proportion")
   plt.xlabel("Time")
   plt.legend()

This is also what happens if we start with a population of aggressive animals:
We consider the initial population
:math:`x=(0, 1)` and introduce a small population aggressive behaviours to have:
:math:`x = (\epsilon, 1 - \epsilon)` where :math:`\epsilon>0`. The plot below
shows this with :math:`\epsilon=10 ^ {-5}`:

.. plot::

   import matplotlib.pyplot as plt
   import nashpy as nash
   import numpy as np

   A = np.array([[2, 1], [3, 0]])
   game = nash.Game(A)
   epsilon = 10 ** -5
   y0 = np.array([epsilon, 1 - epsilon])
   timepoints = np.linspace(0, 10, 10_000)
   sharing_population, aggressive_population = game.replicator_dynamics(y0=y0, timepoints=timepoints).T
   plt.plot(sharing_population, label="$x_1$")
   plt.plot(aggressive_population, label="$x_2$")
   plt.ylim(0, 1)
   plt.ylabel("Population proportion")
   plt.xlabel("Time")
   plt.legend()

However, this is not the case with the third stable population: :math:`x=(1 / 2,
1 / 2)`. The plot below shows :math:`x=(1 / 2 - \epsilon, 1 / 2 + \epsilon)`
with :math:`\epsilon=10^{-2}`:

.. plot::

   import matplotlib.pyplot as plt
   import nashpy as nash
   import numpy as np

   A = np.array([[2, 1], [3, 0]])
   game = nash.Game(A)
   epsilon = 10 ** -2
   y0 = np.array([1 / 2 - epsilon, 1 / 2 + epsilon])
   timepoints = np.linspace(0, 2, 15)
   sharing_population, aggressive_population = game.replicator_dynamics(y0=y0, timepoints=timepoints).T
   plt.plot(sharing_population, label="$x_1$")
   plt.plot(aggressive_population, label="$x_2$")
   plt.ylim(0, 1)
   plt.ylabel("Population proportion")
   plt.xlabel("Time")
   plt.legend()

These observations can be confirmed analytically. Information on this can be
found in [Fudenberg1998]_, [Webb2007]_ and [Nowak2006]_.

The replicator equations were first presented in [Maynard1974]_.

.. _definition-of-the-replicator-mutation-dynamics-equation:

The replicator-mutation dynamics equation
-----------------------------------------

An extension of the :ref:`replicator equation
<definition-of-the-replicator-dynamics-equation>` is to allow for mutation
[Komarova2004]_. In
this case reproduction is imperfect and individuals of a given type can give
individuals of another.

This is expressed using a matrix :math:`Q` where :math:`Q_{ij}` denotes the
probability of an individual of type :math:`j` is produced by an individual of
type :math:`i`.

In this case the replicator equation can be modified to give the
replicator-mutation equation:

.. math::

   \frac{dx_i}{dt} = \sum_{j=1}^Nx_j f_j Q_{ji}- x_i\phi\text{ for all }i

where, as before:

.. math::

   f = Ax \qquad \phi=x^TAx

This can modify emergent behaviour. For the :ref:`Hawk Dove game
<motivating-example-replicator-dynamics>` if there is a 10% change that
aggressive individuals will produce sharing ones the matrix :math:`Q` is given
by:

.. math::

   Q = \begin{pmatrix}
            1 & 0\\
            1 / 10 & 9 / 10
       \end{pmatrix}

The plot below shows the evolution of the system:

.. plot::

   import matplotlib.pyplot as plt
   import nashpy as nash
   import numpy as np

   A = np.array([[2, 1], [3, 0]])
   Q = np.array([[1, 0], [1 / 10, 9 / 10]])
   game = nash.Game(A)
   y0 = np.array([0.95, 0.05])
   timepoints = np.linspace(0, 10, 1500)
   sharing_population, aggressive_population = game.replicator_dynamics(y0=y0, timepoints=timepoints, mutation_matrix=Q).T
   plt.plot(sharing_population, label="$x_1$")
   plt.plot(aggressive_population, label="$x_2$")
   plt.ylim(0, 1)
   plt.ylabel("Population proportion")
   plt.xlabel("Time")
   plt.legend()

.. admonition:: Question
   :class: note

   Show that for :math:`Q=I_N` (the identity matrix of size :math:`N`)
   the replicator-mutation equation corresponds to the replicator equation.

.. admonition:: Answer
   :class: caution, dropdown

   The replicator-mutation equation is:

   .. math::

       \frac{dx_i}{dt} = \sum_{j=1}^Nx_j f_j Q_{ji}- x_i\phi\text{ for all }i

   As :math:`Q=I_N`:

   .. math::

       Q_{ij} =
        \begin{cases}
            1 & \text{ if } i = j\\
            0 & \text{ otherwise}
        \end{cases}

   This gives:

   .. math::

      \begin{align*}
          \frac{dx_i}{dt} &= x_i f_i Q_{ii}- x_i\phi\text{ for all }i && Q_{ij}=0\text{ for all } i\ne j\\
          \frac{dx_i}{dt} &= x_i f_i - x_i\phi\text{ for all }i && Q_{ii}=1\\
          \frac{dx_i}{dt} &= x_i (f_i - \phi)\text{ for all }i
      \end{align*}

   As required.


Exercises
---------

1. Consider a population with
   two types of individuals: :math:`x=(x_1, x_2)` such that
   :math:`x_1 + x_2 = 1`. Obtain all the stable distribution for the
   system defined by the following fitness functions:

   1. :math:`f_1(x)=x_1 - x_2\qquad f_2(x)=x_2 - 2 x_1`
   2. :math:`f_1(x)=x_1x_2 - x_2\qquad f_2(x)=x_2 - x_1 + 1/2`
   3. :math:`f_1(x)=x_1 ^ 2 \qquad f_2(x)=x_2^2`

2. For the following games, obtain all the stable distributions for the
   evolutionary game:

   1. :math:`A = \begin{pmatrix}2 & 4 \\ 5 & 3\end{pmatrix}`
   2. :math:`A = \begin{pmatrix}1 & 0 \\ 0 & 1\end{pmatrix}`


Using Nashpy
------------

See :ref:`how-to-use-replicator-dynamics` for guidance of how to use Nashpy to
obtain numerical solutions of the replicator dynamics equation. See
:ref:`how-to-use-replicator-dynamics-with-mutation` for guidance of how to use
Nashpy to obtain numerical solutions of the replicator-mutation dynamics
equation.This is what is used to obtain all the plots above.
