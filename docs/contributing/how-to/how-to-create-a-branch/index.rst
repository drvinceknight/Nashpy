How to create a branch
======================

To create a branch with name :code:`<name-of-branch>` run::

    $ git branch <name-of-branch>

To go to that branch::

    $ git checkout <name-of-branch>

How to branch from a specific branch, tag or commit
---------------------------------------------------

To create a branch with name :code:`<name-of-branch>` from a specific branch,
tag or commit with name :code:`<location>` run::

    $ git branch <name-of-branch> <location> 

How to create a branch and checkout to it at the same time
----------------------------------------------------------

You can create a branch with name :code:`<name-of-branch>` and checkout in a
single command::

    $ git checkout -b <name-of-branch>
