.. _darglint_discussion:

Checking the format of docstrings with darglint
===============================================

Documentation strings, more commonly referred to as `docstrings
<https://www.python.org/dev/peps/pep-0257/>`_ in python are strings that
directly document a function. Their presence is checked using
:ref:`interrogate-discussion` but the particular format they are written in is
checked using `darglint
<https://github.com/terrencepreilly/darglint>`_.

Once installed darglint can be used to check one of three docstring styles:

1. `Google style guide <https://google.github.io/styleguide/pyguide.html>`_
2. `Sphinx style guide <https://pythonhosted.org/an_example_pypi_project/sphinx.html#function-definitions>`_
3. `Numpy style guide <https://numpydoc.readthedocs.io/en/latest/format.html>`_

For example, consider the file :code:`main.py`:

.. literalinclude:: /_static/contributing/discussion/darglint/main.py

After installing darglint::

    $ python -m pip install darglint

If we check the format of this file against the Google style guide::

    $ darglint -s google main.py
    main.py:get_mean:1: DAR101: - collection
    main.py:get_mean:1: DAR201: - return

we get two errors, we can cross reference the error codes :code:`DAR101` and
:code:`DAR201` at
`<https://github.com/terrencepreilly/darglint#error-codes>`_.

- :code:`DAR101`: "The docstring is missing a parameter in the definition."
- :code:`DAR201`: "The docstring is missing a return from definition."

Note that our file does have both those things but here darglint is telling us
that they do not match with the google style guide.

If we check the format of this file against the Sphinx style guide::

    $ darglint -s sphinx main.py
    main.py:get_mean:1: DAR101: - collection
    main.py:get_mean:1: DAR201: - return

we get the same two errors.

Running, the file against the Numpy style guide gives::

    $ darglint -s numpy main.py
    $

No errors are raised as this is indeed written using the Numpy style guide which
is also the convention chosen for the entire Nashpy source code.

Running darglint as part of the test suite
------------------------------------------

If darglint is installed it will automatically run as part of the flake8 check.
For Nashpy this is done as part of the pytest run which is all configured using
tox.
