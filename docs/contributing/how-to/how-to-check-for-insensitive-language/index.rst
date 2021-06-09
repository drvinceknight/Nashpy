.. _how-to-check-for-insensitive-language:

How to check for insensitive language
=====================================

The documentation is checked for insensitive or inconsiderate language using
`alex <https://github.com/get-alex/alex#cli>`_.

How to install alex
-------------------

To install alex run::

    $ npm install alex --global

Note that this required node, information on install node is available here:
https://www.npmjs.com/get-npm

How to run alex
---------------

To run alex on the documentation::

    $ alex docs**/*.rst

To run alex on the :code:`README.md` file::

    $ alex README.md

How to ignore some checks
-------------------------

To ignore some specific checks annotations can be used. For example
:ref:`john-nash-reference` is annotated to ignore insensitive related to
gendered pronouns:

.. code-block:: md
   :emphasize-lines: 1,2,14,15

   .. <!--alex disable he-she-->
   .. <!--alex disable her-him-->

   This library is named after the mathematician John Nash. He is most famous for
   his work in Game Theory that culminated in him winning a Noble prize in
   Economics. The book [Nasar2011]_ (popularized in a 2001 movie) gives a good
   overview of his life.

   The work he received a Noble prize for was a proof that a game **always** has
   an equilibrium [Nash1950]_. His proof is an exceptional piece of mathematics
   where he uses a fixed point theorem by showing that an equilibrium is equivalent
   to a fixed point of a function.

   ..  <!--alex enable he-she-->
   ..  <!--alex enable her-him-->

Another example is the :code:`README.md` file where an annotation is added to
ignore a specific use of the word "bi":

.. code-block:: md
   :emphasize-lines: 3

   ## Usage

   Create bi-matrix games by passing two 2 dimensional arrays/lists:
