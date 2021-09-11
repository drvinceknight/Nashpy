.. _best-responses-discussion:

Best responses
==============

.. _motivating-example-matching-pennies:

Motivating example: Best Responses in Matching Pennies
------------------------------------------------------

Considering the game :ref:`matching-pennies`:

..  math::

    A = \begin{pmatrix}
    1 & -1\\
    -1 & 1
    \end{pmatrix}
    \qquad
    B = \begin{pmatrix}
    -1 & 1\\
    1 & -1
    \end{pmatrix}

If the row player knows that the column player is playing the :ref:`strategy
<strategies-discussion>` :math:`\sigma_c=(0, 1)` the utility of the row player
is maximised by playing :math:`\sigma_r=(0, 1)`.

In this case :math:`\sigma_r` is referred to as a **best response** to
:math:`\sigma_c`.

Alternatively, if the column player knows that the row player is playing the
:ref:`strategy <strategies-discussion>` :math:`\sigma_r=(0, 1)` the column
player's best response is :math:`\sigma_c=(1, 0)`.

.. _definition-of-best-response:

Definition of a best response in a normal form game
---------------------------------------------------

In a two player game :math:`(A,B)\in{\mathbb{R}^{m\times n}}^2` a strategy
:math:`\sigma_r^*`  of the row player is a best response to a column players'
strategy :math:`\sigma_c` if and only if:

.. math::

   \sigma_r^*=\text{argmax}_{\sigma_r\in \mathcal{S}_1}\sigma_rA\sigma_c^T.

Where :math:`\mathcal{S}_1` denotes the :ref:`space of all
strategies<definition-of-strategy-spaces-in-normal-form-games>` for the first
player.

Similarly a mixed strategy :math:`\sigma_c^*`  of the column player is a best
response to a row players' strategy :math:`\sigma_r` if and only if:

.. math::

   \sigma_c^*=\text{argmax}_{\sigma_c\in \mathcal{S}_2}\sigma_rB\sigma_c^T.


.. admonition:: Question
   :class: note

   For the :ref:`Prisoners Dilemma <prisoners-dilemma>`:

   What is the row player's best response to either of the actions of the
   column player?

.. admonition:: Answer
   :class: caution, dropdown

   Recalling that :math:`A` is given by:

   .. math::

      A = \begin{pmatrix}
      3 & 0\\
      5 & 1
      \end{pmatrix}

   Against the first action of the column player the best response is to choose
   the second action which gives a utility of 5. This can be expressed as:

   .. math::

      \text{argmax}_{i\in\mathcal{S}_1}A_{i1}=2

   Against the second action of the column player the best response is to choose
   the second action which gives a utility of 1. This can be expressed as:

   .. math::

      \text{argmax}_{i\in\mathcal{S}_1}A_{i2}=2


   The row player's best response to either of the actions of the column player
   is :math:`\sigma_r^*=(1,0)`. This can be expressed as:

   .. math::

      \text{argmax}_{i\in\mathcal{S}_1}A_{ij}=2\text{ for all }j\in\mathcal{A}_2

.. _best_responses_in_2_by_2_games:

Generic best responses in 2 by 2 games
--------------------------------------

In two player normal form games with :math:`|A_1|=|A_2|=2`: a 2 by 2 game, the
utility of a row player playing :math:`\sigma_r=(x, 1 - x)` against a strategy
:math:`\sigma_c = (y, 1 - y)` is linear in :math:`x`:

.. math::

   u_r(\sigma_r, \sigma_c) &= (x, 1 - x) A (y, 1 - y) ^T \\
                           &= A_{11}xy + A_{12}x(1-y) + A_{21}(1-x)y + A_{22}(1-x)(1-y) \\
                           &= a x + b

where:

.. math::

   a &=  A_{11}y + A_{12}(1 - y) - A_{21}y - A_{22}(1 - y)\\
   b &=  A_{21}y + A_{22}(1 - y)

This observation allows us to obtain the best response :math:`\sigma_r^*`
against any :math:`\sigma_c = (y, 1 - y)`.

For example, consider :ref:`matching-pennies`. Below is a plot of
:math:`u_r(\sigma_r, \sigma_c)` as a function of :math:`y` for :math:`\sigma_r
\in \{(1, 0), (0, 1)\}`.

