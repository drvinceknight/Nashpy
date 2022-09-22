import sys
import os
sys.path.append(os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'src')))
import nashpy as nash
import numpy as np
import timeit
import csv
from statistics import mean, stdev, variance, quantiles
from scipy.stats import trim_mean

def benchmark_random_symmetric(minsize: int = 2,
                               maxsize: int = 10,
                               lowerbound: int = -10,
                               upperbound: int = 10,
                               repeat: int = 10,
                               number: int = 1,
                               algorithm: str ="support_enumeration()"):
    """
    Creates a list of results of time taken when benchmarking algorithms to find
    the equilibria of purely randomly generated nashpy symmetric Game objects
    Parameters
    ----------
    minsize : int
        The minimum size, n, for the nxn payoff matrices. Must be at least 2.
    maxsize : int
        The maximum size, n, for the nxn payoff matrices.
    lowerbound : int
        The lower bound of values taken for each player's payoff matrix
    upperbound : int
        The upper bound of values taken for each player's payoff matrix
    repeat : int
        The amount of times to benchmark the algorithm.
    number : int
        The amount of times the algorithm is run per round of benchmarking.
    algorithm : string
        The algorithm to be benchmarked. Only tested with "support_enumeration()"
        and "vertex_enumeration()"

    Returns
    -------
    array
        A list of lists containing the times taken for the rounds of benchmarking
        for each size of the game, n.
    """
    results = []

    for n in range(minsize, maxsize+1):
        print("benchmarking " + algorithm + " on game of size " + str(n))
        RANDOM_NXNA = np.random.randint(lowerbound, upperbound, (n, n))
        RANDOM_NXNB = np.random.randint(lowerbound, upperbound, (n, n))

        game = nash.Game(RANDOM_NXNA)

        result = timeit.repeat("tuple(game."+algorithm+")", repeat=repeat, number=number, globals=locals())

        results.append(result)

    return results

def benchmark_random_asymmetric(minsize: int = 2,
                                maxsize: int = 10,
                                lowerbound: int = -10,
                                upperbound: int = 10,
                                repeat: int = 10,
                                number: int = 1,
                                algorithm: str ="support_enumeration()"):
    """
    Creates a list of results of time taken when benchmarking algorithms to find
    the equilibria of purely randomly generated nashpy asymmetric Game objects
    Parameters
    ----------
    minsize : int
        The minimum size, n, for the nxn payoff matrices. Must be at least 2.
    maxsize : int
        The maximum size, n, for the nxn payoff matrices.
    lowerbound : int
        The lower bound of values taken for each player's payoff matrix
    upperbound : int
        The upper bound of values taken for each player's payoff matrix
    repeat : int
        The amount of times to benchmark the algorithm.
    number : int
        The amount of times the algorithm is run per round of benchmarking.
    algorithm : string
        The algorithm to be benchmarked. Only tested with "support_enumeration()"
        and "vertex_enumeration()"

    Returns
    -------
    array
        A list of lists containing the times taken for the rounds of benchmarking
        for each size of the game, n.
    """
    results = []

    for n in range(minsize, maxsize+1):
        print("benchmarking " + algorithm + " on game of size " + str(n))
        RANDOM_NXNA = np.random.randint(lowerbound, upperbound, (n, n))
        RANDOM_NXNB = np.random.randint(lowerbound, upperbound, (n, n))

        game = nash.Game(RANDOM_NXNA, RANDOM_NXNB)

        result = timeit.repeat("tuple(game."+algorithm+")", repeat=repeat, number=number, globals=locals())

        results.append(result)

    return results

if __name__ == "__main__":
    minsize = 12
    maxsize = 12
    for algorithm in ["support_enumeration()", "vertex_enumeration()"]:
        n = minsize
        np.random.seed(0)
        results = benchmark_random_symmetric(minsize=minsize, maxsize=maxsize, repeat=1, number=1, algorithm=algorithm)
        data = []
        for result in results:
            if len(result) >= 2:
                data.append([n, min(result), trim_mean(result, 0.1), mean(result), max(result), stdev(result), variance(result)] + quantiles(result))
                n+=1
            else:
                data.append([n] + result)
                n+=1
        header = ["n", "min", "trimmed mean", "mean", "max", "standard deviation", "variance", "25th quartile", "median", "75th quartile"]
        with open("random_symmetric_"+algorithm+".csv", "a", newline="") as f:
            writer = csv.writer(f)

            #writer.writerow(header)

            writer.writerows(data)

    minsize = 12
    maxsize = 12
    for algorithm in ["support_enumeration()", "vertex_enumeration()"]:
        n = minsize
        np.random.seed(0)
        results = benchmark_random_asymmetric(minsize=minsize, maxsize=maxsize, repeat=1, number=1, algorithm=algorithm)
        data = []
        for result in results:
            if len(result) >= 2:
                data.append([n, min(result), trim_mean(result, 0.1), mean(result), max(result), stdev(result), variance(result)] + quantiles(result))
                n+=1
            else:
                data.append([n] + result)
                n+=1
        header = ["n", "min", "trimmed mean", "mean", "max", "standard deviation", "variance", "25th quartile", "median", "75th quartile"]
        with open("random_asymmetric_"+algorithm+".csv", "a", newline="") as f:
            writer = csv.writer(f)

            #writer.writerow(header)

            writer.writerows(data)
