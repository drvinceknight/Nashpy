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

   \begin{align*}
       f_1 = & \frac{2 (v_1 - 1) + 1 v_2}{N - 1}\\
       f_2 = & \frac{3 v_1 + 1 (v_2 - 1)}{N - 1}
   \end{align*}

Note that :math:`f_i` is dependent on :math:`v`.

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

First defined in [Moran1958]_ the Moran process assumes a constant population of
:math:`N` individuals which can be of :math:`m` different types. There exists a
fitness function :math:`f:[1, \dots, m] \times [1, \dots, m] ^ N \to \mathbb{R}`
that maps each individual to a numeric fitness value which is dependent on the
types of the individuals in the population.

The process is defined as follows, at each step:

1. Every individual :math:`k` has their fitness :math:`f_k` calculated.
2. An individual is randomly selected for copying. This selection is done
   proportional to their fitness: :math:`f_k(v)`. Thus, the probability of selecting
   individual :math:`k` for copying is given by:

   .. math::

      \frac{f_k(v)}{\sum_{h=1^N}f_h(v)}

3. An individual is selected for removal. This selection is done uniformly
   randomly. Thus, the probability of selecting individual :math:`i` for removal
   is given by:

   .. math::

      1 / N

4. An individual of the same type as the individual selected for copying is
   introduced to the population.
5. The individual selected for removal is removed.

The process is repeated until there is only one type of individual left in the
population.

Fitness function on a game
**************************

A common representation of the fitness function :math:`f` is to use a game.

As an example consider a population with :math:`N=10` and :math:`m=3` types of
individuals. The fitness of a given individual is calculated by considering the
utilities received by each individual when they interact with all other
individuals. These interactions are given by the :math:`3\times 3` matrix
:math:`A`:

.. math::

   A = \begin{pmatrix}
            3 & 2 & 1\\
            1 & 3 & 2\\
            2 & 1 & 3
       \end{pmatrix}

:math:`A_{ij}` represents the utility of an individual of type :math:`i`
interacting with an individual of type :math:`j`.

In this setting, the fitness of an individual of type :math:`i` is:

.. math::

   f_i(v) = (v_{i} - 1)A_{ii} + \sum_{j\ne i, j=1}^{N}v_jA_{ij}

For example, if :math:`v=(4, 5, 1)` then the fitness of individuals of each type
are given by:

1. Individuals of the first type:

   .. math::

      3 \times 3 + 5 \times 2 + 1 \times 1 = 20

2. Individuals of the second type:

   .. math::

      4 \times 3 + 4 \times 1 + 1 \times 2 = 18

3. Individuals of the third type:

   .. math::

      0 \times 3 + 4 \times 2 + 5 \times 1 = 13

Selection probabilities on a game
*********************************

The probability of selecting an individual of type :math:`i` for copying
is given by:


.. math::

   \frac{v_{i}\times\left((v_{i} - 1)A_{ii} + \sum_{j\ne i, j=1}^{N}v_jA_{ij}\right)}
        {\sum_{i=1}^mv_{i}\times\left((v_{i} - 1)A_{ii} + \sum_{j\ne i, j=1}^{N}v_jA_{ij}\right)}

So for this :math:`3\times 3` example, the probability of selecting an
individual of each type for copying is given by:


1. Individuals of the first type:

   .. math::

      \frac{4 \times 20}{4 \times 20 + 5 \times 18 + 1 \times 13} = \frac{80}{183}

2. Individuals of the second type:

   .. math::

      \frac{5 \times 18}{4 \times 20 + 5 \times 18 + 1 \times 13} = \frac{90}{183}

3. Individuals of the third type:

   .. math::

      \frac{1 \times 13}{4 \times 20 + 5 \times 18 + 1 \times 13} = \frac{13}{183}

.. admonition:: Question
   :class: note

   For the :ref:`hawk dove game <motivating-example-moran-process>`
   what are the probabilities of selecting an individual for copying and for
   removal for the following populations:

   1. :math:`v=(4, 5)`
   2. :math:`v=(3, 0)`
   3. :math:`v=(6, 6)`

