.. _cooperation-discussion:

The Emergence of Cooperation
============================

.. _motivating-example-cooperation:

Motivating example: can cooperation emerge in a short time frame?
-----------------------------------------------------------------

The repeated :ref:`Prisoners Dilemma <prisoners-dilemma>` is a model of direct
reciprocity.

.. math::

   A = \begin{pmatrix}
       3 & 0\\
       5 & 1
   \end{pmatrix}

1. The first action corresponds to acting in the interest of all individuals
   (this is often referred to as Cooperate).
2. The second action corresponds to acting in ones own self interest (this is
   often referred to as Defect).

In a population of individuals, is it possible for self interest to not become
the norm?

To answer this question we can consider the Iterated Prisoners Dilemma as a
:ref:`repeated game <repeated-games-discussion>` where individuals have **two**
consecutive interactions. The incentive to initially acting selflessly is that
the other individual will do the same in the second interaction.

Recalling :ref:`definition-of-strategies-in-repeated-games` the strategies in
this case must map histories of play to actions. The possible histories of play
are:

.. math::

   \mathcal{H} = \{(\emptyset, \emptyset), (r_1, c_1), (r_1, c_2), (r_2, c_1),
   (r_2, c_2)\}

Row strategies are thus of the form:

Cooperate unconditionally:

.. math::

   \begin{align*}
       (\emptyset, \emptyset) &\to r_1\\
       (r_1, c_1) &\to r_1\\
       (r_1, c_2) &\to r_1\\
       (r_2, c_1) &\to r_1\\
       (r_2, c_2) &\to r_1\\
   \end{align*}

Defect unconditionally:

.. math::

   \begin{align*}
       (\emptyset, \emptyset) &\to r_2\\
       (r_1, c_1) &\to r_2\\
       (r_1, c_2) &\to r_2\\
       (r_2, c_1) &\to r_2\\
       (r_2, c_2) &\to r_2\\
   \end{align*}

Start by cooperating and then repeat the action of the opponent:

.. math::

   \begin{align*}
       (\emptyset, \emptyset) &\to r_1\\
       (r_1, c_1) &\to r_1\\
       (r_1, c_2) &\to r_2\\
       (r_2, c_1) &\to r_1\\
       (r_2, c_2) &\to r_2\\
   \end{align*}

The strategy space when repeating the game **twice** corresponds to 32 different
strategies. We can see how these 32 strategies interact in an evolutionary
setting using :ref:`replicator dynamics <replicator-dynamics-discussion>`.

.. plot::

   import matplotlib.pyplot as plt
   import nashpy as nash
   import nashpy.repeated_games
   import numpy as np

   pd = np.array([[3, 0], [5, 1]])
   stage_game = nash.Game(pd, pd.T)
   ipd = nash.repeated_games.obtain_repeated_game(game=stage_game, repetitions=2)
   A, _ = ipd.payoff_matrices

   timepoints = np.linspace(0, 25, 500)
   xs = ipd.replicator_dynamics(timepoints=timepoints)

   fig, axarr = plt.subplots(nrows=1, ncols=2, figsize=(8, 3))

   ax = axarr[0]
   for i, x in enumerate(zip(*xs)):
       if x[-1] > 10 ** -2:
           ax.plot(x, label=f"{i}")
       else:
           ax.plot(x)
   ax.set_ylim(0, 1)
   ax.set_title("Evolution of IPD strategies")
   ax.set_xlabel("Time")
   ax.set_ylabel("Population proportion")
   ax.legend()

   ax = axarr[1]
   ax.plot(np.sum([x * (A @ x) / 2 for x in xs], axis=1))
   ax.set_ylim(0, 5)
   ax.set_xlabel("Time")
   ax.set_title("Average per turn utility")

   fig.tight_layout()


The legend shows the index in the strategy space of the strategies that have a
final proportion larger than :math:`10 ^ {-2}`. The average utility plot gives
us the answer to our question: the average per turn utility is 1 which implies
that the strategies that survive the evolutionary process are the ones that act
selfishly.

