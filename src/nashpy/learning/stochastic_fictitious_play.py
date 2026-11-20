"""Code to carry out stochastic fictitious learning"""

import numpy as np
from nashpy.learning.fictitious_play import update_play_count
import numpy.typing as npt
from typing import Optional


def get_distribution_response_to_play_count(
    A: npt.NDArray,
    play_count: npt.NDArray,
    epsilon_bar: float,
    etha: float,
    *,
    rng: Optional[np.random.Generator] = None,
) -> int:
    """
    Obtain a mixed strategy as a probability distribution as a response to a given play count

    Parameters
    ----------
    A : array
        The utility matrix.
    play_count : array
        The play counts.
    etha : float
        The noise parameter for the logit choice function.
    epsilon_bar : float
        The maximum stochastic perturbation.
    rng : numpy.random.Generator, optional
        The random number generator used for payoff perturbations.

    Returns
    -------
    int
        The action that corresponds to the best response.

    Raises
    ------
    ValueError
        A value error is raised if the input matrix or logit parameter leads to
        non-finite probabilities.
    """
    rng = np.random.default_rng(rng)
    if np.sum(play_count) == 0:
        strategies = play_count + 1 / len(play_count)
    else:
        strategies = play_count / np.sum(play_count)
    utilities = A @ strategies
    noisy_utilities = utilities + rng.random(A.shape[0]) * epsilon_bar
    logits = etha**-1 * noisy_utilities
    # A common shift preserves the distribution and keeps exponentials at most one.
    weights = np.exp(logits - np.max(logits))
    logit_choice = weights / np.sum(weights)
    try:
        assert np.all(logit_choice < np.inf)
    except AssertionError:
        raise ValueError(
            f"""The matrix with values ranging from {np.min(A)} to {np.max(A)}
            leads to non-finite logit probabilities. Check the payoff values
            and the logit parameter."""
        )
    return logit_choice


def stochastic_fictitious_play(
    A, B, iterations, etha=10**-1, epsilon_bar=10**-2, play_counts=None, *, seed=None
):
    """Return a given sequence of actions and mixed strategies through stochastic fictitious play. The
    implementation corresponds to the description given in [Hofbauer2002]_.


    Parameters
    ----------
    A : array
        The row player payoff matrix
    B : array
        The column player payoff matrix
    iterations : int
        The number of iterations of the algorithm.
    play_counts : array
        The play counts.
    etha : float
        The noise parameter for the logit choice function.
    epsilon_bar : float
        The maximum stochastic perturbation.
    seed : int or numpy.random.Generator, optional
        A seed or generator for the local random number generator.

    Yields
    ------
    Generator
        The play counts
    """
    rng = np.random.default_rng(seed)
    if play_counts is None:
        play_counts = [np.array([0 for _ in range(dimension)]) for dimension in A.shape]

    distributions = None, None

    yield play_counts, distributions

    for _ in range(iterations):
        distributions = [
            get_distribution_response_to_play_count(
                A=matrix,
                play_count=play_count,
                etha=etha,
                epsilon_bar=epsilon_bar,
                rng=rng,
            )
            for matrix, play_count in zip((A, B.transpose()), play_counts[::-1])
        ]

        plays = [
            rng.choice(range(len(distribution)), p=distribution)
            for distribution in distributions
        ]

        play_counts = [
            update_play_count(play_count, play)
            for play_count, play in zip(play_counts, plays)
        ]
        yield play_counts, distributions
