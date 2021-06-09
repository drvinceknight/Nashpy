Testing across environments with tox
====================================

The `tox <https://tox.readthedocs.io/en/latest/>`_ project allows for the
automation of many tasks related to Python packaging and testing.

For Nashpy it is used to:

1. Configure all tests.
2. Test across multiple python versions.

Configure all tests
-------------------

All test commands are written in :code:`tox.ini`. This
include things like checking style
with :ref:`black <black-discussion>` and presence of docstrings with
:ref:`interrogate <interrogate-discussion>`. Running all the checks is done
with a single standard command: :code:`python -m tox`.

Note that :ref:`checking for insensitive language in documentation
<how-to-check-for-insensitive-language>` is not configured or run by tox.

Test across multiple python versions
------------------------------------

This is done thanks to configurations written in :code:`tox.ini`::

    [tox]
    isolated_build = True
    envlist = py38, py39
