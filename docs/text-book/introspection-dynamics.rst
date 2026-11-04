.. _introspection-dynamics:

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

*Given these asymmetric payoffs, how will the players’ strategies evolve
over time if both adapt introspectively?*


.. _definition-of-the-introspection-dynamics:

The Introspection Dynamics
--------------------------

First defined in [Couto2022]_ introspection dynamics on 2 player games is
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
[Couto2022]_) which defines the steady state probability vector :math:`v` which
gives the probability of being in any given state of action pairs.

Calculating the stationary distribution
---------------------------------------

Let :math:`P` be the transition matrix, with states indexed by action pairs
:math:`(i,j)`. Only one player changes action at a time. For :math:`k\ne i`
and :math:`\ell\ne j`,

.. math::

   P_{(i,j),(k,j)} = \frac{1}{2(M_1-1)}
       \frac{1}{1+e^{-\beta(A_{k,j}-A_{i,j})}},

.. math::

   P_{(i,j),(i,\ell)} = \frac{1}{2(M_2-1)}
       \frac{1}{1+e^{-\beta(B_{i,\ell}-B_{i,j})}}.

All other off-diagonal entries are zero, and the diagonal entry makes each
row sum to one. For finite payoffs and finite :math:`\beta`, each player can
eventually reach any action and the process has a unique stationary
distribution. It satisfies

.. math::

   vP=v, \qquad \sum_{i,j}v_{i,j}=1.

Nashpy solves these balance equations using state elimination
[Grassmann1985]_. Eliminating a state redirects its incoming flow according to
its outgoing transition probabilities. The remaining equations use only
non-negative rates, which avoids cancellation when some transitions are rare.
The eliminated state weights are then reconstructed in logarithmic form and
normalised. The returned array has the same shape as the payoff matrices.

At :math:`\beta=0`, all action pairs have probability :math:`1/(M_1M_2)`.
This stationary distribution describes long-run action frequencies; it is
distinct from a pair of mixed strategies forming a Nash equilibrium.

Using Nashpy
------------

See :ref:`how-to-use-introspection-dynamics` for guidance of how to use Nashpy to obtain
numerical simulations of the Introspection dynamics process.
