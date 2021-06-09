Checking for insensitive language with alex
===========================================

`alex <https://github.com/get-alex/alex#cli>`_ is a tool that allows you to identify insensitive and/or inconsiderate
language in written prose. The following description is taken from the project
page:

    "Whether your own or someone else’s writing, alex helps you find gender
    favoring, polarizing, race related, religion inconsiderate, or other unequal
    phrasing in text."

As an example consider the following markdown file:

.. literalinclude:: /_static/contributing/discussion/alex/main.md

If we run alex on it::

    $ alex main.md

We get::

    $ alex main.md
    main.md
    3:1-3:3  warning  `He` may be insensitive, use `They`, `It` instead  he-she  retext-equality

    ⚠ 1 warning


Correcting the markdown file to:

.. literalinclude:: /_static/contributing/discussion/alex/correct_main.md

Running alex now gives::

    $ alex main.md
    main.md: no issues found

The above example is quite a clear one, alex assists by identifying errors like
this but also more subtle ones.

It is possible to ignore certain checks `using a configuration file
<https://github.com/get-alex/alex#configuration>`_ but as described in :ref:`the
how to guide <how-to-check-for-insensitive-language>` it is also possible to
annotate the file itself. This is preferred as it makes exceptions explicit.

FAQ
---

The Frequently asked questions about alex can be found here: https://github.com/get-alex/alex#faq
This includes:

    Q: This is stupid!

    A: Not a question. And yeah, alex isn’t very smart. People are much better
    at this. But people make mistakes, and alex is there to help

The Nashpy library uses alex for exactly this reason, it is one of many efforts
made to ensure the project is inclusive.