.. plot::

   import matplotlib.pyplot as plt
   import nashpy as nash
   import numpy as np

   A = np.array([[1, -1], [-1, 1]])
   game = nash.Game(A)
   ys = [0, 1]
   sigma_rs = [(1, 0), (0, 1)]
   u_rs = [[game[sigma_r, (y, 1 - y)][0] for y in ys] for sigma_r in sigma_rs]
   plt.plot(ys, u_rs[0], label="$(A\sigma_c^T)_1$")
   plt.plot(ys, u_rs[1], label="$(A\sigma_c^T)_2$")
   plt.xlabel("$\sigma_c=(y, 1-y)$")
   plt.title("Utility to row player")
   plt.legend()

Given that the utilities in both cases are linear, the best response to any
value of :math:`y \ne 1/2` is either :math:`(1, 0)` or :math:`(0, 1`.
The best response :math:`\sigma_r^*` is given by:

.. math::

   \sigma_r ^* = \begin{cases}
                    (1, 0),& \text{ if } y > 1/2\\
                    (0, 1),& \text{ if } y < 1/2\\
                    \text{indifferent},& \text{ if } y=1/2
                 \end{cases}

.. _best_responses_condition:

.. admonition:: Question
   :class: note

   For the :ref:`matching-pennies` game:

   What is the column player's best response as a function of :math:`x` where
   :math:`\sigma_r=(x, 1 - x)`.

.. admonition:: Answer
   :class: caution, dropdown

   Recalling that :math:`B` is given by:

   .. math::

      B = \begin{pmatrix}
      -1 & 1\\
      1 & -1
      \end{pmatrix}

   This gives:

   .. math::

      u_c(\sigma_r, (1, 0)) =& -x + (1-x)= 1 - 2x\\
                            =& x - (1-x)= -1 + 2x


   Here is a plot of the utilities:

   .. plot::

      import matplotlib.pyplot as plt
      import nashpy as nash

      xs = np.array([0, 1])
      u_cs = [1 - 2 * xs, - 1 + 2 * xs]
      plt.plot(xs, u_cs[0], label="$(\sigma_rB)_1$")
      plt.plot(xs, u_cs[1], label="$(\sigma_rB)_2$")
      plt.xlabel("$\sigma_r=(x, 1-x)$")
      plt.title("Utility to column player")
      plt.legend()

.. _best_response_condition:

General condition for a best response
-------------------------------------

In a two player game :math:`(A,B)\in{\mathbb{R}^{m\times n}}^2` a strategy
:math:`\sigma_r^*`  of the row player is a best response to a column players'
strategy :math:`\sigma_c` if and only if:

.. math::

   {\sigma_{r^*}}_i > 0 \Rightarrow (A\sigma_c^T)_i = \text{max}_{k \in \mathcal{A}_2}(A\sigma_c ^ T)_k \text{ for all }i \in \mathcal{A}_1


Proof
*****

:math:`(A\sigma_c^T)_i` is the utility of the row player when they play their
:math:`i^{\text{th}}` action. Thus:

.. math::

   \sigma_rA\sigma_c^T=\sum_{i=1}^{m}{\sigma_r}_i(A\sigma_c^T)_i

Let :math:`u=\max_{k}(A\sigma_c^T)_k` giving:

.. math::

   \sigma_rA\sigma_c^T&=\sum_{i=1}^{m}{\sigma_r}_i(u - u + (A\sigma_c^T)_i)\\
                      &=\sum_{i=1}^{m}{\sigma_r}_iu - \sum_{i=1}^{m}{\sigma_r}_i(u - (A\sigma_c^T)_i)\\
                      &=u - \sum_{i=1}^{m}{\sigma_r}_i(u - (A\sigma_c^T)_i)

We know that :math:`u - (A\sigma_c^T)_i\geq 0`, thus the largest
:math:`\sigma_rA\sigma_c^T` can be is :math:`u` which occurs if and only if
:math:`{\sigma_r}_i > 0 \Rightarrow (A\sigma_c^T)_i = u` as required.

.. admonition:: Question
   :class: note

   For the :ref:`Rock Paper Scissors <motivating-example-strategy-for-rps>`
   game:

   Which of the following pairs of strategies are best responses to each other:

   1. :math:`\sigma_r=(0, 0, 1) \text{ and } \sigma_c=(0, 1/2, 1/2)`
   2. :math:`\sigma_r=(1/3, 1/3, 1/3) \text{ and } \sigma_c=(0, 1/2, 1/2)`
   3. :math:`\sigma_r=(1/3, 1/3, 1/3) \text{ and } \sigma_c=(1/3, 1/3, 1/3)`

