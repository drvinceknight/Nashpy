.. _relation-to-gambit:

How does Nashpy relate to Gambit
================================

`Gambit <http://www.gambit-project.org/>`_ is the state of the art software
library for Game Theory [McKelvey2016]_. It also has a Python interface. It
handles :math:`N\geq2` player games and is computationally efficient. It is a
much more mature piece of software than :code:`Nashpy`.

It does **however** sometimes prove difficult to install (because of the
required C libraries), in particular installation is not supported on Windows.
In those instances you can use `Game Theory Explorer
<http://gte.csc.liv.ac.uk/index/>`_ which is a great web point and click
Graphical User Interface (GUI) to Gambit.

The main mission statement of :code:`Nashpy` is to provide a
Python library that implements algorithms that are implemented using the
scientific Python stack (:code:`numpy` and :code:`scipy`).

This is motivated by the fact that `I <http://vknight.org/>`_ wanted a Python
library (not a GUI as I am keen to teach reproducibly research methodologies)
for teaching my Mathematics students. Using the Gambit Python interface is not
sufficient for this as students need to be able to install it on their own
machines (without difficulty).

All the algorithms in :code:`Nashpy` are implemented with readability as the
main motivation. This at times comes at an efficiency cost. For example,
:ref:`support-enumeration` builds the entire Polytope representation (using
functionality of :code:`scipy`) which is not efficient.

**To summarise:**

- If you want to do sophisticated efficient game theoretic computations, use
  `Gambit <http://www.gambit-project.org/>`_.
- If you are happy to use a GUI use `Game Theory Explorer
  <http://gte.csc.liv.ac.uk/index/>`_.
- If you would like a Python library that only requires the common scientific
  python stack for two player games you
  can use :code:`Nashpy`.
