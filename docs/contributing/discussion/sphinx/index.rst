.. _sphinx-discussion:

Using sphinx for documentation
==============================

TODO

Using sphinx-togglebutton for the questions
-------------------------------------------

TODO

Using matplotlib for plotting directives
----------------------------------------

The :code:`matplotlib` library includes a :code:`sphinx` plugin that allows for
plot directives.
To enable it, ensure that :code:`"matplotlib.sphinxext.plot_directive"` is
included in :code:`extensions` in :code:`conf.py`.

For example the following will create a plot::

   .. plot::

      import matplotlib.pyplot as plt
      import numpy as np

      xs = np.linspace(0, 10)
      plt.plot(xs, np.cos(xs))

.. plot::

  import matplotlib.pyplot as plt
  import numpy as np

  xs = np.linspace(0, 10)
  plt.plot(xs, np.cos(xs))

Using mermaid for diagrams
--------------------------

A popular tool for drawing diagrams is `mermaid.js <https://mermaid-js.github.io/>`_.
This can be used directly with
:code:`sphinx`.  To enable it, ensure that :code:`"sphinxcontrib.mermaid"` is
included in :code:`extensions` in :code:`conf.py`.

For example the following will create a flowchart::

   .. mermaid::

      graph TD;
         A-->B;
         A-->C;
         B-->D;
         C-->D;

.. mermaid::

   graph TD;
      A-->B;
      A-->C;
      B-->D;
      C-->D;
