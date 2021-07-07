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
