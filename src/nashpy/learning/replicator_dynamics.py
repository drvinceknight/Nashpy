"""Code to carry out replicator dynamics"""
import numpy as np

# from scipy.integrate import solve_ivp (will change program to use solve_ivp later)
from scipy.integrate import odeint


def get_derivative_of_fitness(x, t, A):
    """
    Find the derivative of fitness function

    Parameters
    ----------
    x : array
        A population distribution.
    t : float
        A time point. This is not actually used but is needed in the function
        signature.
    A : array
        The payoff matrix

    Returns
    -------
    array
        The derivative of the population distribution.
    """
    f = np.dot(A, x)
    phi = np.dot(f, x)
    return x * (f - phi)


def replicator_dynamics(A, y0=None, timepoints=None):
    """
    Implement replicator dynamics

    Parameters
    ----------
    A : array
        The payoff matrix
    y0 : array
        The initial population distribution.
    timepoints: array
        The iterable of timepoints.

    Returns
    -------
    array
        The population distributions over time.
    """

    if timepoints is None:
        timepoints = np.linspace(0, 10, 1000)

    if y0 is None:
        number_of_strategies = len(A)
        y0 = np.ones(number_of_strategies) / number_of_strategies

    xs = odeint(func=get_derivative_of_fitness, y0=y0, t=timepoints, args=(A,))
    return xs


def get_derivative_of_asymmetric_fitness(x, t, A, B):
    """
    Find the derivative of fitness function for the asymmetric replicator
    dynamics scenario

    Parameters
    ----------
    x : array
        A vector combining both population distributions.
    t : float
        A time point. This is not actually used but is needed in the function
        signature.
    A : array
        The row player payoff matrix
    B : array
        The column player payoff matrix

    Returns
    -------
    array
        The derivative of both population distributions.
    """
    number_of_rows = A.shape[0]
    row_vector = x[:number_of_rows]
    col_vector = x[number_of_rows:]

    f1 = A @ col_vector
    f2 = row_vector @ B

    phi1 = f1 @ row_vector
    phi2 = f2 @ col_vector

    row_derivative = row_vector * (f1 - phi1)
    col_derivative = col_vector * (f2 - phi2)

    return np.concatenate((row_derivative, col_derivative))


def asymmetric_replicator_dynamics(A, B, x0=None, y0=None, timepoints=None):
    """
    Implement asymmetric replicator dynamics

    Parameters
    ----------
    A : array
        The row player payoff matrix
    B : array
        The column player payoff matrix
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
    if timepoints is None:
        timepoints = np.linspace(0, 10, 1000)

    if x0 is None:
        number_of_strategies_A = A.shape[0]
        x0 = np.ones(number_of_strategies_A) / number_of_strategies_A

    if y0 is None:
        number_of_strategies_B = A.shape[1]
        y0 = np.ones(number_of_strategies_B) / number_of_strategies_B

    initial_values = np.concatenate((x0, y0))
    xs = odeint(
        func=get_derivative_of_asymmetric_fitness,
        y0=initial_values,
        t=timepoints,
        args=(
            A,
            B,
        ),
    )
    xs1 = xs[:, : A.shape[0]]
    xs2 = xs[:, A.shape[0] :]
    return xs1, xs2