The immediate conclusion is somewhat disappointing: how can a society emerge in
which individuals will do what is best for the collective?

This question can be better answered by considering a much larger strategy space
corresponding to more repetitions of the prisoners dilemma.


The General form of the Prisoners Dilemma
-----------------------------------------

The general form is:


.. math::

   A =
   \begin{pmatrix}
       R & S\\
       T & P
   \end{pmatrix}\qquad
   B =
   \begin{pmatrix}
       R & T\\
       S & P
   \end{pmatrix}

with the following constraints:

.. math::

   T > R > P > S \qquad 2R > T + S

- The first constraint ensures that the second action "Defect" dominates the
  first action "Cooperate".
- The second constraint ensures that a social dilemma arises: the sum of the
  utilities to both players is best when they both cooperate.

This game is a good model of agent (human, etc) interaction: a player can choose
to take a slight loss of utility for the benefit of the other play **and**
themselves.


.. admonition:: Question
   :class: note

   Under what conditions is the following game a Prisoners Dilemma:

   .. math::

      A = \begin{pmatrix}
            1       & -\mu \\
            1 + \mu & 0
          \end{pmatrix}\qquad
      B = A ^ T

.. admonition:: Answer
   :class: caution, dropdown

   This is a Prisoners Dilemma when:

   .. math::

      1 + \mu > 1 \text{ and } 0 > - \mu

   and:

   .. math::

      2 > 1

   Both of these equations hold for :math:`\mu>0`. This is a convenient form for
   the Prisoners Dilemma as it corresponds to a 1 dimensional parametrization.

As a single one shot game there is not much more to say about the Prisoner's
dilemma. It becomes fascinating when studied as a repeated game.

Axelrod's tournaments
---------------------

In 1980, Robert Axelrod (a political scientist) invited submissions to a
computer tournament version of an iterated prisoners dilemma. This was described
in a 1980 paper [Axelrod1980]_.

.. <!--alex ignore tit-->

- 14 strategies were submitted.
- Round robin tournament with 200 stages including a 15th player who played
  uniformly randomly.
- Some complicated strategies, including for example a strategy that used a
  :math:`\chi^2` test to try and identify strategies that were acting randomly. You
  can read more about this tournament here:
  http://axelrod.readthedocs.io/en/stable/reference/overview_of_strategies.html#axelrod-s-first-tournament
- The winner (average score) was in fact a straightforward strategy: Tit For Tat.
  This strategy starts by cooperating and then repeats the opponents previous
  move.

The 15 by 15 payoff matrix (rounded to 1 digit) that corresponds to this
tournament is:

