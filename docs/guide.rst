User Guide
==========

Description
~~~~~~~~~~~

The :mod:`nmrstarlib` package provides a simple Python interface for parsing and
manipulating data stored in NMR-STAR format files used by Biological Magnetic
Resonance Data Bank (BMRB_) for archival of Nuclear Magnetic Resonance (NMR)
experimental data.

The :mod:`nmrstarlib` package provides facilities to convert NMR-STAR formatted files
into their equivalent JSONized (JavaScript Object Notation, an open-standard format that
uses human-readable text to transmit data objects consisting of attribute-value pairs)
representation and visa versa.

The :mod:`nmrstarlib` package also provides facilities to create simulated peak lists for
different types of standard solution and solid-state NMR experiments from chemical
shifts and assignment information deposited in NMR-STAR files.

In addition, the :mod:`nmrstarlib` package provides facilities to visualize assigned
chemical shift data.

Installation
~~~~~~~~~~~~

The :mod:`nmrstarlib` package runs under Python 2.7 and Python 3.4+.
Starting with Python 3.4, pip_ is included by default. To install
system-wide with pip_ run the following:

Install on Linux, Mac OS X
--------------------------

.. code:: bash

   python3 -m pip install nmrstarlib

Install on Windows
------------------

.. code:: bash

   py -3 -m pip install nmrstarlib

Install inside virtualenv
-------------------------

For an isolated install, you can run the same inside a virtualenv_.

.. code:: bash

   $ virtualenv -p /usr/bin/python3 venv  # create virtual environment, use python3 interpreter

   $ source venv/bin/activate             # activate virtual environment

   $ python3 -m pip install nmrstarlib    # install nmrstarlib as usually

   $ deactivate                           # if you are done working in the virtual environment

Get the source code
~~~~~~~~~~~~~~~~~~~

Code is available on GitHub: https://github.com/MoseleyBioinformaticsLab/nmrstarlib

You can either clone the public repository:

.. code:: bash

   $ https://github.com/MoseleyBioinformaticsLab/nmrstarlib.git

Or, download the tarball and/or zipball:

.. code:: bash

   $ curl -OL https://github.com/MoseleyBioinformaticsLab/nmrstarlib/tarball/master

   $ curl -OL https://github.com/MoseleyBioinformaticsLab/nmrstarlib/zipball/master

Once you have a copy of the source, you can embed it in your own Python package,
or install it into your system site-packages easily:

.. code:: bash

   $ python3 setup.py install

Dependencies
~~~~~~~~~~~~

The :mod:`nmrstarlib` package depends on several Python libraries, it will install all
dependencies automatically, but if you wish to install them manually run the
following commands:

   * docopt_ for creating :mod:`nmrstarlib` command-line interface.
      * To install docopt_ run the following:

        .. code:: bash

           python3 -m pip install docopt  # On Linux, Mac OS X
           py -3 -m pip install docopt    # On Windows

   * graphviz_ for visualizing assigned chemical shift values.
      * To install the graphviz_ Python library run the following:

        .. code:: bash

           python3 -m pip install graphviz  # On Linux, Mac OS X
           py -3 -m pip install graphviz    # On Windows

      * The only dependency of the graphviz_ Python library is a working
        installation of Graphviz (`Graphviz download page`_).

Optional dependencies
~~~~~~~~~~~~~~~~~~~~~

   * numpy_ for generating noise values from random distribution during peak list simulation.
      * To install the numpy_ Python library run the following:

        .. code:: bash

           python3 -m pip install numpy  # On Linux, Mac OS X
           py -3 -m pip install numpy    # On Windows

      * If the numpy_ is not installed distributions from the :py:mod:`random` will be used.


Basic usage
~~~~~~~~~~~

The :mod:`nmrstarlib` package can be used in several ways:

   * As a library for accessing and manipulating data stored in NMR-STAR format files.

      * Create the :class:`~nmrstarlib.nmrstarlib.StarFile` generator function that will generate
        (yield) single :class:`~nmrstarlib.nmrstarlib.StarFile` instance at a time.

      * Process each :class:`~nmrstarlib.nmrstarlib.StarFile` instance:

         * Process NMR-STAR files in a for-loop one file at a time.
         * Process as an iterator calling the :py:func:`next` built-in function.
         * Convert the generator into a :py:class:`list` of :class:`~nmrstarlib.nmrstarlib.StarFile` objects.

   * As a command-line tool:

      * Convert from NMR-STAR file format into its equivalent JSON file format and vice versa.
      * Create standard solution and solid-state NMR simulated peak lists from chemical shift values and
        assignment information.
      * Visualize (organize) assigned chemical shift values.

.. note:: Read :doc:`tutorial` to learn more and see code examples on using the :mod:`nmrstarlib`
          as a library and as a command-line tool.


.. _pip: https://pip.pypa.io/
.. _virtualenv: https://virtualenv.pypa.io/
.. _docopt: http://docopt.readthedocs.io/
.. _graphviz: http://graphviz.readthedocs.io/
.. _numpy: http://www.numpy.org/
.. _BMRB: http://www.bmrb.wisc.edu
.. _Graphviz download page: http://www.graphviz.org/Download.php
