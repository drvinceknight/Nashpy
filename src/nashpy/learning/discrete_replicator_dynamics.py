"""Code to carry out discrete replicator dynamics"""

import numpy as np
import numpy.typing as npt


def greenwood_quantize(
    k: npt.NDArray,
    N: int,
):
    """
    rounds populations to nearest integer while keeping total population consistent
    called after each discrete step.
    useful for modeling a finite population of players who can only use pure stratergies

    Parameters
    ----------
    k : array
        non-integer population vector
    N : int
        size of array x
    Returns
    ----------
    array
        integer population vector
    """
    int_k = np.floor(k + 1 / 2)

    Ndash = np.sum(int_k)
    d = int(Ndash - N)

    if d != 0:
        errors = int_k - k
        if d > 0:
            error_index = np.argpartition(errors, -d)[-d:]
            int_k[(error_index)] = int_k[(error_index)] - 1
            return int_k

        if d < 0:
            error_index = np.argpartition(errors, d)[d:]
            int_k[(error_index)] = int_k[(error_index)] + 1
            return int_k

    return int_k


def type_1_discrete_step(x: npt.NDArray, A: npt.NDArray):
    """
    performs type 1 discrete step on population x

    this type of discrete replicator dynamics equation is equivilent to a Euler step of the continuous replicator dynamics equation with step size 1.

    x[t+1]=x[t] + (step_size) * x [payoff_x - average_payoff]

    Parameters
    ----------
    x : array
        the normalised population distribution

    A : array
        the payoff matrix
    Returns
    ----------
    array
        integer population vector
    """

    f = np.matvec(A, (x))

    return x + x * ((f) - (f @ x))


def type_2_discrete_step(x: npt.NDArray, A: npt.NDArray):
    """
    performs type 2 discrete step on population x

    Parameters
    ----------
    x : array
        the normalised population distribution

    A : array
         the payoff matrix
    Returns
    ----------
    array
        integer population vector
    """

    f = np.matvec(A, (x))

    return x * ((f) / (f @ x))


def discrete_replicator_dynamics(
    A,
    x,
    steps=1,
    quantize=False,
    step_function=type_2_discrete_step,
):
    """
    Implement discrete replicator dynamics

    Parameters
    ----------
    A : array
        the payoff matrix

    x : array
        the normalised population distribution

    steps : int
        number of iterations to run the step function

    quantize : bool
        toggles the qantization algorithm

    step_function : function
        determines which function to use per discrete time step

    Returns
    ----------
    array
        integer population vector
    """

    x_over_time = np.zeros((steps, len(x)))
    N = sum(x)
    x = x / N

    for i in range(steps):
        x = step_function(x, A)

        if quantize:
            x = greenwood_quantize(x * N, N)
            x = x / N

        x_over_time[i] = x * N

    return x_over_time
