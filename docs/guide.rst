User Guide
==========

Description
~~~~~~~~~~~

:mod:`nmrstarlib` provides a simple Python interface for the parsing and manipulating
data stored in NMR-STAR format files used by Biological Magnetic Resonance Bank (BMRB_).

Installation
~~~~~~~~~~~~

:mod:`nmrstarlib` runs under Python 3.4+. To install system-wide with pip_ run the following:

.. code:: bash

    $ pip3 install nmrstarlib

For an isolated install, you can run the same inside a virtualenv.

.. code:: bash

   $ virtualenv -p /usr/bin/python3 venv  # create virtual environment, use python3 interpreter

   $ source venv/bin/activate             # activate virtual environment

   $ pip3 install nmrstarlib              # install nmrstarlib as usually

   $ deactivate                           # if you are done working in the virtual environment

Get the source code
~~~~~~~~~~~~~~~~~~~

Code is available on GitHub: **link pointing to github here**

You can either clone the public repository:

.. code:: bash

   $ git clone git://github.com/andreysmelter/nmrstarlib

Or, download the tarball:

.. code:: bash

   $ curl -OL https://github.com/andreysmelter/nmrstarlib/tarball/master
   # optionally, zipball is also available (for Windows users).

Once you have a copy of the source, you can embed it in your own Python package,
or install it into your system site-packages easily:

.. code:: bash

   $ python3 setup.py install

Dependencies
~~~~~~~~~~~~

:mod:`nmrstarlib` depends on several Python libraries:

   * docopt_ for creating :mod:`nmrstarlib` command-line interface.
      * To install docopt_ run the following:

        .. code:: bash

           pip3 install docopt

   * graphviz_ for visualizing assigned chemical shift values.
      * To install graphviz_ Python library run the following:

        .. code:: bash

           pip3 install graphviz

      * The only dependency of graphviz_ Python library is a working installation of Graphviz
        (`download page`_).


Basic usage
~~~~~~~~~~~

:mod:`nmrstarlib` can be used in several ways:

   * As a library for accessing and manipulating data stored in NMR-STAR format files.

      * Create :class:`~nmrstarlib.nmrstarlib.StarFile` generator function that will generate
        (yield) one :class:`~nmrstarlib.nmrstarlib.StarFile` at a time.

      * Process each :class:`~nmrstarlib.nmrstarlib.StarFile` object:

         * Process in a for-loop one file at a time.
         * Process as an iterator calling :py:func:`next` function.
         * Convert generator to a list of :class:`~nmrstarlib.nmrstarlib.StarFile` objects.

   * As a command-line tool:

      * Convert data from NMR-STAR format to JSON format or from JSON format to NMR-STAR format.
      * Visualize (organize) assigned chemical shift values.

Read :doc:`tutorial` to learn more and see code examples on using :mod:`nmrstarlib` as a library
and as a command-line tool.



.. _pip: http://pip.readthedocs.io
.. _docopt: http://docopt.readthedocs.io/
.. _graphviz: http://graphviz.readthedocs.io/
.. _BMRB: http://www.bmrb.wisc.edu
.. _download page: http://www.graphviz.org/Download.php
