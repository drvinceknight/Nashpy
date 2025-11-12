.. _discrete-replicator-dynamics:

Discrete Replicator dynamics
============================
This is the discrete version of the continuous :ref:`replicator dynamics <replicator-dynamics-discussion>` and can be used to model how stratergies evolve over time
in distinct increments.


.. _motivating-example-discrete_replicator_dynamics:


consider the Hawk Dove model shown in :ref:`replicator dynamics <replicator-dynamics-discussion>`, where we wish to model the populations of an aggressive animal and sharing animal over time
but assume the population of aggressive and sharing animals only changes once a day when they interact to eat. 

we can use the same payoff matrix
:math:`A`:

.. math::

   A = \begin{pmatrix}
       2 & 1\\
       3 & 0
   \end{pmatrix}


and starting population distribution

:math:`x_0 = ([0.05,0.95])`:
where 95% are sharers while 5% are aggressive

we can use the following discrete function to find the new population after each time step

:math:`x_{\ i+1} = x_i (\frac{(Ax)_i}{x^T A x})`:

and get discrete results (on the left) similar to the continuous replicator function (on the right)

.. plot::

   import matplotlib.pyplot as plt
   import nashpy as nash
   import numpy as np

   A = np.array([[2, 1], [3, 0]])
   game = nash.Game(A)
   y0 = np.array([0.95, 0.05])
   cont_linspace = np.linspace(0,20,2000)
   sharing_population, aggressive_population =  game.replicator_dynamics(y0 = y0,timepoints = cont_linspace).T
   discrete_sharing_population, discrete_aggressive_population = game.discrete_replicator_dynamics(y0, steps=20).T

   fig, (ax1, ax2) = plt.subplots(1, 2)

   ax1.set_xticks(np.arange(0, 21, step=2))
   ax1.set_ylim(0, 1)
   ax2.set_xticks(np.arange(0, 21, step=2))
   ax2.set_ylim(0, 1)
   ax1.step(np.arange(0, 21, step=1),np.append(y0[0],discrete_sharing_population),label="sharer")
   ax1.step(np.arange(0, 21, step=1),np.append(y0[1],discrete_aggressive_population),label="aggressor")
   ax2.plot(cont_linspace,sharing_population,label="sharer")
   ax2.plot(cont_linspace,aggressive_population,label="aggressor")
   ax1.legend() 
   ax2.legend() 

both the continuous and discrete replicator functions produce a proportion of a total population,
if there were a total of 100 animals in this example this would result in non-intager animal populations.

to resolve this we can use greenwoods algorithm after each discrete time step. 

based on the algorithm described by [Greenwood2019]_,
the quantiszation algorithm rounds the population of each stratergy to its nearest intager value after each step, 
then increments or decrements values with the largest error to ensure the total population stays consistent.



.. plot::

   import matplotlib.pyplot as plt
   import nashpy as nash
   import numpy as np

   A = np.array([[2, 1], [3, 0]])
   game = nash.Game(A)
   y0 = np.array([0.95, 0.05])
   y0q = np.array([95, 5])

   discrete_sharing_population, discrete_aggressive_population = game.discrete_replicator_dynamics(y0, steps=20).T
   quantize_sharing_population, quantize_aggressive_population = game.discrete_replicator_dynamics(y0q, steps=20,quantize=True).T

   fig, (ax1, ax2) = plt.subplots(1, 2)

   ax1.step(np.arange(0, 21, step=1),np.append(y0[0],discrete_sharing_population),label="sharer")
   ax1.step(np.arange(0, 21, step=1),np.append(y0[1],discrete_aggressive_population),label="aggressor")
   ax2.step(np.arange(0, 21, step=1),np.append(y0q[0],quantize_sharing_population),label="sharer")
   ax2.step(np.arange(0, 21, step=1),np.append(y0q[1],quantize_aggressive_population),label="aggressor")

   ax1.set_xticks(np.arange(0, 21, step=2))
   ax1.set_ylim(0, 1)
   ax2.set_xticks(np.arange(0, 21, step=2))
   ax2.set_ylim(0, 100)

   ax1.legend() 
   ax2.legend() 