.. admonition:: Answer
   :class: caution, dropdown

   1. For :math:`v=(4, 5)` the probabilities are given by:

   +------------------+-----------------------------------------------------------------------------------------------------------------+----------------------------------+
   | Type             | Copying                                                                                                         | Removal                          |
   +==================+=================================================================================================================+==================================+
   |        Sharing   |  :math:`\frac{4(3\times 2 + 5 \times 1)}{4(3\times 2 + 5 \times 1) + 5(4\times 3 + 4 \times 0)}=\frac{44}{104}` |  :math:`4 / 9`                   |
   +------------------+-----------------------------------------------------------------------------------------------------------------+----------------------------------+
   |        Aggresive |  :math:`\frac{5(4\times 3 + 4 \times 0)}{4(3\times 2 + 5 \times 1) + 5(4\times 3 + 4 \times 0)}=\frac{60}{104}` |  :math:`5 / 9`                   |
   +------------------+-----------------------------------------------------------------------------------------------------------------+----------------------------------+

   2. For :math:`v=(3, 0)` the probabilities are given by:

   +------------------+-----------------------------------------------------------------------------------------------------------------+----------------------------------+
   | Type             | Copying                                                                                                         | Removal                          |
   +==================+=================================================================================================================+==================================+
   |        Sharing   |  :math:`1`                                                                                                      |  :math:`1`                       |
   +------------------+-----------------------------------------------------------------------------------------------------------------+----------------------------------+
   |        Aggresive |  :math:`0`                                                                                                      |  :math:`0`                       |
   +------------------+-----------------------------------------------------------------------------------------------------------------+----------------------------------+

   3. For :math:`v=(6, 6)` the probabilities are given by:

   +------------------+-----------------------------------------------------------------------------------------------------------------+----------------------------------+
   | Type             | Copying                                                                                                         | Removal                          |
   +==================+=================================================================================================================+==================================+
   |        Sharing   | :math:`\frac{6(5\times 2 + 6 \times 1)}{6(5\times 2 + 6 \times 1) + 6(6\times 3 + 5 \times 0)}=\frac{96}{204}`  |  :math:`6/12=1 / 2`              |
   +------------------+-----------------------------------------------------------------------------------------------------------------+----------------------------------+
   |        Aggresive | :math:`\frac{6(6\times 3 + 5 \times 0)}{6(5\times 2 + 6 \times 1) + 6(6\times 3 + 5 \times 0)}=\frac{108}{204}` |  :math:`6/12=1 / 2`              |
   +------------------+-----------------------------------------------------------------------------------------------------------------+----------------------------------+


The Moran process with mutation
-------------------------------