.. math::

   \begin{pmatrix}
       3. & 3. & 3. & 3. & 3. & 3. & 3. & 3. & 2.6& 3. & 1.4& 1.1& 1.5& 2.2& 2.2\\
       3. & 3. & 3. & 3. & 3. & 3. & 3. & 3. & 3. & 1.2& 1.3& 1.1& 1.3& 2.8& 2.8\\
       3. & 3. & 3. & 3. & 3. & 3. & 3. & 3. & 2.8& 0.1& 2.2& 2.7& 2.7& 1.6& 1.5\\
       3. & 3. & 3. & 3. & 3. & 3. & 3. & 3. & 3.1& 0.5& 2.1& 2.4& 2.4& 2. & 2.1\\
       3. & 3. & 3. & 3. & 3. & 3. & 3. & 3. & 3.3& 1.3& 1.3& 1.3& 1.4& 2.8& 2.6\\
       3. & 3. & 3. & 3. & 3. & 3. & 3. & 3. & 2.6& 2.5& 1.4& 1.2& 1.7& 2.9& 2.9\\
       3. & 3. & 3. & 3. & 3. & 3. & 3. & 3. & 2. & 1.1& 1.2& 1.1& 1.3& 3. & 3.  \\
       3. & 3. & 3. & 3. & 3. & 3. & 3. & 3. & 2. & 1. & 1.3& 1.1& 1.2& 3. & 2.9\\
       2.6& 2.8& 3.2& 2.7& 1.8& 2.6& 1.4& 1.4& 1.5& 3.1& 1.5& 1.4& 2.1& 2.7& 2.9\\
       3. & 1. & 4.9& 3.3& 1.4& 1.1& 1. & 1.2& 2.7& 1. & 2.2& 2.6& 1.2& 2.7& 2.6\\
       1.4& 1.3& 3.5& 2.8& 1.5& 1.4& 1.2& 1.3& 1.7& 3.5& 1.3& 1.1& 1.3& 2.4& 2.4\\
       1.2& 1.1& 3.2& 2.8& 1.4& 1.2& 1.1& 1.1& 1.5& 3.2& 1.2& 1.2& 1.3& 2.3& 2.3\\
       1.5& 1.3& 3.2& 2.8& 1.6& 1.7& 1.2& 1.1& 2.4& 1. & 1.3& 1.2& 1.4& 2.3& 2.4\\
       2.2& 0.9& 3.9& 2.8& 1.1& 0.8& 0.6& 0.6& 1.2& 1.2& 1.8& 2.1& 2. & 2.3& 2.3\\
       2.3& 0.9& 3.9& 2.7& 1.2& 0.7& 0.5& 0.7& 1. & 1.2& 1.8& 2.1& 2. & 2.3& 2.3
   \end{pmatrix}

We see that the first 8 strategies all cooperate with each other (getting a
utility of 3).

These 15 strategies are a small subset of the strategy space for the iterated
prisoners dilemma with :math:`T=200` repetitions.
As before, we can see how these 15 strategies interact in an evolutionary
setting using :ref:`replicator dynamics <replicator-dynamics-discussion>`.

