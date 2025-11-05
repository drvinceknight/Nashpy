.. _moran-process:

Introspection Dynamics
======================

.. _motivating-example-introspection-dynamics:

Motivating Example: Two firms learning through introspection
--------------------------------------------------------------

Consider a market with two competing firms.  

- **Firm 1** can choose between **Advertising** (:math:`A`) and **Research**
  (:math:`R`).
- **Firm 2** has a larger range of strategic options: it can focus on
  **Price Cut** (:math:`P`), **Branding** (:math:`B`), or **Innovation**
  (:math:`I`).

Each firm earns profits depending on the combination of actions they take:

- When Firm 1 advertises and Firm 2 cuts prices, both gain some market share,
  but profits are modest.
- When Firm 1 invests in research and Firm 2 chooses innovation, both achieve
  good long-term results.
- Branding by Firm 2 is mainly effective when Firm 1 advertises.
- Price cuts by Firm 2 are costly if Firm 1 is focusing on research, and so on.

These interactions can be represented by the two *asymmetric* payoff matrices,
:math:`A` for Firm 1 and :math:`B` for Firm 2:

.. math::

   A = \begin{pmatrix}
       3 & 5 & 4 \\
       4 & 2 & 6
   \end{pmatrix},
   \qquad
   B = \begin{pmatrix}
       3 & 5 & 2\\
       1 & 4 & 6
   \end{pmatrix}

The entry :math:`A_{ij}` gives Firm 1’s payoff when it plays its
:math:`i`-th action and Firm 2 plays its :math:`j`-th, and similarly
for :math:`B_{ji}` for Firm 2.

> *Given these asymmetric payoffs, how will the players’ strategies evolve
> over time if both adapt introspectively?*

The

.. _definition-of-the-introspection-dynamics:

The Introspection Dynamics
--------------------------

First defined in [Couto2023]_ introspection dynamics on 2 player games is
defined as a process on 
:math:`N=2` individuals which can use :math:`M_1` and math:`M_2` actions
respectively.

The process is defined as follows, at each step:

1. One of the two player is selected to reconsider their action choice.
2. The chosen player :math:`i\in\{1, 2\}` randomly selects one of their other
   :math:`M_i - 1` actions. 
3. The chosen player compares their payoff :math:`\pi` with their currently
   assigned action to :math:`\tilde \pi` the payoff they would have had with the
   alternative action. They compute :math:`\Delta=\tilde \pi - \pi`.
4. They change their action to the new action with probability given by:
   .. math::

      \frac{1}{1 + e^{-\beta \Delta}}

:math:`\beta` can be interpreted as a learning rate: if :math:`\beta` is zero
than the probability of picking the new action is uniformly random. A high value
of :math:`\beta` indicates that the play will choose the better action with certainty.

This process corresponds to a Markov chain (details of which can be found in
[Couto2023]_) which defines the steady state probability vector :math:`v` which
gives the probability of being in any given state of action pairs.

The transition matrix for :math:`M_1=M_2=2`
-------------------------------------------

.. TODO

Exercises
---------

.. TODO

Using Nashpy
------------

See :ref:`how-to-use-introspection-dynamics` for guidance of how to use Nashpy to obtain
numerical simulations of the Introspection dynamics process.
