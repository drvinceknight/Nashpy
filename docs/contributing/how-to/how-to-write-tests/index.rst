How to write tests
==================

The :ref:`pytest <pytest-discussion>` framework is used for writing and running
tests for Nashpy.

Tests should be written in one of the following locations:

- In a preexisting file in the :code:`test/` directory.
- In a new file in the :code:`test/` directory.

Thanks to :code:`pytest` the format for a test is::

    def test_<functionality>():
        """
        <short summary if necessary>
        """
        <code logic>
        assert <boolean>

For guidance on how to run tests see: :ref:`how-to-run-tests`.

When writing a new test it is good practice to ensure the test fails (either by
modifying the test or by modifying the source code): this ensures that
:ref:`pytest <pytest-discussion>` is running the test in question.

Note that when adding new functionality the coverage of the test suite will be
checked using :ref:`coverage <coverage-discussion>`. Thus, in practice multiple
tests will need to be written to test new functionality completely.

Hypothesis
----------

Property based tests are tests that use random sampling in an efficient manner
to test given properties as opposed to specific values. Nashpy uses
:ref:`hypothesis <hypothesis-discussion>` for this.

For example the following tests that for any given :code:`M`, which is a 3 by 3
numpy integer array, the length of the output of
:code:`get_derivative_of_fitness` is as expected::

    from hypothesis import given, settings
    from hypothesis.strategies import integers
    from hypothesis.extra.numpy import arrays

    @given(M=arrays(np.int8, (3, 3)))
    def test_property_get_derivative_of_fitness(M):
        t = 0
        x = np.zeros(M.shape[1])
        derivative_of_fitness = get_derivative_of_fitness(x, t, M)

        assert len(derivative_of_fitness) == len(x)


