"""Code for implementation of Introspection dynamics"""

import numpy as np
import numpy.typing as npt

from typing import Optional, Generator


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
