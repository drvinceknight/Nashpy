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
