.. _pytest-discussion:

Writing clean tests with pytest
===============================

The `pytest <https://github.com/pytest-dev/pytest>`_ framework allows for cleaner
tests to be written but also for efficient running of tests with multiple
plugins.

Plugins
-------

Coverage: :code:`pytest-cov`
****************************

The `pytest-cov <https://github.com/pytest-dev/pytest-cov>`_ plugin allows you
to run coverage checks with pytest.

Flake8: :code:`pytest-flake8`
*****************************

The `pytest-flake8 <https://github.com/tholo/pytest-flake8>`_ plugin allows you
to run flake8 checks with pytest.

Stochastic effects: :code:`pytest-randomly`
*******************************************

The `pytest-randomly <https://github.com/pytest-dev/pytest-randomly>`_ plugin
does two things (for Nashpy):

1. It randomly shuffles the order of tests: this ensures that tests passing is
   not dependent on the order in which they run.
2. It seeds stochastic tests to ensure that any exceptions are reproducible. In
   practice this has little effect here as ideally stochastic tests are seeded
   or written with :ref:`hypothesis <hypothesis-discussion>`.

Nicer look: :code:`pytest-sugar`
********************************

The `pytest-sugar <https://github.com/Teemu/pytest-sugar>`_ plugin changes the
look of pytest.

Further plugins
---------------

The *Talk Python to Me* podcast episode 267 featured a discussion of a number of
pytest plugins: https://talkpython.fm/episodes/show/267/15-amazing-pytest-plugins
