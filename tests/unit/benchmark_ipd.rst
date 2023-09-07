#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Aug 26 13:46:06 2023

@author: jasrajan
"""
'''
Support Enumeration
'''

import pytest
import nashpy as nash
import numpy as np

def compute_equilibria():
    a = np.array([[3,0],[5,1]])
    b = np.array([[3,5],[0,1]])
    game = nash.Game(a,b)

    equilibria = game.support_enumeration()
    for eq in equilibria:
        print(eq)

def test_compute_equilibria(benchmark):
    # benchmark the 'compute_equilibria' function
    benchmark(compute_equilibria)

#print(game.replicator_dynamics())

'''
Vertex Enumeration
'''

import pytest
import nashpy as nash
import numpy as np

def compute_equilibria():
    a = np.array([[3,0],[5,1]])
    b = np.array([[3,5],[0,1]])
    game = nash.Game(a,b)

    equilibria = game.vertex_enumeration()
    for eq in equilibria:
        print(eq)

def test_compute_equilibria(benchmark):
    # benchmark the 'compute_equilibria' function
    benchmark(compute_equilibria)

#print(game.replicator_dynamics())

'''
Lemke-Howson
'''

import pytest
import nashpy as nash
import numpy as np

def compute_equilibria():
    a = np.array([[6,4],[8,4]])
    b = np.array([[6,8],[4,4]])
    game = nash.Game(a,b)

    equilibria = game.lemke_howson(initial_dropped_label=0)
    for eq in equilibria:
        print(eq)

def test_compute_equilibria(benchmark):
    # benchmark the 'compute_equilibria' function
    benchmark(compute_equilibria)

#print(game.replicator_dynamics())


'''
Support Enumeration - 2 iterations
'''

import pytest
import nashpy as nash
import numpy as np
import nashpy.repeated_games

def compute_equilibria():
    A = np.array([[3,0],[5,1]])
    B = np.array([[3,5],[0,1]])
    ipd = nash.Game(A, B)

    rep_ipd = nash.repeated_games.obtain_repeated_game(game=ipd, repetitions=2)

    equilibria = rep_ipd.vertex_enumeration()
    for eq in equilibria:
        print(eq)

def test_compute_equilibria(benchmark):
    result = benchmark(compute_equilibria)


'''
Vertex Enumeration - 2 iterations
'''

import pytest
import nashpy as nash
import numpy as np
import nashpy.repeated_games

def compute_equilibria():
    A = np.array([[3,0],[5,1]])
    B = np.array([[3,5],[0,1]])
    ipd = nash.Game(A, B)

    rep_ipd = nash.repeated_games.obtain_repeated_game(game=ipd, repetitions=2)

    equilibria = rep_ipd.vertex_enumeration()
    for eq in equilibria:
        print(eq)

def test_compute_equilibria(benchmark):
    result = benchmark(compute_equilibria)
    

'''
Lemke-Howson - 2 iterations
'''

import pytest
import nashpy as nash
import numpy as np
import nashpy.repeated_games

def compute_equilibria():
    A = np.array([[3,0],[5,1]])
    B = np.array([[3,5],[0,1]])
    ipd = nash.Game(A, B)

    rep_ipd = nash.repeated_games.obtain_repeated_game(game=ipd, repetitions=2)

    equilibria = rep_ipd.lemke_howson(initial_dropped_label=0)
    for eq in equilibria:
        print(eq)

def test_compute_equilibria(benchmark):
    result = benchmark(compute_equilibria)

'''
Fictitious Play
'''
import numpy as np
import nashpy as nash
import pytest

def compute_equilibria():
    a = np.array([[3,0],[5,1]])
    b = np.array([[3,5],[0,1]])
    game = nash.Game(a,b)
    etha = 50
    epsilon_bar =0
    iterations = 10000
    np.random.seed(0)

    play_counts_and_distributions = tuple(game.stochastic_fictitious_play(iterations=iterations, etha=etha, epsilon_bar=epsilon_bar))

    # Extract only the row player's play_counts from the output
    play_counts_and_distributions = [play_counts[0] for play_counts, distributions in play_counts_and_distributions]

    probabilities = [
        counts / np.sum(counts)
        if np.sum(counts) != 0
        else np.ones_like(counts) / len(counts)
        for counts in play_counts_and_distributions
    ]

def test_compute_equilibria(benchmark):
    # benchmark the function
    benchmark(compute_equilibria)
    
    


'''
Moran Process
'''
import numpy as np
import nashpy as nash
import matplotlib.pyplot as plt

def compute_equilibria():
    a = np.array([[3,7],[5,1]])
    b = np.array([[3,5],[7,1]])
    game = nash.Game(a,b)
    
    etha=50
    epsilon_bar=0

    iterations = 10000
    np.random.seed(0)

    play_counts_and_distributions = list(game.stochastic_fictitious_play(iterations=iterations,etha=etha,epsilon_bar=epsilon_bar))

    plt.figure()
    # Extract only the row player's play_counts from the output
    play_counts = [play_counts[0] for play_counts, distributions in play_counts_and_distributions]

    probabilities = [
        counts / np.sum(counts)
        if np.sum(counts) != 0
        else np.ones_like(counts) / len(counts)
        for counts in play_counts
    ]

    for number, strategy in enumerate(zip(*probabilities)):
        plt.plot(strategy, label=f"$s_{number}$")

    plt.xlabel("Iteration")
    plt.ylabel("Probability")
    plt.title("Actions taken by row player")
    plt.xlim
    plt.legend()

    plt.show()

compute_equilibria()



