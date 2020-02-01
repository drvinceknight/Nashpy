import numpy as np

prisoner_A = np.array([[3, 0], [5, 1]])
prisoner_B = np.array([[3, 5], [0, 1]])
prisoner_test_1 = (
    prisoner_A,
    prisoner_B,
    "prisoner_test_1",
    (np.array([0, 1]), np.array([0, 1])),
)


prisoner_degen_B = np.array([[3, 3], [1, 1]])
prisoner_degen_test_1 = (
    prisoner_A,
    prisoner_degen_B,
    "prisoner_degen_test_1",
    (np.array([0, 1]), np.array([1, 0])),
)


degen_A_3 = np.array([[1, 3, 3], [3, 1, 3], [1, 3, 3]])
degen_B_3 = np.array([[3, 3, 1], [1, 1, 3], [3, 1, 3]])
degen_test_3 = (
    degen_A_3,
    degen_B_3,
    "degen_test_3",
    (np.array([0.5, 0.5, 0]), np.array([0, 0, 1])),
)
