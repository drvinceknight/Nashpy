"""A class for a normal form game"""
from itertools import combinations

import numpy as np

from .algorithms.lemke_howson import lemke_howson
from .algorithms.lemke_howson_lex import lemke_howson_lex
from .algorithms.support_enumeration import support_enumeration
from .algorithms.vertex_enumeration import vertex_enumeration
from .learning.fictitious_play import fictitious_play
from .learning.replicator_dynamics import replicator_dynamics


class Game:
    """
    A class for a normal form game.

    Parameters
    ----------

        - A, B: 2 dimensional list/arrays representing the payoff matrices for
          non zero sum games.
        - A: 2 dimensional list/array representing the payoff matrix for a
          zero sum game.
    """

    def __init__(self, *args):
        if len(args) == 2:
            self.payoff_matrices = tuple([np.asarray(m) for m in args])
        if len(args) == 1:
            self.payoff_matrices = np.asarray(args[0]), -np.asarray(args[0])
        self.zero_sum = np.array_equal(
            self.payoff_matrices[0], -self.payoff_matrices[1]
        )

    def __repr__(self):
        if self.zero_sum:
            tpe = "Zero sum"
        else:
            tpe = "Bi matrix"
        return """{} game with payoff matrices:

Row player:
{}

Column player:
{}""".format(
            tpe, *self.payoff_matrices
        )

    def __getitem__(self, key):
        row_strategy, column_strategy = key
        return np.array(
            [
                np.dot(row_strategy, np.dot(m, column_strategy))
                for m in self.payoff_matrices
            ]
        )

    def vertex_enumeration(self):
        """
        Obtain the Nash equilibria using enumeration of the vertices of the best
        response polytopes.

        Algorithm implemented here is Algorithm 3.5 of [Nisan2007]_.

        1. Build best responses polytopes of both players
        2. For each vertex pair of both polytopes
        3. Check if pair is fully labelled
        4. Return the normalised pair

        Returns
        -------

            equilibria: A generator.
        """
        return vertex_enumeration(*self.payoff_matrices)

    def support_enumeration(self, non_degenerate=False, tol=10 ** -16):
        """
        Obtain the Nash equilibria using support enumeration.

        Algorithm implemented here is Algorithm 3.4 of [Nisan2007]_.

        1. For each k in 1...min(size of strategy sets)
        2. For each I,J supports of size k
        3. Solve indifference conditions
        4. Check that have Nash Equilibrium.

        Returns
        -------

            equilibria: A generator.
        """
        return support_enumeration(
            *self.payoff_matrices, non_degenerate=non_degenerate, tol=tol
        )

    def lemke_howson_enumeration(self):
        """
        Obtain Nash equilibria for all possible starting dropped labels
        using the lemke howson algorithm. See `Game.lemke_howson` for more
        information.

        Note: this is not guaranteed to find all equilibria.

        Returns
        -------

            equilibria: A generator
        """
        for label in range(sum(self.payoff_matrices[0].shape)):
            yield self.lemke_howson(initial_dropped_label=label)

    def lemke_howson(self, initial_dropped_label):
        """
        Obtain the Nash equilibria using the Lemke Howson algorithm implemented
        using integer pivoting.

        Algorithm implemented here is Algorithm 3.6 of [Nisan2007]_.

        1. Start at the artificial equilibrium (which is fully labeled)
        2. Choose an initial label to drop and move in the polytope for which
           the vertex has that label to the edge
           that does not share that label. (This is implemented using integer
           pivoting)
        3. A label will now be duplicated in the other polytope, drop it in a
           similar way.
        4. Repeat steps 2 and 3 until have Nash Equilibrium.

        Parameters
        ----------

            initial_dropped_label: int

        Returns
        -------

            equilibria: A tuple.
        """
        return lemke_howson(
            *self.payoff_matrices, initial_dropped_label=initial_dropped_label
        )

    def fictitious_play(self, iterations, play_counts=None):
        """
        Return a given sequence of actions through fictitious play. The
        implementation corresponds to the description of chapter 2 of
        [Fudenberg1998]_.

        1. Players have a belief of the strategy of the other player: a vector
        representing the number of times the player has chosen a given strategy.
        2. Players choose a best response to the belief.
        3. Players update their belief based on the latest choice of the
        opponent.

        Parameters
        ----------

            iterations: int
            play_counts: iterator

        Returns
        -------

            plays: A generator
        """
        return fictitious_play(
            *self.payoff_matrices,
            iterations=iterations,
            play_counts=play_counts
        )

    def replicator_dynamics(self, y0=None, timepoints=None):
        """
        Implement replicator dynamics
        Return an array showing probability of each strategy being played over
        time.
        The total population is constant. Strategies can either stay constant
        if equilibria is achieved, replicate or die.

        Parameters
        ----------
            A: nxm array, where n=m
            y0: array
            timepoints: array
        Returns
        -------
            xs: array
        """
        A, _ = self.payoff_matrices
        return replicator_dynamics(A=A, y0=y0, timepoints=timepoints)
