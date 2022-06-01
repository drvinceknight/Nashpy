How to format markdown files
============================

The markdown files are all formatted according to a consistent style using
`mdformat <https://mdformat.readthedocs.io/en/stable/>`_.

How to install mdformat
-----------------------

To install :code:`mdformat` run::

    $ python -m pip install mdformat

How to format all markdown files
--------------------------------

To run :code:`mdformat` on a specific :code:`<file>`::

    $ python -m mdformat <file>

This will reformat :code:`<file>` in place.

To run :code:`mdformat` recursively from the current directory::

    $ python -m mdformat .

How to check markdown files
---------------------------

To check the format of :code:`<file>`::

    $ python -m mdformat --check <file>
