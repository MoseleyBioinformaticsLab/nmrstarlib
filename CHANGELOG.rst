.. :changelog:

Release History
===============

1.0.5 (2017-01-10)
~~~~~~~~~~~~~~~~~~
**Improvements**

- New faster `bmrblex.py` lexical analyzer module based on Python generators.
- Added Cythonized version of `bmrblex` (`cbmrblex.pyx`) for faster tokenization.
- API change: new `nmrstarlib.read_files()` generator that does not require passing list.
- API change: new `StarFile.chem_shifts_by_residue()` representation.
- Added automated tests for `pytest` framework.

1.0.4 (2016-10-06)
~~~~~~~~~~~~~~~~~~

**Bugfixes**

- Fixed broken configuration file path.

1.0.0 (2016-05-25)
~~~~~~~~~~~~~~~~~~

- Initial public release.