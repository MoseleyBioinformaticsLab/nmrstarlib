#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Routines for working with BMRB NMR-STAR format files.

This package includes the following modules:

``nmrstarlib``
    This module provides the :class:`~nmrstarlib.nmrstarlib.StarFile` class which is a python
    dictionary representation of a BMRB NMR-STAR file. Data can be accessed
    directly from the :class:`~nmrstarlib.nmrstarlib.StarFile` instance using bracket accessors.
    The :mod:`~nmrstarlib.nmrstarlib` module relies on the :mod:`~nmrstarlib.bmrblex` module
    for processing of tokens.

``bmrblex``
    This module provides the :func:`~nmrstarlib.bmrblex.bmrblex` generator that is responsible
    for the syntax analysis of BMRB NMR-STAR files, processing word, number, single quoted,
    double quoted, multiline quoted BMRB tokens.

``converter``
    This module provides the :class:`~nmrstarlib.converter.Converter` class that is
    responsible for the conversion of NMR-STAR formated files.

``csviewer``
    This module provides the :class:`~nmrstarlib.csviewer.CSViewer` class that visualizes
    chemical shift values using the Graphviz (http://www.graphviz.org/) DOT Languge description
    and provides code example for utilizing the library.

``noise``
    This module provides the :class:`~nmrstarlib.noise.NoiseGenerator` abstract class and derived
    :class:`~nmrstarlib.noise.RandomNormalNoiseGenerator` for adding random normal noise values
    to peaks in simulated peak list.

``plsimulator``
    This module provides necessary interfaces in order to create a simulated
    :class:`~nmrstarlib.plsimulator.PeakList`.

``translator``
    This module provides :class:`~nmrstarlib.translator.StarFileToStarFile` for
    conversion between NMR-STAR and JSONized NMR-STAR formatted files and
    :class:`~nmrstarlib.translator.StarFileToPeakList` for conversion of NMR-STAR
    formatted files into peak list files using chemical shift values and assignment
    information.
"""

__version__ = "2.0.0"