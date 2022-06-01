.. _mdformat-discussion:

Ensuring consistent markdown format with mdformat
=================================================

From the :code:`mdformat`'s `documentation page
<https://mdformat.readthedocs.io/en/stable/>`_:

.. pull-quote::

   "Mdformat is an opinionated Markdown formatter that can be used to enforce a
   consistent style in Markdown files. Mdformat is a Unix-style command-line
   tool as well as a Python library."

The rationale for using :code:`mdformat` is the same as the one for using
:ref:`black <black-discussion>` which is to avoid spending any time thinking
about the formatting of source files.

Examples of choices that :code:`mdformat` will make:

.. code-block:: md

   # Hello world

   Here is how to write some python code:

      print("Hello Nashpy!)


become:

.. code-block:: md

   # Hello world

   Here is how to write some python code:

   ```
   print("Hello Nashpy!)
   ```
