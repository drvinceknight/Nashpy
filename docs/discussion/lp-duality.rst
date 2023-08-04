.. _lp-duality:

Linear Programming Duality
==========================

This section gives an overview of Linear Programming and specifically states the
Linear Programming Duality Theorem which is necessary to prove the
:ref:`the-minimax-theorem`.

An excellent review of this is given in [vonStengel2023]_.

.. _definition-of-a-linear-program:

Definition of a Linear Program
------------------------------

A linear program defined by :math:`M\in\mathbb{R}^{(m\times n}`,
:math:`b\in\mathbb{R}^{m}` and :math:`c\in\mathbb{R}^n` corresponds to:

.. math::


   \max_{x\in\mathbb{R}^{n}} c^Tx

Subject to:

.. math::

   \begin{align}
        Mx &\leq b \\
        x_i            &\geq 0&&\text{ for }i\leq m
   \end{align}

Such a linear program is **feasible** if there exists some vector :math:`x` that
satisfies the constraints.

.. _definition_of_dual_linear_program:

Definition of the Dual of a Linear Program
------------------------------------------

The dual of the linear program of :ref:`definition-of-a-linear-program` is
defined by:

.. math::

   \min_{y\in\mathbb{R}^{m}} y^Tb

Subject to:

.. math::

   \begin{align}
        M^T y &\geq c \\
        y_i            &\geq 0&&\text{ for }i\leq n
   \end{align}


.. _linear_program_duality_theorem:

Linear Program Duality Theorem
------------------------------

If a linear program and its dual are both feasible then there exists :math:`x`
and :math:`y` that are both optimal solutions such that :math:`c^Tx=y^Tb`.

A variety of proofs of this theorem exist that take different approaches. One
such proof can be found in [Vanderbei1998]_.
