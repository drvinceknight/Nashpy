"""
Code to draw plot for the documentation.

This plots an example of stable steady state strategies in an asymmetric game.

The code should match the reference code in the documentation.
"""
import matplotlib.pyplot as plt
import numpy as np

import nashpy as nash


A = np.array([[2, 2], [3, 4]])
B = np.array([[4, 3], [3, 2]])
game = nash.Game(A, B)
x0 = np.array([0.9, 0.1])
y0 = np.array([0.3, 0.7])
xs, ys = game.asymmetric_replicator_dynamics(x0=x0, y0=y0)

plt.figure(figsize=(13, 5))
plt.subplot(1, 2, 1)
plt.plot(xs)
plt.title("Probability distribution of strategies over time for row player")
plt.xlabel("Timepoints")
plt.ylabel("Probability")
plt.legend([f"$s_{0}$", f"$s_{1}$"])
plt.subplot(1, 2, 2)
plt.plot(ys)
plt.title("Probability distribution of strategies over time for column player")
plt.xlabel("Timepoints")
plt.ylabel("Probability")
plt.legend([f"$s_{0}$", f"$s_{1}$"])

plt.savefig("main.svg", transparent=True)
