.. _how-to-run-tests:

How to run tests
================

To install :code:`tox`::

    $ python -m pip install tox

To run all tests::

    $ python -m tox

If you want to run the tests across a single version of Python::

    $ python -m tox -e <version>

where :code:`version` is either :code:`py38` or :code:`py39`.