.. admonition:: Answer
   :class: caution, dropdown

   Recalling that :math:`A` and :math:`B` are given by:


   .. math::

      A = \begin{pmatrix}
      0  & -1 & 1 \\
      1  & 0  & -1\\
      -1 & 1  & 0\\
      \end{pmatrix}

   .. math::

      B = - A = \begin{pmatrix}
      0  & 1 & -1 \\
      -1  & 0  & 1\\
      1 & -1  & 0\\
      \end{pmatrix}

   We can apply the best response condition to each pairs of strategies:

   1. :math:`A\sigma_c^T = \begin{pmatrix}0\\ -1/2\\ 1/2\\\end{pmatrix}`.
      :math:`\text{max}(A\sigma_c^T)=1/2`. The only :math:`i` for which
      :math:`{\sigma_r}_i > 0` is :math:`i=3` and
      :math:`(A\sigma_c^T)_3=\text{max}(A\sigma_c^T)` thus :math:`\sigma_r`
      **is a best response to** :math:`\sigma_c`.  :math:`\sigma_rB = (1, -1,
      0)`.  :math:`\text{max}(\sigma_rB)=1`. The values of :math:`i` for
      which :math:`{\sigma_c}_i > 0` are :math:`i=2` and :math:`i=3` but
      :math:`(\sigma_r B)_2 \ne \text{max}(\sigma_r B)` thus :math:`\sigma_c`
      **is not a best response to** :math:`\sigma_r`.
   2. :math:`A\sigma_c^T = \begin{pmatrix}0\\ -1/2\\ 1/2\\\end{pmatrix}`.
      :math:`\text{max}(A\sigma_c^T)=1/2`. The values of :math:`i` for which
      :math:`{\sigma_r}_i > 0` are :math:`i=1`, :math:`i=2` and :math:`i=3`
      however, :math:`(A\sigma_c^T)_2 \ne \text{max}(A\sigma_c^T)` thus
      :math:`\sigma_r` **is not a best response to** :math:`\sigma_c`.
      :math:`\sigma_rB = (0, 0, 0)`.  :math:`\text{max}(\sigma_rB)=0`. The
      values of :math:`i` for which :math:`{\sigma_c}_i > 0` are :math:`i=2`
      and :math:`i=3` and :math:`(\sigma_r B)_2 = (\sigma_r B)_3=
      \text{max}(\sigma_r B)` thus :math:`\sigma_c` **is a best response to**
      :math:`\sigma_r`.
   3. :math:`A\sigma_c^T = \begin{pmatrix}0\\ 0\\ 0\\\end{pmatrix}`.
      :math:`\text{max}(A\sigma_c^T)=0`. The values of :math:`i` for which
      :math:`{\sigma_r}_i > 0` are :math:`i=1`, :math:`i=2` and :math:`i=3`
      and :math:`(A\sigma_c^T)_1=(A\sigma_c^T)_2 = (A\sigma_c^T)_3
      =\text{max}(A\sigma_c^T)` thus :math:`\sigma_r` **is a best response
      to** :math:`\sigma_c`.  :math:`\sigma_rB = (0, 0, 0)`.
      :math:`\text{max}(\sigma_rB)=0`. The values of :math:`i` for which
      :math:`{\sigma_c}_i > 0` are :math:`i=1`, :math:`i=2` and :math:`i=3`
      and :math:`(\sigma_r B)_1 =(\sigma_r B)_2 = (\sigma_r B)_3=
      \text{max}(\sigma_r B)` thus :math:`\sigma_c` **is a best response to**
      :math:`\sigma_r`.


Definition of Nash equilibrium
------------------------------

In a two player game :math:`(A, B)\in {\mathbb{R}^{m \times n}} ^ 2`,
:math:`(\sigma_r, \sigma_c)` is a Nash equilibria if :math:`\sigma_r` is a best
response to :math:`\sigma_c` and :math:`\sigma_c` is a best response to
:math:`\sigma_r`.

Using Nashpy
------------

See :ref:`how-to-check-best-responses` for guidance of how to
use Nashpy to check if a strategy is a best response.
