import numpy as np


from nashpy.learning.discete_replicator_dynamics import type_2_discrete_step


def test_type_2_discrete_step():
    """
    Write out hand calculation of this step
    """
    x = np.array((0.2, 0.5, 0.3))
    A = np.array(
        (
            (4, 3),
            (2, 1),
        )
    )
    expected_next_x = np.array((0.25, 0.51, 0.24))
    next_x = type_2_discrete_step(
        A=A,
        x=x,
    )
    assert np.allclose(expected_next_x, next_x)
