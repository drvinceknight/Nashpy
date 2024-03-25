"""A class for a normal form game"""

import numpy as np
import numpy.typing as npt
from typing import Optional, Any
from .algorithms.lemke_howson import lemke_howson
from .algorithms.support_enumeration import support_enumeration
from .algorithms.vertex_enumeration import vertex_enumeration
from .linalg.minimax import linear_program
from .egt.moran_process import moran_process, fixation_probabilities
from .learning.fictitious_play import fictitious_play
from .learning.replicator_dynamics import (
    asymmetric_replicator_dynamics,
    replicator_dynamics,
)
from .learning.stochastic_fictitious_play import stochastic_fictitious_play
from .utils.is_best_response import is_best_response
from .learning.regret_minimization import regret_minimization
from .learning.imitation_dynamics import imitation_dynamics


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

    def __init__(self, *args: Any) -> None:
        if len(args) == 2:
            if (not len(args[0]) == len(args[1])) or (
                not len(args[0][0]) == len(args[1][0])
            ):
                raise ValueError("Unequal dimensions for matrices A and B")
            self.payoff_matrices = tuple([np.asarray(m) for m in args])
        if len(args) == 1:
            self.payoff_matrices = np.asarray(args[0]), -np.asarray(args[0])
        self.zero_sum = np.array_equal(
            self.payoff_matrices[0], -self.payoff_matrices[1]
        )

    def __repr__(self) -> str:
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

    def __getitem__(self, key: Any) -> npt.NDArray:
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
        generator
            The equilibria.
        """
        return vertex_enumeration(*self.payoff_matrices)

    def support_enumeration(self, non_degenerate=False, tol=10**-16):
        """
        Obtain the Nash equilibria using support enumeration.

        Algorithm implemented here is Algorithm 3.4 of [Nisan2007]_.

        1. For each k in 1...min(size of strategy sets)
        2. For each I,J supports of size k
        3. Solve indifference conditions
        4. Check that have Nash Equilibrium.

        Parameters
        ----------
        non_degenerate : bool
            Whether or not to consider supports of equal size. By default
            (False) only considers supports of equal size.
        tol : float
            A tolerance parameter for equality.

        Returns
        -------
        generator
            The equilibria.
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

        Yields
        ------
        Tuple
            An equilibria
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
            The initial dropped label.

        Returns
        -------
        Tuple
            An equilibria
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
        iterations : int
            The number of iterations of the algorithm.
        play_counts : array
            The play counts.

        Returns
        -------
        Generator
            The play counts
        """
        return fictitious_play(
            *self.payoff_matrices, iterations=iterations, play_counts=play_counts
        )

    def stochastic_fictitious_play(
        self, iterations, play_counts=None, etha=10**-1, epsilon_bar=10**-2
    ):
        """Return a given sequence of actions and mixed strategies through stochastic fictitious play. The
        implementation corresponds to the description given in [Hofbauer2002]_.


        Parameters
        ----------
        iterations : int
            The number of iterations of the algorithm.
        play_counts : array
            The play counts.
        etha : float
            The noise parameter for the logit choice function.
        epsilon_bar : float
            The maximum stochastic perturbation.

        Returns
        -------
        Generator
            The play counts
        """
        return stochastic_fictitious_play(
            *self.payoff_matrices,
            iterations=iterations,
            play_counts=play_counts,
            etha=etha,
            epsilon_bar=epsilon_bar
        )

    def replicator_dynamics(self, y0=None, timepoints=None, mutation_matrix=None):
        """
        Implement replicator dynamics
        Return an array showing probability of each strategy being played over
        time.
        The total population is constant. Strategies can either stay constant
        if equilibria is achieved, replicate or die.

        Parameters
        ----------
        y0 : array
            The initial population distribution.
        timepoints: array
            The iterable of timepoints.
        mutation_matrix : array
            The mutation rate matrix. Element [i, j] gives the probability of an
            individual of type i mutating to an individual of type j. Default
            behaviour is to be the identity matrix which corresponds to no mutation.

        Returns
        -------
        array
            The population distributions over time.
        """
        A, _ = self.payoff_matrices
        return replicator_dynamics(
            A=A, y0=y0, timepoints=timepoints, mutation_matrix=mutation_matrix
        )

    def asymmetric_replicator_dynamics(self, x0=None, y0=None, timepoints=None):
        """
        Returns two arrays, corresponding to the two players, showing the
        probability of each strategy being played over time using the asymmetric
        replicator dynamics algorithm.

        Parameters
        ----------
        x0 : array
            The initial population distribution of the row player.
        y0 : array
            The initial population distribution of the column player.
        timepoints: array
            The iterable of timepoints.

        Returns
        -------
        Tuple
            The 2 population distributions over time.
        """
        A, B = self.payoff_matrices
        return asymmetric_replicator_dynamics(
            A=A, B=B, x0=x0, y0=y0, timepoints=timepoints
        )

    def is_best_response(self, sigma_r, sigma_c):
        """
        Checks if sigma_r is a best response to sigma_c  and vice versa.

        Parameters
        ----------
        sigma_r : array
            The row player strategy
        sigma_c : array
            The column player strategy

        Returns
        -------
        tuple
            A pair of booleans, the first indicates if sigma_r is a best
            response to sigma_c. The second indicates if sigma_c is a best
            response to sigma_r.
        """
        A, B = self.payoff_matrices
        is_row_strategy_best_response = is_best_response(
            A=A,
            sigma_c=sigma_c,
            sigma_r=sigma_r,
        )
        is_column_strategy_best_response = is_best_response(
            A=B.T,
            sigma_c=sigma_r,
            sigma_r=sigma_c,
        )
        return (is_row_strategy_best_response, is_column_strategy_best_response)

    def moran_process(
        self,
        initial_population,
        mutation_probability=0,
        replacement_stochastic_matrix: Optional[npt.NDArray] = None,
        interaction_graph_adjacency_matrix: Optional[npt.NDArray] = None,
    ):
        """
        Return a generator of population across the Moran process. The last
        population is when only a single type of individual is present in the
        population.

        Parameters
        ----------
        initial_population : array
            the initial population
        mutation_probability : float
            the probability of an individual selected to be copied mutates to
            another individual from the original set of strategies (even if they are
            no longer present in the population).
        replacement_stochastic_matrix: array
            Individual i chosen for replacement will replace individual j with
            probability P_{ij}.
            Default is None: this is equivalent to P_{ij} = 1 / N for all i, j.
        interaction_graph_adjacency_matrix : array
            the adjacency matrix for the interaction graph G: individuals of type i
            interact with individuals of type j count towards fitness iff G_{ij} =
            1.  Default is None: if so a complete graph is used -- this corresponds
            to all individuals interacting with each other (with no self
            interactions)


        Returns
        -------
        Generator
            The generations.
        """
        A, _ = self.payoff_matrices
        return moran_process(
            A=A,
            initial_population=initial_population,
            mutation_probability=mutation_probability,
            interaction_graph_adjacency_matrix=interaction_graph_adjacency_matrix,
            replacement_stochastic_matrix=replacement_stochastic_matrix,
        )

    def fixation_probabilities(
        self,
        initial_population,
        repetitions,
        replacement_stochastic_matrix: Optional[npt.NDArray] = None,
        interaction_graph_adjacency_matrix: Optional[npt.NDArray] = None,
    ):
        """
        Return the fixation probabilities for all types of individuals.

        The returned array will have the same dimension as the number of rows or
        columns as the payoff matrix A. The ith element of the returned array
        corresponds to the probability that the ith strategy becomes fixed given the
        initial population.

        This is a stochastic algorithm and the probabilities are estimated over a
        number of repetitions.

        Parameters
        ----------
        initial_population : array
            the initial population
        repetitions : int
            The number of iterations of the algorithm.
        replacement_stochastic_matrix: array
            Individual i chosen for replacement will replace individual j with
            probability P_{ij}.
            Default is None: this is equivalent to P_{ij} = 1 / N for all i, j.
        interaction_graph_adjacency_matrix : array
            the adjacency matrix for the interaction graph G: individuals of type i
            interact with individuals of type j count towards fitness iff G_{ij} =
            1.  Default is None: if so a complete graph is used -- this corresponds
            to all individuals interacting with each other (with no self
            interactions)



        Returns
        -------
        array
            The fixation probability of each type.
        """
        A, _ = self.payoff_matrices
        return fixation_probabilities(
            A=A,
            initial_population=initial_population,
            repetitions=repetitions,
            interaction_graph_adjacency_matrix=interaction_graph_adjacency_matrix,
            replacement_stochastic_matrix=replacement_stochastic_matrix,
        )

    def linear_program(self):
        """
        Returns the Nash Equilibrium for a zero sum game by solving the Linear
        Program that corresponds to the minimax theorem.

        Returns
        -------
        tuple
            The Nash equilibria
        Raises
        ------
        ValueError
            A value error is raised if the game is not zero sum
        """
        if self.zero_sum is False:
            raise ValueError(
                "The Linear Program corresponding to the minimax theorem is defined only for Zero Sum games."
            )
        A, B = self.payoff_matrices
        row_strategy = linear_program(row_player_payoff_matrix=A)
        column_strategy = linear_program(row_player_payoff_matrix=B.T)
        return row_strategy, column_strategy

    def regret_minimization(self, learning_rate=0.1, iterations=100):
        """
        Obtain the Nash equilibria using regret minimization method using N number of itreations.
        The code provided is based on the concept of regret matching,
        with the fixed learning rate.

        Algorithm implemented here is Algorithm 4.3 Theorem 4.4 of [Nisan2007]_

        1. Build best Strategies probability of both players

        Parameters
        ----------
        learning_rate : float
            The  learning_rate determines the magnitude of the update towards the regrets

        iterations : Integer
            This value is defaulted to 100 itrations, this number could be modified to a larger or smaller number based on the untilities/payoff matrix shape

        Returns
        -------
        Generator
            The equilibria.
        """
        A, B = self.payoff_matrices
        return regret_minimization(
            A=A, B=B, learning_rate=learning_rate, iterations=iterations
        )

    def imitation_dynamics(
        self,
        population_size=100,
        iterations=1000,
        random_seed=None,
        threshold=0.5,
    ):
        """
        Simulate the imitation dynamics for a given game represented by payoff matrices A and B.

        Parameters
        ----------
        population_size : number
            number of individuals in the population of the group (default: 100)
        iterations : number
            number of generations to simulate (default: 1000)
        random_seed : number
            seed for reproducibility (default: None)
        threshold : float
            threshold value for representing strategies as 0 or 1 (default: 0.5)

        Returns
        -------
        Generator
            The equilibria.
        """
        A, B = self.payoff_matrices
        return imitation_dynamics(
            A=A,
            B=B,
            population_size=population_size,
            iterations=iterations,
            random_seed=random_seed,
            threshold=threshold,
        )
