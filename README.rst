nmrstarlib
==========

.. image:: https://img.shields.io/pypi/l/nmrstarlib.svg
   :target: https://choosealicense.com/licenses/mit/
   :alt: License information

.. image:: https://img.shields.io/pypi/v/nmrstarlib.svg
   :target: https://pypi.org/project/nmrstarlib/
   :alt: Current library version

.. image:: https://img.shields.io/pypi/pyversions/nmrstarlib.svg
   :target: https://pypi.org/project/nmrstarlib/
   :alt: Supported Python versions

.. image:: https://readthedocs.org/projects/nmrstarlib/badge/?version=latest
   :target: http://nmrstarlib.readthedocs.io/en/latest/?badge=latest
   :alt: Documentation status

.. image:: https://api.travis-ci.org/MoseleyBioinformaticsLab/nmrstarlib.svg?branch=master
   :target: https://travis-ci.org/MoseleyBioinformaticsLab/nmrstarlib
   :alt: Travis CI status

.. image:: https://codecov.io/gh/MoseleyBioinformaticsLab/nmrstarlib/branch/master/graphs/badge.svg?branch=master
   :target: https://codecov.io/gh/MoseleyBioinformaticsLab/nmrstarlib
   :alt: Code coverage information

.. image:: https://img.shields.io/badge/DOI-10.1186%2Fs12859--017--1580--5-blue.svg
   :target: http://bmcbioinformatics.biomedcentral.com/articles/10.1186/s12859-017-1580-5
   :alt: Citation link

.. image:: https://pepy.tech/badge/nmrstarlib
   :target: https://pepy.tech/project/nmrstarlib
   :alt: Downloads

|

.. image:: https://raw.githubusercontent.com/MoseleyBioinformaticsLab/nmrstarlib/master/docs/_static/images/nmrstarlib_logo.png
   :width: 50%
   :align: center
   :target: http://nmrstarlib.readthedocs.io/

The `nmrstarlib` package is a Python library that facilitates reading and writing
NMR-STAR formatted files used by the Biological Magnetic Resonance Data Bank (BMRB_)
for archival of Nuclear Magnetic Resonance (NMR) data and CIF formatted files used
by Protein Data Bank (PDB_).

The `nmrstarlib` package provides facilities to convert NMR-STAR and CIF formatted
files into their equivalent JSONized representation and vice versa. JSON stands
for JavaScript Object Notation, an open-standard format that uses human-readable
text to transmit data objects consisting of attribute-value pairs.

The `nmrstarlib` package also provides facilities to create simulated peak lists for
different types of standard solution and solid-state NMR experiments from chemical
shifts and assignment information deposited in NMR-STAR files.

In addition, the `nmrstarlib` package provides methods to visualize chemical shift data.

The `nmrstarlib` package can be used in several ways:

   * As a library for accessing and manipulating data stored in NMR-STAR and CIF formatted files.
   * As a command-line tool to convert between NMR-STAR/CIF format and its equivalent JSONized
     NMR-STAR/CIF format, to create a large number of simulated peak lists,
     and also to visualize chemical shift data from NMR-STAR formatted files.

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

The `nmrstarlib` package runs under Python 2.7 and Python 3.4+. Use pip_ to install.
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
`StarFile` instance(s):

.. code:: python

   >>> import nmrstarlib
   >>>
   >>> # "path": path_to_file / path_to_dir / path_to_archive / bmrb_id / pdb_id / file_url
   >>> for file in nmrstarlib.read_files("path"):
   ...     print(file.id)      # print BMRB/PDB id of a file
   ...     print(file.source)  # print source of a file
   ...     print(file.keys())  # print top-level keys
   >>>

.. image:: https://raw.githubusercontent.com/MoseleyBioinformaticsLab/nmrstarlib/master/docs/_static/images/nmrstarlib_demo.gif
   :align: center


.. note:: Read the `User Guide`_ and `The nmrstarlib Tutorial`_ on ReadTheDocs_
          to learn more and to see code examples on using the `nmrstarlib` as a
          library and as a command-line tool.

License
~~~~~~~

This package is distributed under the MIT_ `license`.

.. _pip: https://pip.pypa.io
.. _docopt: http://docopt.readthedocs.io
.. _graphviz: http://graphviz.readthedocs.io
.. _BMRB: http://www.bmrb.wisc.edu
.. _PDB: https://www.rcsb.org
.. _Graphviz download page: http://www.graphviz.org/Download.php

.. _GitHub: https://github.com/MoseleyBioinformaticsLab/nmrstarlib
.. _ReadTheDocs: http://nmrstarlib.readthedocs.io
.. _User Guide: http://nmrstarlib.readthedocs.io/en/latest/guide.html
.. _The nmrstarlib Tutorial: http://nmrstarlib.readthedocs.io/en/latest/tutorial.html
.. _PyPI: https://pypi.org/project/nmrstarlib

.. _MIT: https://choosealicense.com/licenses/mit

.. _10.1186/s12859-017-1580-5: http://bmcbioinformatics.biomedcentral.com/articles/10.1186/s12859-017-1580-5
