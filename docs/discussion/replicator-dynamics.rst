.. _replicator-dynamics:

Replicator dynamics
===================

The replicator dynamic algorithm implemented in :code:`Nashpy` is based on the
one described in [Fudenberg1998]_.


Strategies are assigned amongst the popoulation. Individuals randomly 
encounter other individuals and play their assigned strategy.

As the game continues, the proportion of the population playing each strategy 
increases or decreases depending on whether the payoff of the strategy is higher 
or lower respectively than the mean payoff of the population.

The row player represents a given individual and the column player is the population.

Given a matrix :math:`A\in\mathbb{R}^{m\times n}` that corresponds to the utilities 
of the row player, we have:

.. math::

   f = Ax 

Where :math:`f\in\mathbb{R}^{m\times 1}` corresponds to the fitness of each strategy 
and :math:`x\in\mathbb{R}^{m\times 1}` corresponds to the population size of each strategy  

Equivalently, where :math:`\phi` equals the average fitness of the population, we have: 

.. math::

   \phi = fx

In matrix formation we can calculate the rate of change of the strategies:

.. math::

   \frac{dx}{dt}_i = x_i(f_i - \phi)\text{ for all }i

Discussion
----------

Stability is acheived in replicator dynamics when :math:`\frac{dx}{dt} = 0`.
Every stable steady state is a Nash equilibria, and every Nash equilibria is a steady 
state in replicator dynamics. 

A steady state is when the population shares of all strategies are constant.

Steady states are reached when either:

- An entire population plays the same strategy
- A population plays a mixture of the strategies (such that there is indifference between the fitness)

It is possible that the game does not converge to a steady state. See below an example of a game of Rock, 
Paper, Scissors that does not converge::

>>> import numpy as np
>>> import nashpy as nash
>>> import matplotlib.pyplot as plt
>>> A = np.array([[0, -1, 1], [1, 0, -1], [-1, 1, 0]])
>>> game = nash.Game(A)
>>> y0 = np.array([0.3, 0.35, 0.35])

>>> plt.plot(game.replicator_dynamics(y0=y0)) # doctest: +SKIP
>>> plt.xlabel("Timepoints") # doctest: +SKIP
>>> plt.ylabel("Probability") # doctest: +SKIP
>>> plt.title("Probability distribution of strategies over time") # doctest: +SKIP
>>> plt.legend([f"$s_{0}$", f"$s_{1}$", f"$s_{2}$"], loc='upper left') # doctest: +SKIP

.. image:: /_static/learning/evolutionary_dynamics/non_convergence_example/main.svg

Below shows an example of a stable steady state::

>>> import numpy as np
>>> import nashpy as nash
>>> import matplotlib.pyplot as plt
>>> A = np.array([[4, 3], [2, 3]])
>>> game = nash.Game(A)
>>> y0 = np.array([1 / 2, 1 / 2])
>>> timepoints = np.linspace(0, 10, 1000)

>>> plt.plot(game.replicator_dynamics(y0=y0, timepoints=timepoints)) # doctest: +SKIP
>>> plt.xlabel("Timepoints") # doctest: +SKIP
>>> plt.ylabel("Probability") # doctest: +SKIP
>>> plt.title("Probability distribution of strategies over time") # doctest: +SKIP
>>> plt.legend([f"$s_{0}$", f"$s_{1}$"]) # doctest: +SKIP

.. image:: /_static/learning/evolutionary_dynamics/steady_state_example/main.svg

Evolutionary stable strategies (ESS) stay stable subject to small evolutionary change. This means that 
the strategy cannot be invaded by any of the other strategies in the population.
Every ESS is an asymptotically stable steady state of the replicator dynamic, but the converse does not 
necessarily hold.

To visualise an example of ESS consider the matrix :math:`A = \begin{pmatrix} 4 & 3 \\ 2 & 3\end{pmatrix}`.
It can be shown that :math:`(1, 0)` is an ESS for this game. Below we take a small change from this strategy 
and note that the replicator dynamics guide us back to it.

>>> import numpy as np
>>> import nashpy as nash
>>> import matplotlib.pyplot as plt
>>> A = np.array([[4, 3], [2, 3]])
>>> game=nash.Game(A)
>>> epsilon = 1 / 10
>>> y0 = np.array([1 - epsilon, 0 + epsilon])
>>> timepoints = np.linspace(0, 10, 1000)
>>> timepoints[-1]
10.0


>>> plt.plot(game.replicator_dynamics(y0=y0, timepoints=timepoints)) # doctest: +SKIP
>>> plt.xlabel("Timepoints") # doctest: +SKIP
>>> plt.ylabel("Probability") # doctest: +SKIP
>>> plt.title("Probability distribution of strategies over time") # doctest: +SKIP
>>> plt.legend([f"$s_{0}$", f"$s_{1}$"]) # doctest: +SKIP

.. image:: /_static/learning/evolutionary_dynamics/ess_example/main.svg
