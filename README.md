# Nash: a python library for the computation of equilibria of normal form games.

**This is a library with standard dependencies so that it is pip installable: if
you want to do sophisticated equilibria computation you should use
[gambit](https://github.com/gambitproject/gambit).**

This code is based on code that was implemented in
[Sagemath](http://www.sagemath.org/).

# Tests

To run the full test suite:

- Install the library (preferably in a virtual environment)

    python setup.py develop

- Run the tests:

    python -m unittest discover tests
