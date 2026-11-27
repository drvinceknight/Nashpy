.. _regret-minimization:

Regret Minimization
===================

Nashpy implements cumulative external regret matching for two-player bimatrix
games. This deterministic, full-information version evaluates utilities
against the opponent's mixed strategy each round.
For background on positive-regret matching and averaging, see
[Neller2013]_, Section 2.3.

Updates
-------

Let :math:`A, B \in \mathbb{R}^{m \times n}` be the payoff matrices and
:math:`x_t \in \Delta_m`, :math:`y_t \in \Delta_n` the mixed strategies
played in round :math:`t`. Both players start uniformly, with zero cumulative
regrets.

The pure-action utility vectors are

.. math::

   a_t = A y_t, \qquad b_t = B^{\mathsf T} x_t.

The corresponding instantaneous regrets compare each action's utility to the
player's current expected payoff:

.. math::

   r^r_t = a_t - (x_t^{\mathsf T} a_t) \mathbf{1}_m,
   \qquad
   r^c_t = b_t - (y_t^{\mathsf T} b_t) \mathbf{1}_n.

Accumulate these signed differences for each action:

.. math::

   R^r_t = R^r_{t-1} + r^r_t, \qquad
   R^c_t = R^c_{t-1} + r^c_t.

Negative entries must remain in the cumulative vectors. Only when choosing the
next strategy do we take the positive part :math:`R^+_i = \max(R_i, 0)`:

.. math::

   x_{t+1,i} =
   \begin{cases}
      R^{r,+}_{t,i} / \sum_j R^{r,+}_{t,j}
         & \text{if } \sum_j R^{r,+}_{t,j} > 0, \\
      1/m & \text{otherwise}.
   \end{cases}

The column player uses the same rule with its own :math:`n` actions. Both
players' utilities and regrets use the same pre-update profile
:math:`(x_t, y_t)`.

Averaging and convergence
-------------------------

After :math:`T > 0` played rounds the returned vectors are

.. math::

   \bar{x}_T = \frac{1}{T} \sum_{t=1}^T x_t,
   \qquad
   \bar{y}_T = \frac{1}{T} \sum_{t=1}^T y_t.

The uniform initial strategies count as the first round. For zero rounds,
Nashpy returns the uniform strategies by convention. The generator yields
one final pair.

In zero-sum games, both players' vanishing average external regret implies that
the average profiles approach the set of Nash equilibria. For :math:`B=-A`,
the non-negative duality gap

.. math::

   g_T = \max_i (A\bar{y}_T)_i -
         \min_j (\bar{x}_T^{\mathsf T} A)_j

is zero exactly at an equilibrium. It equals the sum of the two players'
best-response gains and is bounded above by the sum of their positive average
external regrets. A finite number of rounds need not give an exact equilibrium.
See [Zinkevich2007]_, Section 2.3, for the connection between regret and
approximate equilibrium.

In general bimatrix games, the pair of average marginal strategies can lie
outside the set of Nash equilibria.

Using Nashpy
------------

See :ref:`how-to-use-regret-minimization` for examples and migration guidance.
