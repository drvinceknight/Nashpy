"""Code to carry out discrete replicator dynamics"""

import numpy as np
import numpy.typing as npt


def greenwood_quantize(
    k: npt.NDArray,
    N: int,
):
    """
    rounds populations to nearest integer while keeping total population consistent

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
    int_k = np.zeros(k.shape)
    for i in range(0, len(k)):
        int_k[i] = np.floor((k[i]) + 1 / 2)

    Ndash = np.sum(int_k)
    d = int(Ndash - N)

    if d != 0:
        errors = np.zeros(k.shape)
        for i in range(0, len(k)):
            errors[i] = int_k[i] - k[i]
        errors_sorted = np.sort(errors)

        if d > 0:
            for i in range(0, d):
                error_location = (np.where(errors == (errors_sorted[i])))[0][0]
                int_k[error_location] -= 1
                errors[error_location] = 0
                errors_sorted[i] = 0

        if d < 0:
            for i in range(0, -d):
                error_location = (np.where(errors == (errors_sorted[-i])))[0][0]
                int_k[error_location] += 1
                errors[error_location] = 0
                errors_sorted[-i] = 0

    return int_k


def type_1_discrete_step(x: npt.NDArray, A: npt.NDArray):
    """
    this version of discrete replicator dynamics is equivilent to a Euler step of the continuous replicator dynamics equation with step size 1.

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

    Ax = np.matvec(A, (x))

    return x + x * ((Ax) - (np.dot(Ax, (x))))


def type_2_discrete_step(x: npt.NDArray, A: npt.NDArray):
    """
    FILL IN THIS DOCSTRING

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

    Ax = np.matvec(A, (x))

    return x * ((Ax) / (np.dot(Ax, (x))))  # NEW_X NOT NORMALISED


def discrete_replicator_dynamics(
    x,
    A,
    steps=1,
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

    step_function : function
        determines which function to use per discrete time step

    Returns
    ----------
    array
        integer population vector
    """

    # data verification
    # check values sum < infinity

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
