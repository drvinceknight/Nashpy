.. _pip-compile-discussion:

Auto generating requirements.txt with pip-compile
=================================================

:ref:`Read the docs <readthedocs-discussion>` requires a :code:`requirements.txt`
file to build the documentation. Nashpy uses :ref:`flit <flit-discussion>` for
packaging which in turns uses the :code:`pyproject.toml` configuration setup.

The :code:`requirements.txt` file required by Read the docs can be automatically
generated using `pip-compile
<https://github.com/jazzband/pip-tools/#example-usage-for-pip-compile>`_ which
is part of `pip-tools <https://github.com/jazzband/pip-tools>`_.

To do this, first :ref:`activate the environment <how-to-env>`::

    $ source env/bin/activate

Then install :code:`pip-tools`::

    $ python -m pip install pip-tools

Then use :code:`pip-compile` to generate :code:`requirements.txt`::

    $ pip-compile pyproject.toml

Note that in practice this only needs to be done when the requirements in
:code:`pyproject.toml` are modified.
