"""
Code to draw plot for the documentation.

This plots a non-convergent stochastic fictitious play example.

The code should match the reference code in the documentation.
"""

import matplotlib.pyplot as plt
import nashpy as nash
import numpy as np

A = np.array([[0, 1, 0], [0, 0, 1], [1, 0, 0]])
B = np.array([[0, 0, 1], [1, 0, 0], [0, 1, 0]])
game = nash.Game(A, B)
iterations = 10000
np.random.seed(0)
play_counts_and_distribuions = tuple(
    game.stochastic_fictitious_play(iterations=iterations)
)

plt.figure()
probabilities = [
    row_play_counts / np.sum(row_play_counts)
    if np.sum(row_play_counts) != 0
    else row_play_counts + 1 / len(row_play_counts)
    for (row_play_counts, col_play_counts), _ in play_counts_and_distribuions
]
for number, strategy in enumerate(zip(*probabilities)):
    plt.plot(strategy, label=f"$s_{number}$")
plt.xlabel("Iteration")
plt.ylabel("Probability")
plt.title("Actions taken by row player")
plt.legend()
plt.savefig("divergent_example/main.svg", transparent=True)
