"""Code to carry out replicator dynamics"""
import numpy as np
from scipy.integrate import odeint

def get_derivative_of_fitness(x, t, A):
    """
    Find the derivative of fitness function
    """
    f = np.dot(A, x)
    phi = np.dot(f, x)
    return x * (f - phi)


def replicator_dynamics(A, y0, timepoints):
    """
    Implement replicator dynamics
    """
    xs = odeint(func=get_derivative_of_fitness, y0=y0, t=timepoints, args=(A,))
    return xs 