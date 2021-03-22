"""Code to carry out replicator dynamics"""
import numpy as np

# from scipy.integrate import solve_ivp (will change program to use solve_ivp later)
from scipy.integrate import odeint


def get_derivative_of_fitness(x, t, A):
    """
    Find the derivative of fitness function
    """
    f = np.dot(A, x)
    phi = np.dot(f, x)
    return x * (f - phi)


def replicator_dynamics(A, y0=None, timepoints=None):
    """
    Implement replicator dynamics
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
    """
    separator = A.shape[0]
    x1 = x[:separator]
    x2 = x[separator:]

    f1 = np.dot(A, x2)
    f2 = np.dot(x1, B)

    phi1 = np.dot(f1, x1)
    phi2 = np.dot(f2, x2)

    x1_derivative = x1 * (f1 - phi1)
    x2_derivative = x2 * (f2 - phi2)

    return np.concatenate((x1_derivative, x2_derivative))


def asymmetric_replicator_dynamics(A, B, x0=None, y0=None, timepoints=None):
    """
    Implement asymmetric replicator dynamics
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
    xs1 = np.array([iter[: A.shape[0]] for iter in xs])
    xs2 = np.array([iter[A.shape[0] :] for iter in xs])
    return xs1, xs2
