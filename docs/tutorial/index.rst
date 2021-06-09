Tutorial: building and finding the equilibrium for  a game
==========================================================

Introduction to game theory
---------------------------

Game theory is the study of strategic interactions between rational agents.
This means that it is the study of interactions when the involved
parties try and do what is best from their point of view.

As an example let us consider `Rock Paper Scissors
<https://en.wikipedia.org/wiki/Rock%E2%80%93paper%E2%80%93scissors>`_. This is a
common game where two players choose one of 3 options (in game theory we call
these *strategies*):

- Rock
- Paper
- Scissors

The winner is decided according to the following:

- Rock crushes scissors
- Paper covers Rock
- Scissors cuts paper


We can represent this mathematically using a 3 by 3 matrix:

.. math::

   A =
   \begin{pmatrix}
        0 & -1 &  1\\
        1 &  0 & -1\\
       -1 &  1 &  0
   \end{pmatrix}

The matrix :math:`A_{ij}` shows the utility to the player controlling the rows
when they play the :math:`i` th row and their opponent (the column player) plays
the :math:`j` th column. For example, if the row player played Scissors (the 3rd
strategy) and the column player played Paper (the 2nd strategy) then the row
player gets: :math:`A_{32}=1` because Scissors cuts Paper.

A recommend text book on Game Theory is [Maschler2013]_.

Installing Nashpy
-----------------

We are going to study this game using Nashpy, first though we need to install
it. Nasphy requires the following things to be on your computer:

- Python 3.5 or greater;
- Scipy 0.19.0 or greater;
- Numpy 1.12.1 or greater.

Assuming you have those installed, to install Nashpy:

- On Mac OSX or linux open a terminal;
- On Windows open the Command prompt or similar

and type::

    $ python -m pip install nashpy

If this does not work, you might not have Python or one of the other
dependencies. You might also have problems due to :code:`pip` not being
recognised. To overcome these, using the `Anaconda
<https://www.continuum.io/downloads>`_ distribution of Python
is recommended as it installs straightforwardly on all operating systems and
also includes the libraries needed to run :code:`Nashpy`.

Creating a game
---------------

We can create this game using Nashpy::

    >>> import nashpy as nash
    >>> import numpy as np
    >>> A = np.array([[0, -1, 1], [1, 0, -1], [-1, 1, 0]])
    >>> rps = nash.Game(A)
    >>> rps
    Zero sum game with payoff matrices:
    <BLANKLINE>
    Row player:
    [[ 0 -1  1]
     [ 1  0 -1]
     [-1  1  0]]
    <BLANKLINE>
    Column player:
    [[ 0  1 -1]
     [-1  0  1]
     [ 1 -1  0]]


The string representation of the game also contains some information. For
example, it is also showing the matrix that corresponds to the utility of the
column player. In this case that is :math:`-A` but that does not always
have to be the case.

We can in fact pass a pair of matrices to the game class to create the same
game::

    >>> B = - A
    >>> rps = nash.Game(A, B)
    >>> rps
    Zero sum game with payoff matrices:
    <BLANKLINE>
    Row player:
    [[ 0 -1  1]
     [ 1  0 -1]
     [-1  1  0]]
    <BLANKLINE>
    Column player:
    [[ 0  1 -1]
     [-1  0  1]
     [ 1 -1  0]]

We get the exact same game, if passed a single game, :code:`Nashpy` will assume
that the game is a *zero sum game*: in other words the utilities of both players
are opposite.

Calculating the utility of a pair of strategies
-----------------------------------------------

If the row player played Scissors (the 3rd
strategy) and the column player played Paper (the 2nd strategy) then the row
player gets: :math:`A_{32}=1` because Scissors cuts Paper.

A mathematical approach to representing a strategy is to consider a vector of
the size: the number of strategies. For example :math:`\sigma_r=(0, 0, 1)` is
the row strategy where the row player always plays their third strategy.
Similarly :math:`\sigma_c=(0, 1, 0)` is the strategy for the column player where
they always play their second strategy.

When we represent strategies like this we can get the utility to the row player
using the following linear algebraic expression:

.. math::

   \sigma_r A \sigma_c^T

Similarly, if :math:`B` is the utility to the column player their utility is
given by:

.. math::

   \sigma_r B \sigma_c^T


We can use Nashpy to find these utilities::

    >>> sigma_r = [0, 0, 1]
    >>> sigma_c = [0, 1, 0]
    >>> rps[sigma_r, sigma_c]
    array([ 1, -1])

Players can choose to play randomly, in which case the utility
corresponds to the long term average. This is where our representation of
strategies and utility calculations becomes particularly useful. For example,
let us assume the column player decides to play Rock and Paper "randomly". This
corresponds to :math:`\sigma_c=(1/2, 1/2, 0)`::

    >>> sigma_c = [1 / 2, 1 / 2, 0]
    >>> rps[sigma_r, sigma_c]
    array([0., 0.])

The row player might then decide to change their strategy and "randomly" play
Paper and Scissors::

    >>> sigma_r = [0, 1 / 2, 1 / 2]
    >>> rps[sigma_r, sigma_c]
    array([ 0.25, -0.25])

The column player would then probably deviate once more. Whether or not their is
a pair of strategies for both players at which they both no longer have a reason
to move is going to be answered in the next section.

Computing Nash equilibria
-------------------------

Nash equilibria is (in two player games) a pair of strategies at which both
players do not have an incentive to deviate. We can find these using
:code:`Nashpy`::

    >>> eqs = rps.support_enumeration()
    >>> list(eqs)
    [(array([0.333..., 0.333..., 0.333...]), array([0.333..., 0.333..., 0.333...]))]

*Nash* equilibria is an important concept as it allows to gain an initial
understanding of emergent behaviour in complex systems.

Learning in games
-----------------

Nash equilibria are not always observed during non cooperative play: they
correspond to strategies at which no play has an incentive to move but that does
not necessarily imply that players can arrive at that equilibria naturally.

We can illustrate this using :code:`Nashpy`::

    >>> import numpy as np
    >>> iterations = 100
    >>> np.random.seed(0)
    >>> play_counts = rps.fictitious_play(iterations=iterations)
    >>> for row_play_count, column_play_count in play_counts:
    ...     print(row_play_count, column_play_count)
    [0 0 0] [0 0 0]
    [1. 0. 0.] [0. 1. 0.]
    ...
    [28. 39. 32.] [37. 26. 36.]
    [29. 39. 32.] [37. 26. 37.]

Over time we can see the behaviour emerge, as the play counts can be normalised
to give strategy vectors. Note that these will not always converge.
