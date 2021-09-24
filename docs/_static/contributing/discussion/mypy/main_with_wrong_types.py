from typing import Iterable


def get_mean(collection: Iterable) -> float:
    """
    Obtain the average of a collection of objects.

    Parameters
    ----------
    collection : Iterable
        A list of numbers

    Returns
    -------
    float
        The mean of the numbers.
    """
    return sum(collection) / len(collection)
