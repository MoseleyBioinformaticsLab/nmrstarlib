"""Routines for working with BMRB NMR-STAR format files.

This package includes the following modules:

``nmrstarlib``
    This module provides the :class:`~nmrstarlib.nmrstarlib.StarFile` class which is a python
    dictionary representation of a BMRB NMR-STAR file. Data can be accessed
    directly from the :class:`~nmrstarlib.nmrstarlib.StarFile` instance using bracket accessors.
    The :mod:`~nmrstarlib.nmrstarlib` module relies on the :mod:`~nmrstarlib.bmrblex` module
    for processing of tokens.

``bmrblex``
    This module provides the :class:`~nmrstarlib.bmrblex.bmrblex` class that is responsible for
    the syntax analysis of BMRB NMR-STAR files, processing word, number, single quoted,
    double quoted, multiline quoted BMRB tokens.

``converter``
    This module provides the :class:`~nmrstarlib.converter.Converter` class that is
    responsible for the conversion between NMR-STAR formated files and an equivalent
    JSONized file format.

``csviewer``
    This module provides the :func:`~nmrstarlib.csviewer.csviewer` function that visualizes
    chemical shift values using the Graphviz (http://www.graphviz.org/) DOT Languge description.
"""

import os
from . import nmrstarlib

this_directory = os.path.dirname(__file__)
config_file = os.path.join(this_directory, '../conf/constants.json')
nmrstarlib.update_constants(config_file)
