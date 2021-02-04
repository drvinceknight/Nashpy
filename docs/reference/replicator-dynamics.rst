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

Equivalently:

.. math::

   \phi = fx

We get:

.. math::

   \frac{dx}{dt} = x(f - \phi)

Discussion
----------

