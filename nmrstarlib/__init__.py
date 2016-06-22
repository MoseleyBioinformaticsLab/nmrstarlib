"""Routines for working with BMRB NMR-STAR format files.

This package includes two modules:

``nmrstarlib``
    This module provides :class:`~nmrstarlib.nmrstarlib.StarFile` class which is a python
    dictionary representation of BMRB NMR-STAR file. Data can be accessed
    directly from the :class:`~nmrstarlib.nmrstarlib.StarFile` instance using bracket accessors.
    :mod:`~nmrstarlib.nmrstarlib` relies on :mod:`~nmrstarlib.bmrblex` for processing tokens.


``bmrblex``
    This module provides :class:`~nmrstarlib.bmrblex.bmrblex` class that is responsible for
    syntax analysis if BMRB NMR-STAR files, processing word, number,
    single quoted, double quoted, multiline quoted BMRB tokens.

"""