.. plot::

   import matplotlib.pyplot as plt
   import nashpy as nash
   import numpy as np

   # Payoff matrix obtained by using the Axelrod library and the documentation
   # written here: https://axelrod.readthedocs.io/en/stable/tutorials/running_axelrods_first_tournament/index.html#creating-the-tournament
   A = np.array([
       [3.   , 2.975, 3.   , 3.   , 3.   , 2.975, 3.   , 3.   , 2.625, 2.985, 1.409, 1.14  , 1.469 , 2.217, 2.238 ],
       [3.   , 2.98 , 3.02 , 3.004, 3.   , 2.98 , 3.   , 3.   , 2.975, 1.165, 1.297, 1.076 , 1.325 , 2.824, 2.836 ],
       [3.   , 2.97 , 3.   , 3.   , 3.   , 2.97 , 3.   , 3.   , 2.757, 0.075, 2.22 , 2.658 , 2.718 , 1.57 , 1.52  ],
       [3.   , 2.974, 3.   , 3.   , 3.   , 2.974, 3.   , 3.   , 3.056, 0.472, 2.088, 2.383 , 2.428 , 1.995, 2.129 ],
       [3.   , 2.975, 3.   , 3.   , 3.   , 2.975, 3.   , 3.   , 3.316, 1.285, 1.343, 1.331 , 1.413 , 2.802, 2.648 ],
       [3.   , 2.98 , 3.02 , 3.004, 3.   , 2.98 , 3.   , 3.   , 2.63 , 2.525, 1.375, 1.191 , 1.685 , 2.873, 2.928 ],
       [3.   , 2.975, 3.   , 3.   , 3.   , 2.975, 3.   , 3.   , 2.043, 1.055, 1.173, 1.111 , 1.315 , 3.033, 2.967 ],
       [3.   , 2.975, 3.   , 3.   , 3.   , 2.975, 3.   , 3.   , 2.047, 1.045, 1.271, 1.121 , 1.215 , 3.003, 2.915 ],
       [2.625, 2.775, 3.162, 2.676, 1.846, 2.605, 1.383, 1.382, 1.5  , 3.143, 1.463, 1.371 , 2.064 , 2.74 , 2.892 ],
       [2.985, 1.015, 4.9  , 3.302, 1.36 , 1.1  , 1.005, 1.17 , 2.748, 1.   , 2.22 , 2.646 , 1.19  , 2.67 , 2.582 ],
       [1.434, 1.307, 3.52 , 2.828, 1.458, 1.4  , 1.173, 1.271, 1.723, 3.495, 1.293, 1.136 , 1.315 , 2.414, 2.443 ],
       [1.165, 1.076, 3.228, 2.753, 1.371, 1.216, 1.111, 1.131, 1.451, 3.211, 1.151, 1.1675, 1.27  , 2.293, 2.327 ],
       [1.494, 1.285, 3.188, 2.763, 1.648, 1.71 , 1.21 , 1.145, 2.369, 1.04 , 1.29 , 1.2   , 1.3995, 2.317, 2.374 ],
       [2.227, 0.909, 3.92 , 2.81 , 1.127, 0.803, 0.553, 0.648, 1.18 , 1.225, 1.824, 2.053 , 1.987 , 2.265, 2.279 ],
       [2.258, 0.891, 3.925, 2.704, 1.168, 0.658, 0.537, 0.68 , 0.997, 1.237, 1.833, 2.102 , 1.979 , 2.304, 2.2745]])

   ipd = nash.Game(A, A.T)

   timepoints = np.linspace(0, 25, 500)
   xs = ipd.replicator_dynamics(timepoints=timepoints)

   fig, axarr = plt.subplots(nrows=1, ncols=2, figsize=(8, 3))

   ax = axarr[0]
   for i, x in enumerate(zip(*xs)):
       if x[-1] > 10 ** -2:
           ax.plot(x, label=f"{i}")
       else:
           ax.plot(x)
   ax.set_ylim(0, 1)
   ax.set_title("Evolution of strategies in Axelrod's 1st tournament")
   ax.set_xlabel("Time")
   ax.set_ylabel("Population proportion")
   ax.legend()

   ax = axarr[1]
   ax.plot(np.sum([x * (A @ x) for x in xs], axis=1))
   ax.set_ylim(0, 5)
   ax.set_xlabel("Time")
   ax.set_title("Average per turn utility")

   fig.tight_layout()

It is evident here that cooperation emerges from this strategy space.

The fact that Tit For Tat won garnered a lot of research (still ongoing) as it
showed a mathematical model of how cooperative behaviour can emerge in complex
situations. However, recent research has shown that Tit For Tat is not a
universally strong strategy [Knight2018]_, [Harper2017]_, [Press2012]_.

Exercises
---------


Justify if the following games are Prisoners dilemmas or not:

1. .. math :: 

      A =
        \begin{pmatrix}
        3 & 0\\
        5 & 1
        \end{pmatrix}
        \qquad
      B =
        \begin{pmatrix}
        3 & 5\\
        0 & 1
        \end{pmatrix}

2. .. math:: 

      A =
        \begin{pmatrix}
        1 & -1\\
        2 & 0
        \end{pmatrix}
        \qquad
      B =
        \begin{pmatrix}
        1 & 2\\
        -1 & 0
        \end{pmatrix}
3. .. math::
    
      A =
        \begin{pmatrix}
        1 & -1\\
        2 & 0
        \end{pmatrix}
        \qquad
      B =
        \begin{pmatrix}
        3 & 5\\
        0 & 1
        \end{pmatrix}
4. .. math::

      A =
        \begin{pmatrix}
        6 & 0\\
        12 & 1
        \end{pmatrix}
        \qquad
      B =
        \begin{pmatrix}
        6 & 12\\
        0 & 0
        \end{pmatrix}

Using Python
------------

There is a Python library (:code:`axelrod`) with over 200 strategies that can be
used to reproduce this work [Knight2016]_. You can read the documentation for it
here: http://axelrod.readthedocs.io.
