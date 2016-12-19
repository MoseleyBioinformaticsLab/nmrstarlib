nmrstarlib
==========

The `nmrstarlib` package is a Python library that facilitates reading and writing
NMR-STAR formatted files used by the Biological Magnetic Resonance Data Bank (BMRB_)
for archival of Nuclear Magnetic Resonance (NMR) data.

The `nmrstarlib` package provides facilities to convert NMR-STAR formatted files into
their equivalent JSONized (JavaScript Object Notation, an open-standard format that
uses human-readable text to transmit data objects consisting of attribute-value pairs)
representation and vice versa.

In addition, the nmrstarlib package provides methods to visualize chemical shift data.

The `nmrstarlib` package can be used in several ways:

   * As a library for accessing and manipulating data stored in NMR-STAR format files.
   * As a command-line tool to convert between NMR-STAR format and its equivalent JSONized
     NMR-STAR format and also to visualize chemical shift data.

Links
~~~~~

   * nmrstarlib @ GitHub_
   * nmrstarlib @ PyPI_
   * Documentation @ ReadTheDocs_

Installation
~~~~~~~~~~~~

The `nmrstarlib` package runs under Python 3, use pip_ to install. Starting with Python 3.4
pip_ is included by default.

Install on Linux, Mac OS X
--------------------------

.. code:: bash

   python3 -m pip install nmrstarlib

Also make sure that dependencies are installed on the system:

.. code:: bash

   python3 -m pip install docopt
   python3 -m pip install graphviz

graphviz_ Python library requires a working installation of Graphviz (`download page`_).

Install on Windows
------------------

.. code:: bash

   py -3 -m pip install nmrstarlib

Also make sure that dependencies are installed on the system:

.. code:: bash

   py -3 -m pip install docopt
   py -3 -m pip install graphviz

graphviz_ Python library requires a working installation of Graphviz (`download page`_).


Quickstart
~~~~~~~~~~

Import `nmrstarlib` library and create generator function that will yield
`nmrstarlib.nmrstarlib.StarFile` instance(s):

.. code:: python

   >>> from nmrstarlib import nmrstarlib
   >>>
   >>> # "path": path_to_file / path_to_dir / path_to_archive / bmrb_id / file_url
   >>> starfile_gen = nmrstarlib.read_files(["path"])
   >>>
   >>> for starfile in starfile_gen:
   ...     print(starfile.bmrbid)         # print BMRB id of StarFile
   ...     print(starfile.source)         # print source of StarFile
   ...     print(list(starfile.keys()))   # print StarFile saveframe categories
   >>>

.. note:: Read `User Guide`_ and `The nmrstarlib Tutorial`_ on ReadTheDocs_ to learn more and see code examples on using
          `nmrstarlib` as a library and as a command-line tool.

License
~~~~~~~

This package is distributed under the MIT_ `license`.

.. _pip: https://pip.pypa.io/
.. _docopt: http://docopt.readthedocs.io/
.. _graphviz: http://graphviz.readthedocs.io/
.. _BMRB: http://www.bmrb.wisc.edu
.. _download page: http://www.graphviz.org/Download.php

.. _GitHub: https://github.com/MoseleyBioinformaticsLab/nmrstarlib
.. _ReadTheDocs: http://nmrstarlib.readthedocs.io/
.. _User Guide: http://nmrstarlib.readthedocs.io/en/latest/guide.html
.. _The nmrstarlib Tutorial: http://nmrstarlib.readthedocs.io/en/latest/tutorial.html
.. _PyPI: https://pypi.python.org/pypi/nmrstarlib

.. _MIT: http://opensource.org/licenses/MIT
