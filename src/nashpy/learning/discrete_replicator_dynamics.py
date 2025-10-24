import numpy as np
import numpy.typing as npt
from typing import Optional, Tuple


def greenwood_quantize(
    k: npt.NDArray,
    N: int,
):
    """
    rounds populations to nearest intager while keeping total population consistent

    Parameters
        ----------
        x : array
            non-intager population vector
        N : int
            size of array x
    Returns
        ----------
        array
            intager population vector
    """
    int_k = np.zeros(k.shape)
    for i in range(0, len(k)):
        int_k[i] = np.floor((k[i]) + 1 / 2)

    Ndash = np.sum(k)
    d = int(Ndash - N)

    if d == 0:
        return int_k
    else:
        errors = np.zeros(k.shape)  # calculate errors
        for i in range(0, len(k)):
            errors[i] = int_k[i] - k[i]
        errors_sorted = np.sort(errors)

        if d > 0:
            for i in range(0, d):  # decrement ki with largest error value
                int_k[(np.where(errors == (errors_sorted[i])))[0][0]] -= 1

            return int_k

        if d < 0:
            for i in range(0, -d):  # increment ki with smallest error value
                int_k[(np.where(errors == (errors_sorted[-i])))[0][0]] += 1

            return int_k


def type_1_discrete_step(x, A):
    """
    this is one eular step of the regular replicator dynmaics function...
    
    Parameters
        ----------
        A : array
            the payoff matrix

        x : array
            the normalised population distribution

    Returns
        ----------
        array
            intager population vector
    """

    Ax = np.matvec(A, (x))

    return x + x * ((Ax) - (np.dot(Ax, (x))))  # NEW_X NOT NORMALISED


def type_2_discrete_step(x, A):
    """
    FILL IN THIS DOCSTRING

    Parameters
        ----------
        A : array
            the payoff matrix

        x : array
            the normalised population distribution

    Returns
        ----------
        array
            intager population vector
    """

    Ax = np.matvec(A, (x))

    return x * ((Ax) / (np.dot(Ax, (x))))  # NEW_X NOT NORMALISED

def discrete_replicator_dynamics(
    x,
    A,
    steps,
    quantize=False,
    step_function=type_2_discrete_step,
):
    
    """
    FILL IN THIS DOCSTRING

    Parameters
        ----------
        x : array
            the normalised population distribution

        A : array
            the payoff matrix

        steps : int
            number of iterations to run the step function

        quantize : bool
            toggles the qantization algorithm

    Returns
        ----------
        array
            intager population vector
    """

    x_over_time = np.zeros((steps, len(x)))
    N = sum(x)
    x = x / N

    for i in range(0, steps):
        x = step_function(x, A)

        if quantize == True:
            x = greenwood_quantize(x * N, N)
            x = x / N

        x_over_time[i] = x * N

    return x_over_time