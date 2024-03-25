Regret Minimization
===================

Introduction
------------

In the context of game theory, "Regret" refers to the difference between a player's actual payoff and the payoff they would have received by playing a different strategy. By minimising regrets, players converge towards a Nash Equilibrium where no player has an incentive to deviate from their chosen strategy unilaterally

Regret minimization is a concept used in game theory to model how players learn and adapt their strategies over time. It measures the "regret" experienced by a player for not choosing a different strategy that could have yielded a better outcome in hindsight.

Mathematically, let's consider a sequential game where player :math:`i` selects a strategy from a set :math:`S_i` at each time step. The regret :math:`R_i(t)` of player :math:`i` at time :math:`t` with respect to strategy :math:`s` is defined as:

.. math::

    R_i(t) = \max_{s' \in S_i} \sum_{\tau=1}^{t} u_i(s', s_{-i}^\tau) - \sum_{\tau=1}^{t} u_i(s, s_{-i}^\tau)

where:
- :math:`s_{-i}^\tau` represents the joint strategy profile of all players except :math:`i` up to time :math:`\tau`.
- :math:`u_i(s, s_{-i}^\tau)` is the utility or payoff obtained by player :math:`i` when playing strategy :math:`s` against the joint strategy :math:`s_{-i}^\tau`.

The regret measures how much payoff player :math:`i` could have gained if they had chosen a different strategy instead of :math:`s` in each time step up to time :math:`t`.

Regret Minimization Implementation
----------------------------------

An algorithm can be used to minimize "regret" by iteratively updating strategies based on past regrets. At each time step, a player selects the strategy that minimizes their regret. This approach aims to converge towards a strategy profile with low regret.

Mathematically, the algorithm can be summarized as follows:

- Initialize strategies for all players.
- At each time step :math:`t`:
  - Calculate the regret for each player based on their current strategy.
  - Update strategies by selecting the option that minimizes regret for each player.
- Repeat until convergence or a stopping condition is met.

By iteratively updating strategies to minimize regret, players can learn to make better decisions over time and potentially converge towards a Nash equilibrium in the game.


Using Nashpy
------------

See :ref:`how-to-use-regret-minimization` for guidance of how to use Nashpy to
use Regret Minimization.
