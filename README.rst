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

The `nmrstarlib` package runs under Python 2.7 and Python 3.4+, use pip_ to install. Starting with Python 3.4
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
   BMRB id: 15000
   Source: http://rest.bmrb.wisc.edu/bmrb/NMR-STAR3/15000
   List of saveframes and comments: ['data', 'comment_0', 'save_entry_information', 'comment_1',
   'save_citation_1', 'comment_2', 'save_assembly', 'comment_3', 'save_F5-Phe-cVHP', 'comment_4',
   'save_natural_source', 'comment_5', 'save_experimental_source', 'comment_6','save_chem_comp_PHF',
   'comment_7', 'comment_8', 'save_unlabeled_sample', 'save_selectively_labeled_sample',
   'comment_9', 'save_sample_conditions', 'comment_10', 'save_NMRPipe', 'save_PIPP', 'save_SPARKY',
   'save_CYANA', 'save_X-PLOR_NIH', 'comment_11', 'comment_12', 'save_spectrometer_1',
   'save_spectrometer_2', 'save_spectrometer_3', 'save_spectrometer_4', 'save_spectrometer_5',
   'save_spectrometer_6', 'save_NMR_spectrometer_list', 'comment_13', 'save_experiment_list',
   'comment_14', 'comment_15', 'comment_16', 'save_chemical_shift_reference_1', 'comment_17',
   'comment_18', 'save_assigned_chem_shift_list_1']
   BMRB id: 18569
   Source: http://rest.bmrb.wisc.edu/bmrb/NMR-STAR3/18569
   List of saveframes and comments: ['data', 'comment_0', 'save_entry_information', 'comment_1',
   'save_entry_citation', 'comment_2', 'save_assembly', 'comment_3', 'save_EVH1', 'comment_4',
   'save_natural_source', 'comment_5', 'save_experimental_source', 'comment_6', 'comment_7',
   'save_sample_1', 'save_sample_2', 'save_sample_3', 'save_sample_4', 'comment_8',
   'save_sample_conditions_1', 'save_sample_conditions_2', 'save_sample_conditions_3',
   'save_sample_conditions_4', 'comment_9', 'save_AZARA', 'save_xwinnmr', 'save_ANSIG',
   'save_CNS', 'comment_10', 'comment_11', 'save_spectrometer_1', 'save_spectrometer_2',
   'save_NMR_spectrometer_list', 'comment_12', 'save_experiment_list', 'comment_13',
   'comment_14', 'comment_15', 'save_chemical_shift_reference_1', 'comment_16', 'comment_17',
   'save_assigned_chem_shift_list_1', 'comment_18', 'save_combined_NOESY_peak_list']

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

.. _10.1186/s12859-017-1580-5: http://bmcbioinformatics.biomedcentral.com/articles/10.1186/s12859-017-1580-5
