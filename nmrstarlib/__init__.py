"""Routines for working with BMRB NMR-STAR format files.

This package includes the following modules:

``nmrstarlib``
    This module provides :class:`~nmrstarlib.nmrstarlib.StarFile` class which is a python
    dictionary representation of BMRB NMR-STAR file. Data can be accessed
    directly from the :class:`~nmrstarlib.nmrstarlib.StarFile` instance using bracket accessors.
    :mod:`~nmrstarlib.nmrstarlib` relies on :mod:`~nmrstarlib.bmrblex` for processing of tokens.


``bmrblex``
    This module provides :class:`~nmrstarlib.bmrblex.bmrblex` class that is responsible for
    syntax analysis of BMRB NMR-STAR files, processing word, number,
    single quoted, double quoted, multiline quoted BMRB tokens.

``converter``
    This module provides :class:`~nmrstarlib.converter.Converter` class that is responsible for
    conversion of NMR-STAR files into JSON format and back to NMR-STAR format.

``csviewer``
    This module provides :func:`~nmrstarlib.csviewer.csviewer` function that visualizes
    chemical shift values using graphviz (http://www.graphviz.org/) DOT Languge description.
"""
import os
from . import nmrstarlib

this_directory = os.path.dirname(__file__)
config_file = os.path.join(this_directory, '../conf/constants.json')
nmrstarlib.update_constants(config_file)