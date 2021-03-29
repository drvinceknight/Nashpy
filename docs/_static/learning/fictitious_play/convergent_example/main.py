"""
Code to draw plot for the documentation.

This plots a divergent fictitious play example.

The code should match the reference code in the documentation.
"""
import matplotlib.pyplot as plt
import numpy as np

import nashpy as nash

A = np.array([[1 / 2, 1, 0], [0, 1 / 2, 1], [1, 0, 1 / 2]])
B = np.array([[1 / 2, 0, 1], [1, 1 / 2, 0], [0, 1, 1 / 2]])
game = nash.Game(A, B)
iterations = 10000
np.random.seed(0)
play_counts = tuple(game.fictitious_play(iterations=iterations))


plt.figure()
probabilities = [
    row_play_counts / np.sum(row_play_counts)
    for row_play_counts, col_play_counts in play_counts
]
for number, strategy in enumerate(zip(*probabilities)):
    plt.plot(strategy, label=f"$s_{number}$")

plt.xlabel("Iteration")
plt.ylabel("Probability")
plt.legend()
plt.title("Actions taken by row player")
plt.savefig("main.svg", transparent=True)
