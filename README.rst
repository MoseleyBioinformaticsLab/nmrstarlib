nmrstarlib
==========

The :mod:`nmrstarlib` package is a Python library that facilitates reading and writing
NMR-STAR formatted files used by the Biological Magnetic Resonance Data Bank (BMRB_)
for archival of Nuclear Magnetic Resonance (NMR) data.

The :mod:`nmrstarlib` package provides facilities to convert NMR-STAR formatted files into
their equivalent JSONized (JavaScript Object Notation, an open-standard format that
uses human-readable text to transmit data objects consisting of attribute-value pairs)
representation and vice versa.

In addition, the nmrstarlib package provides methods to visualize chemical shift data.

The :mod:`nmrstarlib` package can be used in several ways:

   * As a library for accessing and manipulating data stored in NMR-STAR format files.
   * As a command-line tool to convert between NMR-STAR format and its equivalent JSONized
     NMR-STAR format and also to visualize chemical shift data.

Links
~~~~~

   * nmrstarlib @ GitHub
   * nmrstarlib @ PyPI
   * Documentation @ ReadTheDocs

Installation
~~~~~~~~~~~~

The :mod:`nmrstarlib` package runs under Python 3, use pip_ to install. Starting with Python 3.4
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

Import :mod:`nmrstarlib` library and create generator function that will yield
:class:`~nmrstarlib.nmrstarlib.StarFile` instance(s):

>>> from nmrstarlib import nmrstarlib
>>>
>>> # "path": path_to_file / path_to_dir / path_to_archive / bmrb_id / file_url
>>> starfile_gen = nmrstarlib.read_files(["path"])
>>>
>>> for starfile in in starfile_gen:
...     print(starfile.bmrbid)         # print BMRB id of StarFile
...     print(starfile.source)         # print source of StarFile
...     print(list(starfile.keys()))   # print StarFile saveframe categories
>>>

.. note:: Read :doc:`guide` and :doc:`tutorial` to learn more and see code examples on using
          :mod:`nmrstarlib` as a library and as a command-line tool.

License
~~~~~~~

This package is distributed under the MIT_ :doc:`license`.

.. _pip: https://pip.pypa.io/
.. _docopt: http://docopt.readthedocs.io/
.. _graphviz: http://graphviz.readthedocs.io/
.. _BMRB: http://www.bmrb.wisc.edu
.. _download page: http://www.graphviz.org/Download.php

.. _MIT: http://opensource.org/licenses/MIT
