"""Code for implementation of Introspection dynamics"""

import numpy as np
import numpy.typing as npt
from scipy.special import expit, logsumexp

from typing import Optional, Generator


def introspection_dynamics_state_distribution(
    A: npt.NDArray, B: npt.NDArray, beta: float
) -> npt.NDArray:
    """
    Calculate the stationary distribution of introspection dynamics.

    Parameters
    ----------
    A : array
        The row player's payoff matrix.
    B : array
        The column player's payoff matrix, with the same shape as A.
    beta : float
        The finite, non-negative learning intensity.

    Returns
    -------
    array
        An array with the same shape as A. Entry (i, j) is the long-run
        probability of the row player choosing i and the column player choosing j.

    Raises
    ------
    ValueError
        If beta is not finite and non-negative, or the payoff matrices do not
        have finite entries, equal shapes and at least two actions per player.
    LinAlgError
        If the stationary equations are numerically singular. Large scaled
        payoff differences can cause transition probabilities to underflow.

    Notes
    -----
    Solve the balance equations of the Markov chain defined in [Couto2022]_
    by eliminating states using only non-negative transition rates
    [Grassmann1985]_.
    The calculation uses a dense matrix with one row and column per action pair.
    """
    A, B = np.asarray(A, dtype=float), np.asarray(B, dtype=float)
    if A.ndim != 2 or A.shape != B.shape or min(A.shape) < 2:
        raise ValueError(
            "Payoff matrices must have the same shape and at least two actions "
            "per player."
        )
    if not np.all(np.isfinite(A)) or not np.all(np.isfinite(B)):
        raise ValueError("Payoff matrices must contain finite payoffs.")
    if not np.isfinite(beta) or beta < 0:
        raise ValueError("The learning intensity must be finite and non-negative.")

    if beta == 0:
        return np.full(A.shape, 1 / A.size)

    number_of_rows, number_of_columns = A.shape
    number_of_states = A.size
    rates = np.zeros((number_of_states, number_of_states))
    for row, column in np.ndindex(A.shape):
        state = row * number_of_columns + column
        for alternative_row in range(number_of_rows):
            if alternative_row != row:
                destination = alternative_row * number_of_columns + column
                with np.errstate(over="ignore"):
                    payoff_change = beta * (A[alternative_row, column] - A[row, column])
                rates[state, destination] = expit(payoff_change) / (
                    2 * (number_of_rows - 1)
                )
        for alternative_column in range(number_of_columns):
            if alternative_column != column:
                destination = row * number_of_columns + alternative_column
                with np.errstate(over="ignore"):
                    payoff_change = beta * (B[row, alternative_column] - B[row, column])
                rates[state, destination] = expit(payoff_change) / (
                    2 * (number_of_columns - 1)
                )

    # Eliminate a state by distributing its incoming flow over its outgoing
    # destinations. Unlike a general linear solve, this avoids subtracting
    # nearly equal numbers when transitions are very unlikely.
    exit_rates = np.zeros(number_of_states)
    for state in range(number_of_states - 1, 0, -1):
        exit_rates[state] = rates[state, :state].sum()
        if exit_rates[state] == 0:
            raise np.linalg.LinAlgError(
                "Transition probabilities underflow; use a smaller beta."
            )
        rates[:state, :state] += np.outer(
            rates[:state, state], rates[state, :state] / exit_rates[state]
        )

    # Reconstruct relative weights in log space to avoid overflowing ratios
    # between the probabilities of rare and frequently visited states.
    log_weights = np.zeros(number_of_states)
    with np.errstate(divide="ignore"):
        for state in range(1, number_of_states):
            log_weights[state] = logsumexp(
                log_weights[:state] + np.log(rates[:state, state])
            ) - np.log(exit_rates[state])
    return np.exp(log_weights - logsumexp(log_weights)).reshape(A.shape)


def introspection_dynamics(
    A: npt.NDArray,
    B: npt.NDArray,
    number_of_iterations: int,
    beta: float,
    initial_actions: Optional[npt.NDArray[np.int64]] = None,
) -> Generator[npt.NDArray, None, None]:
    """
    Run introspection dynamics.

    Parameters
    ----------
    A : array
        a payoff matrix for the row player
    B : array
        a payoff matrix for the column player
    number_of_iterations : int
        the number of steps to simulate the process
    beta : float
        The learning intensity. A value of 0 indicates random choice of actions,
        a high value means a higher likelihood of choosing an action that gives
        a better payoff.
    initial_actions : array
        The indices of the actions chosen by both players.

    Yields
    ------
    Generator
        the actions chosen at each step by both players
    """
    number_of_actions = A.shape
    payoff_matrices = [A, B]
    players = [0, 1]
    action_spaces = [list(range(number_of_actions[player])) for player in players]
    if initial_actions is None:
        actions = np.array(
            [np.random.choice(action_space) for action_space in action_spaces]
        )
    else:
        actions = np.array(initial_actions)

    yield actions

    for _ in range(number_of_iterations):
        player = np.random.choice(players)

        payoff_matrix = payoff_matrices[player]
        current_score = payoff_matrix[actions[0]][actions[1]]
        current_action = actions[player]

        action_space = action_spaces[player]
        potential_action_space = [
            action for action in action_space if action != current_action
        ]

        potential_action = np.random.choice(potential_action_space)
        potential_actions = np.array(
            [
                action if i != player else potential_action
                for i, action in enumerate(actions)
            ]
        )
        potential_score = payoff_matrix[potential_actions[0]][potential_actions[1]]
        delta = potential_score - current_score

        probability_of_change = 1 / (1 + np.exp(-beta * delta))

        if np.random.random() < probability_of_change:
            actions = potential_actions

        yield actions
