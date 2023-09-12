Writing benchmarks with pytest benchmark and memray
===================================================

`pytest-benchmark <https://github.com/ionelmc/pytest-benchmark>`_ is a tool that allows you to write benchmarks to be run with pytest.

The `pytest-benchmark` creates a :code:`benchmark` fixture that can be passed to
a test. For example consider this test:

.. literalinclude:: /../benchmarks/test_support_enumeration.py
   :pyobject: test_support_enumeration_on_two_by_two_game

The `benchmark` fixture is a function with signature::

    benchmark(<function>, *args, **kwargs)

Running benchmarks
------------------

To run the benchmarks no extra commands are necessary. For example if the
benchmarks are located in :code:`benchmarks/` then the following command will
run them::

    python -m pytest benchmarks

Comparing benchmarks
--------------------

To save the results of a benchmark run you can run::

    python -m pytest benchmarks --benchmark-autosave

To compare the results with a saved set of benchmarks::

    python -m pytest benchmarks --benchmark-compare

Profiling memory with memray
----------------------------

`pytest-memray <https://pytest-memray.readthedocs.io/en/latest/>`_ is a plugin
that profiles the memory use when running a specific set of tests.
