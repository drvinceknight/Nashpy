How to update from upstream
===========================

In order to bring your local repository up to date with any upstream changes::

    $ git remote add upstream https://github.com/drvinceknight/Nashpy.git
    $ git pull upstream main

The above:

1. Creates a new remote with alias :code:`upstream` that points at the main
   source repository for Nashpy. You can list all your
   remote repositories by running::

       $ git remote -v

2. Pulls the latest changes from the :code:`main` branch of the upstream
   repository.
