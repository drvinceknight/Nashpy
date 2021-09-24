Checking of type hints using mypy
=================================

Optional type hints can be added to python code which allows specification
of the type of a variable. Type hints were specified in
`PEP484 <https://www.python.org/dev/peps/pep-0484/>`_.

Type hints are ignored when running the code but can be statically analysed
using a various tools:

- `Mypy <https://mypy.readthedocs.io/en/stable/introduction.html>`_.
- `Pyright <https://github.com/Microsoft/pyright>`_

`Mypy <https://mypy.readthedocs.io/en/stable/introduction.html>`_ is used for
Nashpy.

For example, consider the file :code:`main.py`:

.. literalinclude:: /_static/contributing/discussion/mypy/main.py

After installing mypy::

    $ python -m pip install mypy

If we check the annotations present in the file::

    $ python -m mypy main.py
    Success: no issues found in 1 source file

There are no issues because there are no annotations. If the following
annotations are added:

.. literalinclude:: /_static/contributing/discussion/mypy/main_with_wrong_types.py

We get::

    $ python -m mypy main.py
    main_with_wrong_types.py:17: error: Argument 1 to "len" has incompatible type "Iterable[Any]"; expected "Sized"
    Found 1 error in 1 file (checked 1 source file)

Mypy has found an error here: the :code:`Iterable` type does not necessarily
have a length. The following modifies this:

.. literalinclude:: /_static/contributing/discussion/mypy/main_with_correct_types.py

We get::

    $ python -m mypy main.py
    Success: no issues found in 1 source file

--ignore-missing-import
-----------------------

In some cases some imported modules cannot be used checked with Mypy, these can
be ignored by running the following::

    $ python -m mypy --ignore-missing-import main.py

Overlap of functionality with darglint
--------------------------------------

The python library `darglint <darglint_discussion>`_ checks the format of the
docstrings. This will also use any type annotations and so the type annotations
and the types specified in the docstrings must correspond.
