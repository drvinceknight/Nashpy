"""A class for a Regret Minimization algorithm"""

import numpy as np
from typing import Generator, Tuple, Any
import numpy.typing as npt


def compute_regrets(strategy_utilities, current_strategy):
    """
    This function calculates the regrets for a player based on the strategy utilities and the current strategy.
    Regrets represent the difference between the utility achieved by playing a strategy and the maximum utility
    that could have been achieved by playing any strategy.
    In this implementation, only positive regrets are considered

    Parameters
    ----------
    strategy_utilities : array
        Player New Strategy matrix
    current_strategy : array
        Player Current Strategy matrix


    Returns
    -------
    regrets
        Regret for the Strategies chosen.
    """
    regrets = np.maximum(0, strategy_utilities - current_strategy)
    return regrets


def update_strategy(current_strategy, regrets, learning_rate):
    """
    This function updates the player's strategy based on the regrets, the current strategy, and a fixed learning rate.
    It scales the regrets by the learning rate and adds them to the current strategy.
    Finally, it normalizes the updated strategy to ensure that the probabilities sum up to 1.

    Parameters
    ----------
    current_strategy : array
        Player Current Strategy matrix
    regrets : array
        Player Current Strategy matrix
    learning_rate: float ( Optional Defaulted to 0.1 )
        The  learning_rate determines the magnitude of the update towards the regrets
        The learning rate scales the regrets before they are added to the current strategy.
        A higher learning rate results in a larger update, while a lower learning rate leads to a smaller update.
        This value allows you to control the pace towards a Nash equilibrium.

    Returns
    -------
    latest_strategy:  arrary
        latest_strategy is the average of the updates strategy
    """
    updated_strategy = current_strategy + learning_rate * regrets
    latest_strategy = updated_strategy / np.sum(updated_strategy)
    return latest_strategy


def generate_abs_strategy(strategy_list):
    """
    This function will return most favorable utility by a player based on the max probability value.
    Will take only one variable, strategy_list as the input

    Parameters
    ----------
    strategy_list : array
        Array of strategy list to be updated with an absolute value

    Returns
    -------
    favorable_strategy : Absolute stratedy by removing the fractions
    """
    max_probability = max(strategy_list)
    strategy_relative = [1 if x == max_probability else 0 for x in strategy_list]
    sum_value_in_the_list = sum(strategy_relative)
    favorable_strategy = [x / sum_value_in_the_list for x in strategy_relative]
    return favorable_strategy


def regret_minimization(
    A: npt.NDArray, B: npt.NDArray, learning_rate=0.1, iterations=100
) -> Generator[Tuple[float, float], Any, None]:
    """
    Obtain the Nash equilibria using regret minimization method using N number of itreations.
    The code provided is based on the concept of regret matching,
    with the fixed learning rate.

    Algorithm implemented here is Algorithm 4.3 Theorem 4.4 of [Nisan2007]_

    1. Build best Strategies probability of both players

    Parameters
    ----------
    A : array
        The row player utility matrix.
    B : array
        The column player utility matrix

    learning_rate : float ( Optional Defaulted to 0.1 )
        The  learning_rate determines the magnitude of the update towards the regrets
        The learning rate scales the regrets before they are added to the current strategy.
        A higher learning rate results in a larger update, while a lower learning rate leads to a smaller update.
        This value allows you to control the pace towards a Nash equilibrium.

    iterations : Integer ( Optional Defaulted to 100 )
        This value is defaulted to 100 itrations, this number could be modified to a larger or smaller number based on the untilities/payoff matrix shape


    Yields
    -------
    Generator
        The equilibria.
    """
    num_strategies_1, num_strategies_2 = A.shape
    strategy_A = np.ones(num_strategies_1) / num_strategies_1
    strategy_B = np.ones(num_strategies_2) / num_strategies_2

    for itration_num in range(iterations):
        strategy_utilities_A = np.dot(A, strategy_B)
        strategy_utilities_B = np.dot(B, strategy_A)

        regrets_A = compute_regrets(strategy_utilities_A, strategy_A)
        regrets_B = compute_regrets(strategy_utilities_B, strategy_B)

        strategy_A = update_strategy(strategy_A, regrets_A, learning_rate)
        strategy_B = update_strategy(strategy_B, regrets_B, learning_rate)

    strategy_A_final = generate_abs_strategy(strategy_A)
    strategy_B_final = generate_abs_strategy(strategy_B)

    yield strategy_A_final, strategy_B_final
