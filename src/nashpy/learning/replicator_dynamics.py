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


def get_xs_over_time(get_derivative_of_fitness, epsilon, t, A):
    xs = odeint(func=get_derivative_of_fitness, y0=[1 - epsilon, epsilon], t=t, args=(A,))
    return xs