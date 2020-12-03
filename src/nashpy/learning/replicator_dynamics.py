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


def replicator_dynamics(A, y0, timepoints=None):
    """
    Implement replicator dynamics
    """
    if timepoints is None:
        timepoints = np.linspace(0, 10, 1000)

    if y0 is None:
        y0 = np.zeros((len(A),))
        for i in range(len(A)):
            y0[i]= 1/len(A)
            
    xs = odeint(func=get_derivative_of_fitness, y0=y0, t=timepoints, args=(A,))
    return xs 