Tutorial: make a contribution to the documentation
==================================================

In this tutorial we will make a contribution to the documentation of Nashpy.

Forking the repository
----------------------

Navigate to http://github.com and create an account. If you are in education you
can apply for a specific education account here: https://education.github.com.

Navigate to the Github repository for Nashpy:
https://github.com/drvinceknight/Nashpy. This is the hub for development of the
source code. You cannot make modification to this copy of the source code so you
need to create your own copy under your Github account. You do this by creating
a **fork**. Do this by clicking the :code:`Fork` button and following the
instructions:

.. image:: /_static/contributing/tutorial/forking/main.png

Cloning the repository
----------------------

Once we have a fork of the repository on **your** Github account, create a copy
of it to your computer. This is called cloning. Do this by clicking the `Code`
button and copying the address of the repository to your clipboard:

.. image:: /_static/contributing/tutorial/cloning/main.png

If you have not installed :code:`git` go to https://git-scm.com and install.

Now to create a clone of the source code open your command line tool and type
the following (**replace** :code:`<your username>` with your Github username):

    $ git clone https://github.com/<your username>/Nashpy.git

This will download the source code to your computer::

    $ git clone https://github.com/<your username>/Nashpy.git
    Cloning into 'Nashpy'...
    remote: Enumerating objects: 1813, done.
    remote: Counting objects: 100% (362/362), done.
    remote: Compressing objects: 100% (225/225), done.
    remote: Total 1813 (delta 160), reused 233 (delta 79), pack-reused 1451
    Receiving objects: 100% (1813/1813), 439.94 KiB | 2.67 MiB/s, done.
    Resolving deltas: 100% (905/905), done.

Creating a branch
-----------------

In order to modify the source code you must create a new branch. After cloning,
first change directory in to the Nashpy source code::

    $ cd Nashpy

Now, to keep the changes you are about to make separate from the :code:`main`
source code, create a **branch**::

    $ git branch add-name-to-contributors-list

Now checkout to that branch::

    $ git checkout add-name-to-contributors-list

Modifying the documentation
---------------------------

Using your preferred editor, open the file
:code:`Nashpy/docs/contributing/reference/contributors/index.rst`. If you do not
have a preferred editor `Visual Studio Code <https://code.visualstudio.com>`_ is
recommended.

Now add you name to the file (**replace** :code:`<your username>`
with your Github username)::

    List of contributors
    --------------------

    - `@drvinceknight <https://github.com/drvinceknight>`_
    - `@<your username> <https://github.com/<your username>`_

Checking the modification
-------------------------

To build the documentation, first create a virtual environment specifically for
purposes to work on Nashpy::

    $ python -m venv env

This creates a directory :code:`env` which holds a separate version of python.
To tell your command line tool to now use this version:

On Linux or macOS type::

    $ source env/bin/activate

On Windows type::

    $ env\Scripts\activate

Now install the Nashpy software in to this environment::

    $ python -m pip install flit
    $ python -m flit install --symlink

To build the documentation::

    $ cd docs
    $ sphinx-build -b html . _build/html
    Running Sphinx v3.1.2
    loading pickled environment... done
    building [mo]: targets for 0 po files that are out of date
    building [html]: targets for 2 source files that are out of date
    updating environment: 1 added, 2 changed, 1 removed
    reading sources... [100%] contributing/tutorial/index
    looking for now-outdated files... none found
    pickling environment... done
    checking consistency... done
    preparing documents... done
    writing output... [100%] index
    generating indices...  genindex py-modindexdone
    highlighting module code... [100%] nashpy.learning.fictitious_play
    writing additional pages...  searchdone
    copying images... [100%] _static/contributing/tutorial/cloning/main.png
    copying static files... ... done
    copying extra files... done
    dumping search index in English (code: en)... done
    dumping object inventory... done
    build succeeded.

    The HTML pages are in _build/html.

You can open :code:`_build/html/index.html` in a browser to see the
documentation locally which should include the changes you made.

Running the test suite
----------------------

You can run the entire test suite which will check that this modification has
not caused any problems::

    $ python -m pip install tox
    $ python -m tox

Committing the change
---------------------

Now you need to **stage** this file::

    $ git add docs/contributing/reference/contributors/index.rst

Now commit this file::

    $ git commit

This will open a text editor where you can write your commit title and message::

    Add <your username> to list of contributors

    I am doing the contribution tutorial.

Closing the editor will commit the changes you made.

Pushing the change to Github
----------------------------

Now that all that is done, you are going to send the changes back to your copy
of the source code on Github::

    $ git push origin add-name-to-contributors-list

Opening a Pull Request
----------------------

You now have 2 copies of the modified source code of Nashpy. One locally on your
computer, the other under your Github account. In order to include those changes
in to the main source code of Nashpy you will open a Pull request.

To do this, go to your fork of the Nashpy repository:
:code:`https://github.com/<your username>/Nashpy`. You should see a
:code:`Compare and Pull Request` button:

.. image:: /_static/contributing/tutorial/before_pr/main.png

Once you have clicked on that, you can review your changes and then eventually
click on :code:`Create pull request` to create the Pull Request.

Making further modifications
----------------------------

Once a Pull Request is opened, a number of automated checks will start. This
will check the various software tests but also build a viewable version of the
documentation.

You can click on the corresponding :code:`details` button to see any of these:

.. image:: /_static/contributing/tutorial/ci/main.png

Your modification will also be reviewed:

.. image:: /_static/contributing/tutorial/review/main.png

To make any required changes, **modify the files**.

Then stage and commit the files::

    $ git add docs/contributing/reference/contributors/index.rst
    $ git commit

This will open a text editor where you can write your commit title and message
(similarly to before).

Once this is done, push the code to Github which will automatically update the
pull request::

    $ git push origin add-name-to-contributors-list

This final process of making further modifications might repeat itself and
eventually the Pull Request will be **merged** and your changes included in the
main version of the Nashpy source code.