The Moran process can be modified to allow for mutation. When a new individual
is selected for copying, there is a :math:`p` probability that they mutate to a
another type from the original population (even if they are no longer present in
the population.

The following plot shows 4 possible outcomes of the Moran process of :ref:`the
Hawk Dove game <motivating-example-moran-process>` with a probability of
mutation of :math:`p=.2`. Note that as opposed to the numerical simulations
without mutation, the process does not terminate as new types of individuals can
always enter the population.

.. plot::

   import matplotlib.pyplot as plt
   import nashpy as nash
   import numpy as np

   A = np.array([[2, 1], [3, 0]])
   game = nash.Game(A)
   initial_population = [0, 0, 0, 0, 1]
   mutation_probability = .2
   plt.figure()
   for seed in (0, 2, 4, 6):
       np.random.seed(seed)
       generations = game.moran_process(initial_population=initial_population, mutation_probability=mutation_probability)
       plt.plot(list(map(sum, (next(generations) for _ in range(15)))), label=f"Random seed={seed}")
   plt.ylabel("Count of aggressive animals")
   plt.xlabel("Generations")
   plt.legend()

The Moran process with 2 types of individuals
---------------------------------------------

When considering a Moran process on 2 types of individuals the fitness function
is defined by
:math:`A` which is, in this case is a 2 by 2 matrix.

In the case of a only two types of individuals, the population vector :math:`v`
can be replaced by an integer :math:`n` which represents the number of
individuals of the first type. The number of individuals of the second type is
then given by :math:`N - n`.

.. <!--alex ignore death-->

In this case the random process is a specific type of process called a birth
death process:

- A set of possible states: :math:`S = \{0, 1, \dots, N\}`
- Two absorbing states: :math:`0` and `N`.
- Probabilities :math:`p_{ij}` of going from state :math:`i` to :math:`j`
  defined by:

    - :math:`p_{i, i + 1} + p_{i, i - 1} \leq 1` for :math:`1\leq i \leq N - 1`.
    - :math:`p_{ii} = 1 - p_{i, i + 1} - p_{i, i - 1}` for :math:`1\leq i \leq N - 1`.
    - :math:`p_{00} = p_{NN} = 1`.

Fixation probability
********************

The probability of starting in state :math:`i` and the process ending in state
:math:`N` is denoted by :math:`x_i`.

The probability of a single individual of the first type being able to take over
the population is denoted by :math:`\rho` and :math:`\rho=x_1`.

Given a birth death process, the probability :math:`x_i` is given by:

.. math::

   x_i=\frac{1+\sum_{j=1}^{i-1}\prod_{k=1}^j\gamma_k}{1+\sum_{j=1}^{N-1}\prod_{k=1}^j\gamma_k}

where:

.. math::

   \gamma_k = \frac{p_{k,k-1}}{p_{k,k+1}}

The proof of this result is omitted here but it allows for the specific case of
the Moran process to be obtained:

The transition probabilities are then given by:

.. math::

   \begin{align*}
       p_{i,i+1}&=\frac{if_{1}(i)}{if_{1}(i) + (N-i)f_{2}(i)}\frac{N-i}{N}\\
       p_{i,i-1}&=\frac{(N-i)f_{2}(i)}{if_{1}(i) + (N-i)f_{2}(i)}\frac{i}{N}
   \end{align*}

which gives:

.. math::

   \begin{align*}
       \gamma_i&=\frac{p_{i, i - 1}}{p_{i, i +1}}\\
               &=\frac{\frac{(N-i)f_{2}(i)}{if_{1}(i) + (N-i)f_{2}(i)}\frac{i}{N}}
                      {\frac{if_{1}(i)}{if_{1}(i) + (N-i)f_{2}(i)}\frac{N-i}{N}}\\
               &=\frac{(N-i)f_{2}(i)\frac{i}{N}}
                      {if_{1}(i)\frac{N-i}{N}}\\
               &=\frac{f_{2}(i)}{f_{1}(i)}
   \end{align*}

Thus, the formula for :math:`x_i` in the general birth death process can be used
to obtain the fixation probability :math:`\rho=x_1`.

.. admonition:: Question
   :class: note

   For the :ref:`hawk dove game <motivating-example-moran-process>`
   obtain :math:`\rho` for the following population sizes:

   1. :math:`N=2`
   2. :math:`N=3`
   3. :math:`N=4`

.. admonition:: Answer
   :class: caution, dropdown

   In the case of the hawk dove game we have:

    .. math::

       \begin{align*}
           f_{1}(i) &= 2(i - 1)+1\times (N - i)=N + i - 2\\
           f_{2}(i) &= 3i\\
       \end{align*}

    1. For N = 2 we have:

        +------------------+--------------+
        |                  | :math:`i=1`  |
        +==================+==============+
        | :math:`f_{1}(i)` |      1       |
        +------------------+--------------+
        | :math:`f_{2}(i)` |      3       |
        +------------------+--------------+
        | :math:`\gamma_i` |      3       |
        +------------------+--------------+

       Thus:

       .. math::

          \rho = \frac{1}{1 + 3} = \frac{1}{4}

    2. For N = 3 we have:

        +------------------+--------------+--------------+
        |                  | :math:`i=1`  | :math:`i=2`  |
        +==================+==============+==============+
        | :math:`f_{1}(i)` |  1 + 1 = 2   |   1 + 2 = 3  |
        +------------------+--------------+--------------+
        | :math:`f_{2}(i)` |     3        |       6      |
        +------------------+--------------+--------------+
        | :math:`\gamma_i` |      3/2     |     6/3=2    |
        +------------------+--------------+--------------+

       Thus:

       .. math::

          \rho = \frac{1}{1 + 3/2 + 3/2 \times 2}=\frac{1}{11/2}=\frac{2}{11}

    3. For N = 4 we have:

        +------------------+--------------+--------------+--------------+
        |                  | :math:`i=1`  | :math:`i=2`  | :math:`i=3`  |
        +==================+==============+==============+==============+
        | :math:`f_{1}(i)` |  2 + 1 = 3   |   2 + 2 = 4  |   2 + 3 = 5  |
        +------------------+--------------+--------------+--------------+
        | :math:`f_{2}(i)` |      3       |       6      |      9       |
        +------------------+--------------+--------------+--------------+
        | :math:`\gamma_i` |      1       |    6/4=3/2   |      9/5     |
        +------------------+--------------+--------------+--------------+

       Thus:

       .. math::

          \rho = \frac{1}{1 + 1 + 1\times 3/2 + 1\times3/2\times9/5}=\frac{1}{62/10}=\frac{5}{31}

    Below is a the fixation probability :math:`\rho` for more values of :math:`N`

    .. plot::

       import matplotlib.pyplot as plt
       import nashpy as nash
       import numpy as np

       def theoretic_fixation(N, A, i=1):
           """
           Calculate x_i as given by the theoretic formula
           """
           f_ones = np.array([(A[0, 0] * (i - 1) + A[0, 1] * (N - i)) for i in range(1, N)])
           f_twos = np.array([(A[1, 0] * i + A[1, 1] * (N - i - 1)) for i in range(1, N)])
           gammas = f_twos / f_ones
           return (1 + np.sum(np.cumprod(gammas[:i-1]))) / (1 + np.sum(np.cumprod(gammas)))

       def approximate_fixation(N, A, i=None, repetitions=10):
           """
           Repeat the Moran process and calculate the fixation probability

           This is done by carrying out the following steps:

           1. Creating a game
           2. Building an initial population with i individuals
              of the first type
           3. Getting the fixation probabilities of both types
           4. Returning the probability of the first type
           """
           game = nash.Game(A)
           initial_population = i * [0] + (N - i) * [1]
           probabilities = game.fixation_probabilities(
               initial_population=initial_population,
               repetitions=repetitions
           )

           return probabilities[tuple(0 for _ in range(N))]

       A = np.array([[2, 1], [3, 0]])
       np.random.seed(0)
       N_values = range(2, 16)
       repetitions = 100
       probabilities = [approximate_fixation(N, i=1, A=A, repetitions=repetitions) for N in N_values]
       plt.scatter(N_values, probabilities, label=f"Simulated over {repetitions} repetitions")
       plt.plot(N_values, [theoretic_fixation(N=N, i=1, A=A) for N in N_values], label="Theoretic")
       plt.ylim(0, 1)
       plt.xlabel("$N$")
       plt.ylabel(r"$\rho$")
       plt.legend();

Exercises
---------

1. For the following games, obtain the fixation probability :math:`x_1`
   for :math:`N=4`:

   1. :math:`A=\begin{pmatrix}1 & 1 \\ 1 & 1\end{pmatrix}`
   2. :math:`A=\begin{pmatrix}1 & 2 \\ 3 & 1\end{pmatrix}`

2. Consider the game
   :math:`A=\begin{pmatrix}r & 1 \\ 1 & 1\end{pmatrix}` for :math:`r>1`
   and :math:`N`, and obtain :math:`x_1` as a function of :math:`r`. How
   does :math:`r` effect the chance of fixation?
3. Prove the theorem for fixation probabilities in a birth
   death process (a Moran process with 2 types).

Using Nashpy
------------

See :ref:`how-to-use-moran_process` for guidance of how to use Nashpy to obtain
numerical simulations of the Moran process. See
:ref:`how-to-obtain-fixation-probabilities` for guidance of how to use Nashpy to
obtain approximations of the fixation probabilities. This is what is used to
obtain all the plots above.
