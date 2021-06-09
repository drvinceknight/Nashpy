.. _readthedocs-discussion:

Hosting documentation on Read The Docs
======================================

.. <!--alex disable hostesses-hosts-->

Read the docs is a web service that builds and hosts documentation. You can read
more about the service here: https://readthedocs.org

.. <!--alex enable hostesses-hosts-->

The documentation contained in :code:`docs/` is automatically built and can be
viewed at https://nashpy.readthedocs.io/en/stable/.

Settings
--------

Read the docs allows you to configure your build using a :code:`readthedocs.yml`
file. This is not currently used by Nashpy.

The default version (ie when going to https://nashpy.readthedocs.io/) is the
:code:`stable` version which means the last release.

You can view the version of the documentation currently on the :code:`main`
branch by going to: https://nashpy.readthedocs.io/latest.

Configuration file
------------------

Read the docs can have specific settings set in a :code:`.readthedocs.yml` file.
Details on this can be found here:
https://docs.readthedocs.io/en/stable/config-file/v2.html#packages

One specific setting used by Nashpy is::

    python:
       version: 3.8
       install:
         - method: pip
           path: .

This ensures Read the docs does not look for a :code:`requirements.txt` file to
install the library. Instead it runs :code:`pip install .` which uses
:ref:`pyproject.toml-file`.

A powerful feature offered by Read the docs is that it can build documentation
in pull requests.

Building documentation in pull requests
---------------------------------------

To set this up you need to ensure the following things are done:

.. <!--alex disable hook-->

1. The repository settings on Read the docs instruct pull requests to be built.
2. The correct web hook is in place on Github.
3. The correct settings of the web hook are done on the Github repository.

.. <!--alex enable hook-->

To instruct pull requests to be built ensure the following box is ticked in the
Advanced settings for your project on Read the docs:

.. image:: /_static/contributing/discussion/readthedocs/instruction/main.png

.. <!--alex disable hooks-->

Setting up the web hooks correctly is described here:
https://docs.readthedocs.io/en/latest/pull-requests.html

.. <!--alex enable hooks-->

When done correctly this is what `Applications settings
<https://github.com/settings/applications?o=used-desc>`_ should look like:

.. image:: /_static/contributing/discussion/readthedocs/web_hook/main.png

The final thing to check is the setting on the specific Github repository (under
:code:`Settings/Webhooks`) which
should have the following 4 boxes ticked:

- Branch or tag creation
- Branch or tag deletion
- Pull requests
- Pushes

When done correctly this should look like:

.. image:: /_static/contributing/discussion/readthedocs/github_settings_branches/main.png
.. image:: /_static/contributing/discussion/readthedocs/github_settings_PRs_and_pushes/main.png

This is described here:
https://docs.readthedocs.io/en/latest/webhooks.html#github (although note that
ticking the Pull Requests box is not indicated there).

Reviewing documentation on Pull Requests
----------------------------------------

If this is all done correctly you will be able to view your documentation during
pull requests:

.. image:: /_static/contributing/tutorial/ci/main.png

For example here is how the documentation looked for pull request that
added this specific page of the documentation:

.. image:: /_static/contributing/discussion/readthedocs/preview/main.png
