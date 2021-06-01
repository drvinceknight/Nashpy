How to make a commit
====================

To commit changes to a given code :code:`<file.py>`.

First, stage it::

    $ git add <file.py>

Now that the file is staged, create a commit::

    $ git commit

This will open a text editor (a default text editor of your choice can be set).
In there write a commit message in the following format::

    <commit title>

    <commit message>

Save and exit from the text editor and your commit should be applied.

Commit message style
--------------------

The :code:`<commit title>` should be short and follow the style: "If
this commit is applied it will :code:`<commit title>` will happen."

The :code:`<commit message>` should include further details and can go over many
lines.

Here is some good guidance on writing commit messages:
https://chris.beams.io/posts/git-commit/

Do not use :code:`git commit -m "<commit message>"`
---------------------------------------------------

It is possible to write a commit message directly as you make the commit by
typing::

    $ git commit -m <commit title>

This is not recommended as it encourages unclear commit messages.
