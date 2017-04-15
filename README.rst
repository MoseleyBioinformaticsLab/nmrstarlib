nmrstarlib
==========

.. image:: https://raw.githubusercontent.com/MoseleyBioinformaticsLab/nmrstarlib/master/docs/_static/images/nmrstarlib_logo.png
  :width: 50%
  :align: center

The `nmrstarlib` package is a Python library that facilitates reading and writing
NMR-STAR formatted files used by the Biological Magnetic Resonance Data Bank (BMRB_)
for archival of Nuclear Magnetic Resonance (NMR) data.

The `nmrstarlib` package provides facilities to convert NMR-STAR formatted files into
their equivalent JSONized (JavaScript Object Notation, an open-standard format that
uses human-readable text to transmit data objects consisting of attribute-value pairs)
representation and vice versa.

The `nmrstarlib` package also provides facilities to create simulated peak lists for
different types of standard solution and solid-state NMR experiments from chemical
shifts and assignment information deposited in NMR-STAR files.

In addition, the `nmrstarlib` package provides methods to visualize chemical shift data.

The `nmrstarlib` package can be used in several ways:

   * As a library for accessing and manipulating data stored in NMR-STAR format files.
   * As a command-line tool to convert between NMR-STAR format and its equivalent JSONized
     NMR-STAR format, to create a large number of simulated peak lists,
     and also to visualize chemical shift data.

Citation
~~~~~~~~

When using `nmrstarlib` in published work, please cite the following paper:

   * Smelter, Andrey, Morgan Astra, and Hunter NB Moseley. "A fast and efficient python
     library for interfacing with the Biological Magnetic Resonance Data Bank."
     *BMC Bioinformatics* 18.1 (2017): 175. doi: `10.1186/s12859-017-1580-5`_.


Links
~~~~~

   * nmrstarlib @ GitHub_
   * nmrstarlib @ PyPI_
   * Documentation @ ReadTheDocs_

Installation
~~~~~~~~~~~~

The `nmrstarlib` package runs under Python 2.7 and Python 3.4+, use pip_ to install.
Starting with Python 3.4, pip_ is included by default.

Install on Linux, Mac OS X
--------------------------

.. code:: bash

   python3 -m pip install nmrstarlib

Install on Windows
------------------

.. code:: bash

   py -3 -m pip install nmrstarlib

Quickstart
~~~~~~~~~~

Import `nmrstarlib` library and create generator function that will yield
`nmrstarlib.nmrstarlib.StarFile` instance(s):

.. code:: python

   >>> from nmrstarlib import nmrstarlib
   >>>
   >>> # "path": path_to_file / path_to_dir / path_to_archive / bmrb_id / file_url
   >>> starfile_gen = nmrstarlib.read_files("path")
   >>>
   >>> for starfile in starfile_gen:
   ...     print(starfile.bmrbid)         # print BMRB id of StarFile
   ...     print(starfile.source)         # print source of StarFile
   ...     print(list(starfile.keys()))   # print StarFile saveframe categories
   >>>
   >>> # For example, let's read two files: one using BMRB id and the other one using URL:
   >>> starfile_gen = nmrstarlib.read_files("15000", "http://rest.bmrb.wisc.edu/bmrb/NMR-STAR3/18569")
   >>>
   >>> for starfile in starfile_gen:
   ...     print("BMRB id:", starfile.bmrbid)
   ...     print("Source:", starfile.source)
   ...     print("List of saveframes and comments:", list(starfile.keys()))
   >>>


.. note:: Read the `User Guide`_ and `The nmrstarlib Tutorial`_ on ReadTheDocs_
          to learn more and to see code examples on using the `nmrstarlib` as a
          library and as a command-line tool.

License
~~~~~~~

This package is distributed under the MIT_ `license`.

.. _pip: https://pip.pypa.io/
.. _docopt: http://docopt.readthedocs.io/
.. _graphviz: http://graphviz.readthedocs.io/
.. _BMRB: http://www.bmrb.wisc.edu
.. _Graphviz download page: http://www.graphviz.org/Download.php

.. _GitHub: https://github.com/MoseleyBioinformaticsLab/nmrstarlib
.. _ReadTheDocs: http://nmrstarlib.readthedocs.io/
.. _User Guide: http://nmrstarlib.readthedocs.io/en/latest/guide.html
.. _The nmrstarlib Tutorial: http://nmrstarlib.readthedocs.io/en/latest/tutorial.html
.. _PyPI: https://pypi.python.org/pypi/nmrstarlib

.. _MIT: http://opensource.org/licenses/MIT

.. _10.1186/s12859-017-1580-5: http://bmcbioinformatics.biomedcentral.com/articles/10.1186/s12859-017-1580-5
