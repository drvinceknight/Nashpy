"""
Code to draw plot for the documentation.

This plots an example of non-convergence in asymmetric replicator dynamics.

The code should match the reference code in the documentation.
"""
import matplotlib.pyplot as plt
import numpy as np

import nashpy as nash

A = np.array([[0, -1, 1], [1, 0, -1], [-1, 1, 0]])
B = A.transpose()
game = nash.Game(A, B)
x0 = np.array([0.3, 0.35, 0.35])
y0 = np.array([0.3, 0.35, 0.35])
xs, ys = game.asymmetric_replicator_dynamics(x0=x0, y0=y0)

plt.figure(figsize=(13, 5))
plt.subplot(1, 2, 1)
plt.plot(xs)
plt.title("Probability distribution of strategies over time for row player")
plt.xlabel("Timepoints")
plt.ylabel("Probability")
plt.legend([f"$s_{0}$", f"$s_{1}$", f"$s_{2}$"])
plt.subplot(1, 2, 2)
plt.plot(ys)
plt.title("Probability distribution of strategies over time for column player")
plt.xlabel("Timepoints")
plt.ylabel("Probability")
plt.legend([f"$s_{0}$", f"$s_{1}$", f"$s_{2}$"])

plt.savefig("main.svg", transparent=True)
