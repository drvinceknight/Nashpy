.. _discrete-replicator-dynamics:

Discrete Replicator dynamics
============================

.. _motivating-example-discrete-replicator-dynamics:

Motivating example: once a day hawk dove game
---------------------------------------------

Consider the Hawk Dove model shown in :ref:`replicator dynamics <replicator-dynamics-discussion>`, 
where we wish to model the populations of aggressive and sharing animals over time
but assume the population of aggressive and sharing animals only changes once a day.

We use the following payoff matrix:

.. math::

   A = \begin{pmatrix}
       2 & 1\\
       3 & 0
   \end{pmatrix}


and starting population distribution

.. math::

   x_0 = \begin{pmatrix}0.05\\0.95\end{pmatrix}

where 95% are sharers while 5% are aggressive.

How would we model this situation with the added constraint of discrete time?

The discrete replicator dynamics equation
-----------------------------------------

Given a population with :math:`N` types of individuals. Where the fitness of an
individual of type :math:`i` when interacting with an individual of type
:math:`j` is given by :math:`A_{ij}` where :math:`A\in\mathbb{R}^{N \times N}`.
The discrete replicator dynamics equation defines a sequence :math:`x^{(t)}` given by:

.. math::

   x_{i}^{(t + 1)} = x_i^{(t)} \frac{(Ax)_i}{{x^{(t)}}^T A x^{(t)}}

where:

.. math::

   \phi = \sum_{i=1} ^ N x_i^{(t)} f_i(x)

where :math:`f_i` is the population dependent fitness of individuals of type
:math:`i`:

.. math::

   f_i(x) = (Ax^{(t)})_i


For the :ref:`motivating-example-discrete-replicator-dynamics` this gives
discrete results (on the left) similar to the continuous replicator function (on the right).

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

Both the continuous and discrete replicator functions produce a proportion of a total population, this addresses
the first modelling challenge: to have discrete time.

However what if we wanted to model a finite population of 100 animals?

Quantizing a Population Distribution
------------------------------------

This algorithm is first described in [Greenwood2019]_, the aim is to convert a continuous population
distribution :math:`\mathbf{x} = (x_1, \dots, x_n)` into a vector of integer
counts :math:`\mathbf{k} = (k_1, \dots, k_n)` such that the entries sum exactly
to :math:`N` while remaining as close as possible to the unquantised values
:math:`N x_i`.

This quantization step is done at every step of the discrete replicator dynamics
to ensure the population vector remains integer.

Algorithm (Quantisation of a Population Distribution)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Given a population distribution :math:`\mathbf{x}` and a total population
:math:`N`, proceed as follows:

1. **Initial rounding step**

   For each :math:`i = 1, \dots, n`, compute

   .. math::

      k'_i = \left\lfloor N x_i - \tfrac{1}{2} \right\rfloor.

2. **Check population consistency**

   Compute the discrepancy

   .. math::

      d = \sum_{i=1}^n k'_i - N.

   If :math:`d = 0`, return :math:`\mathbf{k}'` immediately.

3. **Compute rounding errors**

   For each :math:`i`, compute the error

   .. math::

      \delta_i = k'_i - N x_i,

   which quantifies the deviation of :math:`k'_i` from its exact value
   :math:`N x_i`.

4. **Adjust to restore the correct total**

   - If :math:`d > 0` (too many individuals have been allocated):

     Select the :math:`d` largest errors :math:`\delta_i` and decrement each
     corresponding :math:`k'_i` by 1.

   - If :math:`d < 0` (too few individuals have been allocated):

     Select the :math:`|d|` smallest errors :math:`\delta_i` and increment each
     corresponding :math:`k'_i` by 1.

5. **Return the corrected population**

   The adjusted vector :math:`\mathbf{k}'` now sums to :math:`N` and is the
   closest integer-valued approximation to the unquantised population
   :math:`N \mathbf{x}`.


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


Using Nashpy
------------

See :ref:`how-to-use-discrete-replicator-dynamics` for guidance of how to use Nashpy to
obtain numerical solutions of the discrete replicator dynamics equation.
