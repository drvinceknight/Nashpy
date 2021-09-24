How to write a type hint
========================

Type hints allow to annotate code in a machine and human readable way so as to
indicate the types of each variable. The general syntax of this is::

    def <function>(
        variable_1: type = default_value,
        variable_2: type,
        ) -> type

For example here is the annotated source code for some internal functionality::

    import numpy as np
    import numpy.typing as npt


    def make_tableau(M: npt.NDArray) -> npt.NDArray:
        """
        Make a tableau for the given matrix M.
        This tableau corresponds to the polytope of the form:
           Mx <= 1 and x >= 0
        Parameters
        ----------
        M : array
            A matrix with linear coefficients defining the polytope.
        Returns
        -------
        array
            The tableau that corresponds to the polytope.
        """
        return np.append(
            np.append(M, np.eye(M.shape[0]), axis=1),
            np.ones((M.shape[0], 1)),
            axis=1,
        )


How to check type annotations in a module
------------------------------------------

Running tests with :ref:`tox <how-to-run-tests>` will automatically check
type annotations.

If you want to check a specific file, use `Mypy
<https://mypy.readthedocs.io/en/stable/introduction.html>`_::

    $ python -m pip install mypy
    $ python -m mypy --ignore-missing-imports <path_to_file>
