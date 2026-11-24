.. _imitation-dynamics:

Imitation Dynamics
==================

An imitate-the-best process models individuals who copy a strategy that has
performed well, rather than calculating a best response from the full game.
Nashpy implements a two-population version for bimatrix games.

Population state
----------------

Consider a game with payoff matrices
:math:`A, B \in \mathbb{R}^{m \times n}` and two populations of size
:math:`N`. At generation :math:`t`, let

.. math::

   P^{r}(t) \in (\Delta_m)^N

denote the row population and let

.. math::

   P^{c}(t) \in (\Delta_n)^N

denote the column population. Thus, :math:`P_i^r(t)` and :math:`P_i^c(t)`
are mixed strategies for the individuals at position :math:`i`.

Each initial mixed strategy is sampled from a uniform Dirichlet distribution
on the appropriate simplex. The row and column populations therefore have
different strategy dimensions in a rectangular game.

Payoffs
-------

Individuals at the same position in the two populations are paired. Their
expected payoffs are

.. math::

   \pi_i^r(t) = P_i^r(t)^{\mathsf T} A P_i^c(t)

and

.. math::

   \pi_i^c(t) = P_i^r(t)^{\mathsf T} B P_i^c(t).

The fittest row and column individuals are selected independently:

.. math::

   i_r^* = \mathop{\mathrm{argmax}}_i \pi_i^r(t), \qquad
   i_c^* = \mathop{\mathrm{argmax}}_i \pi_i^c(t).

If several individuals have the same maximum payoff, the first is selected.

Imitation update
----------------

Every individual copies the fittest strategy in their own population:

.. math::

   P_i^r(t + 1) = P_{i_r^*}^r(t), \qquad
   P_i^c(t + 1) = P_{i_c^*}^c(t)

for every :math:`i \in \{1, \ldots, N\}`. Under this global, synchronous
update rule, each population is homogeneous after its first update. Further
iterations therefore leave the population unchanged.

Returned profiles
-----------------

After the requested iterations, Nashpy calculates each population's mean
mixed strategy and applies a component-wise threshold :math:`\tau`. A component
is returned as 1 when it is at least :math:`\tau`, and as 0 otherwise.

These thresholded profiles are a representation of the final populations.
They need not sum to 1 and are not necessarily Nash equilibria.

Comparison with fictitious play
-------------------------------

Imitation dynamics copies strategies that achieved high expected payoffs in a
population. Fictitious play instead records the opponent's historical actions
and repeatedly chooses a best response to those empirical play counts. Thus,
the two processes use different information and their generated states have
different interpretations.

Using Nashpy
------------

See :ref:`how-to-use-imitation-dynamics` for an executable example.
