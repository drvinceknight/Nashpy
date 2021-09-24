How to write a docstring
========================

All functionality needs to have a documentation string (`docstrings
<https://www.python.org/dev/peps/pep-0257/>`_). The convention used in Nashpy is
to follow `Numpy's docstring convention
<https://numpydoc.readthedocs.io/en/latest/format.html#docstring-standard>`_::

    def <function>(<signature>):
        """
        <short summary>

        Parameters
        ----------
        <paramter> : <type>
            <description>
        <paramter> : <type>
            <description>
        ...
        <paramter> : <type>
            <description>

        Returns
        -------
        <type>
            <description>
        """

If the function/method does not return anything but is instead a **generator**
then :code:`Returns` should be replaced with :code:`Yields`.


How to check dosctrings in a module
-----------------------------------

Running tests with :ref:`tox <how-to-run-tests>` will automatically check
formatting of docstrings.

If you want to check a specific file, use `darglint
<https://github.com/terrencepreilly/darglint>`_::

    $ python -m pip install darglint
    $ darglint -s numpy <path_to_file>
