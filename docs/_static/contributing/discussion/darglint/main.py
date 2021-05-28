def get_mean(collection):
    """
    Obtain the average of a collection of objects.

    Parameters
    ----------
    collection : list
        A list of numbers

    Returns
    -------
    float
        The mean of the numbers.
    """
    return sum(collection) / len(collection)
