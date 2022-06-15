.. _asymmetric-replicator-dynamics:

Asymmetric replicator dynamics
==============================

The asymmetric replicator dynamics algorithm is implemented in :code:`Nashpy`
based on the work presented in  [Elvio2011]_. This is considered as the 
asymmetric version of the symmetric :ref:`replicator-dynamics-discussion`.

There exists a population with two types of individuals where each type has 
their own strategy set. Strategies are assigned amongst the population. 
Individuals randomly encounter individuals of the opposite type and play their 
assigned strategies.

As the game progresses the proportion of each type playing each strategy changes
based on their previous interactions.

The row player represents the first type of individuals and the column player 
represents the other one.

Given two matrices :math:`A\in\mathbb{R}^{m\times n}` and 
:math:`B\in\mathbb{R}^{m\times n}` that correspond to the utilities 
of the row player and column player respectively, we define:

.. math::

    f_x = Ay \\
    f_y = x^T B

Where :math:`x\in\mathbb{R}^{m\times 1}` and :math:`y\in\mathbb{R}^{n\times 1}` 
corresponds to the population size of the strategies of the two players and 
:math:`f_x\in\mathbb{R}^{n\times1}` and :math:`f_y\in\mathbb{R}^{1\times m}` 
corresponds to the fitness of the strategies of the row player and the column 
player respectively.

Similarly, the average fitness for the two types of populations is given by 
:math:`\phi_x` and :math:`\phi_y` where:

.. math::

    \phi_x = f_x x^T \\
    \phi_y = f_y y


In matrix notation the rate of change of the strategies of both types of 
individuals is captured by:

.. math::

    \frac{dx}{dt}_i = x_i((f_x)_i - \phi_x) \text{ for all }i \\
    \frac{dy}{dt}_i = y_i((f_y)_i - \phi_y) \text{ for all }i


Discussion
----------

Stability is achieved in asymmetric replicator dynamics when both
:math:`\frac{dx}{dt} = 0` and :math:`\frac{dy}{dt} = 0`.
Every stable steady state is a Nash equilibria, and every Nash equilibria
is a steady state in asymmetric replicator dynamics.

Similarly to :ref:`replicator-dynamics-discussion`, a game is not guaranteed to converge
to a steady state.
Find below the probability distributions for both the row player and the column 
player over time, of a game that does not converge::


>>> import matplotlib.pyplot as plt
>>> import nashpy as nash
>>> import numpy as np
>>> A = np.array([[0, -1, 1], [1, 0, -1], [-1, 1, 0]])
>>> B = A.transpose()
>>> game = nash.Game(A, B)
>>> x0 = np.array([0.3, 0.35, 0.35])
>>> y0 = np.array([0.3, 0.35, 0.35])
>>> xs, ys = game.asymmetric_replicator_dynamics(x0=x0, y0=y0)

>>> plt.figure(figsize=(15, 5)) # doctest: +SKIP
>>> plt.subplot(1, 2, 1) # doctest: +SKIP
>>> plt.plot(xs) # doctest: +SKIP
>>> plt.title("Probability distribution of strategies over time for row player") # doctest: +SKIP
>>> plt.legend([f"$s_{0}$", f"$s_{1}$", f"$s_{2}$"]) # doctest: +SKIP
>>> plt.subplot(1, 2, 2) # doctest: +SKIP
>>> plt.plot(ys) # doctest: +SKIP
>>> plt.xlabel("Timepoints") # doctest: +SKIP
>>> plt.ylabel("Probability") # doctest: +SKIP
>>> plt.title("Probability distribution of strategies over time for column player") # doctest: +SKIP
>>> plt.legend([f"$s_{0}$", f"$s_{1}$", f"$s_{2}$"]) # doctest: +SKIP

.. image:: /_static/learning/asymmetric_evolutionary_dynamics/non_convergence_example/main.svg

Find below an example of a game that is able to reach a stable steady state::

>>> import matplotlib.pyplot as plt
>>> import nashpy as nash
>>> import numpy as np
>>> A = np.array([[2, 2], [3, 4]])
>>> B = np.array([[4, 3], [3, 2]])
>>> game = nash.Game(A, B)
>>> x0 = np.array([0.9, 0.1])
>>> y0 = np.array([0.3, 0.7])
>>> xs, ys = game.asymmetric_replicator_dynamics(x0=x0, y0=y0)

>>> plt.figure(figsize=(15, 5)) # doctest: +SKIP
>>> plt.subplot(1, 2, 1) # doctest: +SKIP
>>> plt.plot(xs) # doctest: +SKIP
>>> plt.title("Probability distribution of strategies over time for row player") # doctest: +SKIP
>>> plt.legend([f"$s_{0}$", f"$s_{1}$"]) # doctest: +SKIP
>>> plt.subplot(1, 2, 2) # doctest: +SKIP
>>> plt.plot(ys) # doctest: +SKIP
>>> plt.xlabel("Timepoints") # doctest: +SKIP
>>> plt.ylabel("Probability") # doctest: +SKIP
>>> plt.title("Probability distribution of strategies over time for column player") # doctest: +SKIP
>>> plt.legend([f"$s_{0}$", f"$s_{1}$"]) # doctest: +SKIP

.. image:: /_static/learning/asymmetric_evolutionary_dynamics/steady_state_example/main.svg
