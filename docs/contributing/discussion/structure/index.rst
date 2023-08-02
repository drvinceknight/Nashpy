The code structure of Nashpy
============================

The directory structure
-----------------------

The directory structure for Nashpy is::

    ├── src/
    ├── tests/
    ├── docs/
    ├── CHANGES.md
    ├── CITATION.md
    ├── LICENSE
    ├── README.md
    ├── paper.bib
    ├── paper.md
    ├── pyproject.toml
    ├── .readthedocs.yml
    ├── setup.cfg
    └── tox.ini

Here is a brief description of each of these:

The :code:`src/` directory
**************************

The :code:`src/` directory contains the source code. It's structure is as
follows::

    src/
    └── nashpy
        ├── __init__.py
        ├── game.py
        ├── algorithms/
        ├── integer_pivoting/
        ├── learning/
        └── polytope/

- The :code:`__init__.py` file contains the various commands to import all the
  functionality of the library.
- The :code:`game.py` file contains the main :code:`nashpy.Game` class.
- The :code:`algorithms/` directory contains further modules with algorithms for
  computation of Nash equilibria.
- The :code:`integer_pivoting/` directory contains further modules with
  algorithms for integer pivoting.
- The :code:`learning/` directory contains further modules for various learning
  algorithms.
- The :code:`polytope` directory contains further modules with
  code for :ref:`best response polytopes <vertex-enumeration>`.

The :code:`tests/` directory
****************************

This contains all the test files.

The :code:`docs/` directory
****************************

The documentation is written using the Diataxis framework [Procida2021]_. As
well as various configuration files for :ref:`sphinx <sphinx-discussion>` there
are 5 main subdirectories::

    docs/
    ├── contributing
    │   ├── discussion/
    │   ├── how-to/
    │   ├── index.rst
    │   ├── reference/
    │   └── tutorial/
    ├── discussion/
    ├── how-to/
    ├── index.rst
    ├── reference/
    └── tutorial/

- The :code:`contributing/` directory contains the specific contributing
  documentation. Which itself is written using Diataxis [Procida2021]_.
- The :code:`discussion/` directory contains source files for the discussion
  described at [Procida2021]_ as: "explanation is discussion that clarifies and
  illuminates a particular topic."
- The :code:`reference/` directory contains source files for the reference
  described at [Procida2021]_ as: "reference guides are technical descriptions
  of the machinery and how to operate it."
- The :code:`how-to/` directory contains source files for the how to guides
  described at [Procida2021]_ as: "how-to guides are directions that take the
  reader through the steps required to solve a real-world problem"
- The :code:`tutorial/` directory contains source files for the tutorial
  described at [Procida2021]_ as: "tutorials are lessons that take the reader by
  the hand through a series of steps to complete a project of some kind."


The :code:`CHANGES.md` file
***************************

Makes a note of different changes in versions of Nashpy.


The :code:`CITATION.md` file
****************************

Contains information for citing Nashpy.

The :code:`LICENSE` file
************************

Contains the license.


The :code:`README.md` file
**************************

Contains the first entry point documentation to the Nashpy project.


The :code:`paper.bib` and :code:`paper.md` files
************************************************

These are the source files for the `Journal of Open Source Software
<https://joss.theoj.org>`_ paper written about Nashpy: [Knight2018b]_.

.. _pyproject.toml-file:

The :code:`pyproject.toml` file
*******************************

Contains all the build instructions for packaging Nashpy and is used by
:ref:`flit <flit-discussion>`.

The :code:`.readthedocs.yml` file
*********************************

.. <!--alex disable hostesses-hosts-->

This includes configuration settings  for the online service that hosts the
documentation :ref:`read the docs <readthedocs-discussion>`.

.. <!--alex enable hostesses-hosts-->

The :code:`setup.cfg` file
**************************

Contains some configuration instructions for testing.

The :code:`tox.ini` file
************************

Contains the instructions for the test runner :code:`tox`.

The Game class
--------------

The :code:`nashpy.Game` class is an umbrella class that creates an object
oriented interface to all functionality of Nashpy as methods on a game.
