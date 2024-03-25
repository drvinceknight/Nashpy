Imitation Dynamics
==================

Introduction
------------

The mathematical model of imitation dynamics describes how individuals in a population adapt their strategies over time based on observing the strategies of others. This document provides a detailed mathematical formulation for understanding and simulating imitation dynamics in strategic games.

Initialization
---------------

- Let `N` denote the number of individuals in the population.
- Let `M` denote the number of strategies available to each individual.
- Initialize the population as an :math:`N \times M` \ matrix `P`, where each row represents the strategy of an individual.

Interaction and Payoff Calculation
-----------------------------------

- Define a payoff matrix `U` for each player, where :math:`U_ij` represents the payoff for player `i` when they choose strategy `j` and their opponent chooses strategy `k`.
- Calculate the payoff for each individual `n` given their strategy :math:`P_n` and the strategies of all other individuals:
  :math:`\text{Payoff}_n = \text{P}_n \cdot U \cdot P^T`

Imitation Mechanism
--------------------

- Identify the fittest individual based on their payoffs.
- Let `F` be the index (or indices) of the fittest individual.
- Update the strategies of all individuals to match the strategy of the fittest individual:
  :math:`P_n` = :math:`P_F`, for all :math:`n = 1, 2, \ldots, N`

Population Update
-----------------

- Repeat the interaction, payoff calculation, and imitation mechanism steps for a certain number of generations or until convergence.

Convergence and Nash Equilibrium
---------------------------------

- Check for convergence by comparing strategies of successive generations.
- If strategies stabilize, it indicates a potential Nash equilibrium.

Thresholding (Optional)
------------------------

- Apply a thresholding mechanism to discretize strategies, values must range between 0 and 1, defaulted to 0.5.

Comparison with Fictitious Play
-------------------------------

Even though the Imitation dynamics method to find equilibrium looks similar to the Fictional Play method, with strategies updated adaptively over time and players adjusting their strategies based on observations of past interactions or outcomes, there are a few differences between them, which are listed below.

**Key Differences between Imitation Dynamics and Fictitious Play**


**Strategy Update Mechanism**

- In :code:`imitation_dynamics`, players copy the strategy of the most successful individual. This means that at each iteration, players directly mimic the strategy of the individual who achieved the highest payoff. 

- In :code:`fictitious_play`, on the other hand, players update their strategies based on observed play counts of opponents' strategies. This involves players selecting their next move based on the cumulative history of their opponents' strategies rather than directly imitating successful players.

Using Nashpy
------------

See :ref:`how-to-use-imitation-dynamics` for guidance of how to use Nashpy to
simulation Imitation Dynamics.
