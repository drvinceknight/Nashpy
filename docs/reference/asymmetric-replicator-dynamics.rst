.. _asymmetric-replicator-dynamics:

Asymmetric replicator dynamics
==============================

The asymmetric replicator dynamics algorithm is implemented in :code:`Nashpy`
based on the work presented in  [Elvio2011]_. This is considered as the 
asymmetric version of the symmetric :ref:`replicator-dynamics`.

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

