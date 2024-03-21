Greedy Algorithm with Regret Minimization in Game Theory
=========================================================

Introduction
------------

In game theory, the greedy algorithm is often employed as a heuristic approach for optimization problems, while regret minimization is utilized to model how players learn and adapt their strategies over time. This document elaborates on the combination of these two concepts, explaining the mathematical formulations and their application in game theory.

Greedy Algorithm
----------------

The greedy algorithm is a simple heuristic approach used for optimization problems. It makes locally optimal choices at each step with the hope of finding a global optimum. In game theory, the greedy algorithm can be applied in various scenarios, such as resource allocation or strategy selection.

Mathematically, the greedy algorithm can be described as follows:

- Let :math:`S` be the set of available choices or actions.
- At each step :math:`i`, choose the option :math:`s_i` that maximizes or minimizes some objective function :math:`f(s_i)` among the available choices.
- Repeat this process until a stopping condition is met (e.g., reaching a certain number of iterations or convergence).

Regret Minimization in Game Theory
-----------------------------------

Regret minimization is a concept used in game theory to model how players learn and adapt their strategies over time. It measures the "regret" experienced by a player for not choosing a different strategy that could have yielded a better outcome in hindsight.

Mathematically, let's consider a sequential game where player :math:`i` selects a strategy from a set :math:`S_i` at each time step. The regret :math:`R_i(t)` of player :math:`i` at time :math:`t` with respect to strategy :math:`s` is defined as:

.. math::

    R_i(t) = \max_{s' \in S_i} \sum_{\tau=1}^{t} u_i(s', s_{-i}^\tau) - \sum_{\tau=1}^{t} u_i(s, s_{-i}^\tau)

where:
- :math:`s_{-i}^\tau` represents the joint strategy profile of all players except :math:`i` up to time :math:`\tau`.
- :math:`u_i(s, s_{-i}^\tau)` is the utility or payoff obtained by player :math:`i` when playing strategy :math:`s` against the joint strategy :math:`s_{-i}^\tau`.

The regret measures how much payoff player :math:`i` could have gained if they had chosen a different strategy instead of :math:`s` in each time step up to time :math:`t`.

Combining Greedy Algorithm with Regret Minimization
-----------------------------------------------------

In the context of game theory, the greedy algorithm can be used to minimize regret by iteratively updating strategies based on past regrets. At each time step, a player selects the strategy that minimizes their regret. This approach aims to converge towards a strategy profile with low regret.

Mathematically, the algorithm can be summarized as follows:

- Initialize strategies for all players.
- At each time step :math:`t`:
  - Calculate the regret for each player based on their current strategy.
  - Update strategies by selecting the option that minimizes regret for each player using the greedy algorithm.
- Repeat until convergence or a stopping condition is met.

By iteratively updating strategies to minimize regret, players can learn to make better decisions over time and potentially converge towards a Nash equilibrium in the game.


Using Nashpy
------------

See :ref:`how-to-use-regret-minimization` for guidance of how to use Nashpy to
use Regret Minimization.
