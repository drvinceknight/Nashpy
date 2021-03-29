"""
Code to draw plot for the documentation.

This plots an example of non-convergence.

The code should match the reference code in the documentation.
"""
import matplotlib.pyplot as plt
import numpy as np

import nashpy as nash

A = np.array([[0, -1, 1], [1, 0, -1], [-1, 1, 0]])
game = nash.Game(A)
y0 = np.array([0.3, 0.35, 0.35])

plt.plot(game.replicator_dynamics(y0=y0))
plt.xlabel("Timepoints")
plt.ylabel("Probability")
plt.title("Probability distribution of strategies over time")
plt.legend([f"$s_{0}$", f"$s_{1}$", f"$s_{2}$"], loc="upper left")

plt.savefig("main.svg", transparent=True)
