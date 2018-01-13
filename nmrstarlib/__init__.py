#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Routines for working with ``BMRB NMR-STAR`` and ``PDB CIF`` formatted files.

This package includes the following modules:

``nmrstarlib``
    This module provides the :class:`~nmrstarlib.nmrstarlib.StarFile` superclass and 
    :class:`~nmrstarlib.nmrstarlib.NMRStarFile` and :class:`~nmrstarlib.nmrstarlib.CIFFile`
    which are python dictionary representation of a BMRB NMR-STAR file and PDB CIF file, 
    respectively. Data can be accessed directly from the instance using bracket accessors.
    The :mod:`~nmrstarlib.nmrstarlib` module relies on the :mod:`~nmrstarlib.bmrblex` module
    for processing of tokens.

``bmrblex``
    This module provides the :func:`~nmrstarlib.bmrblex.bmrblex` generator that is responsible
    for the syntax analysis of BMRB NMR-STAR and PDB CIF files, processing word, number, single quoted,
    double quoted, multiline quoted tokens.

``converter``
    This module provides the :class:`~nmrstarlib.converter.Converter` class that is
    responsible for the conversion of NMR-STAR and CIF formatted files.

``csviewer``
    This module provides the :class:`~nmrstarlib.csviewer.CSViewer` class that visualizes
    chemical shift values from NMR-STAR files using the Graphviz (http://www.graphviz.org/) 
    DOT Languge description and provides code example for utilizing the library.

``noise``
    This module provides the :class:`~nmrstarlib.noise.NoiseGenerator` class 
    for adding random normal noise values to peaks in simulated peak list for 
    NMR-STAR formatted files.

``plsimulator``
    This module provides necessary interfaces in order to create a simulated
    :class:`~nmrstarlib.plsimulator.PeakList` from NMR-STAR formatted files.

``translator``
    This module provides :class:`~nmrstarlib.translator.StarFileToStarFile` for
    conversion between NMR-STAR/CIF and JSONized NMR-STAR/CIF formatted files and
    :class:`~nmrstarlib.translator.StarFileToPeakList` for conversion of NMR-STAR
    formatted files into peak list files using chemical shift values and assignment
    information.

``fileio``
    This module provides the :func:`~nmrstarlib.fileio.read_files` generator
    to open files from different sources (single file/multiple files on a local 
    machine, directory/archive of files, URL address of a file).
"""

__version__ = "2.1.0"


from .fileio import read_files
