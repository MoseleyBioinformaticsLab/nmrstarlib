.. :changelog:

Release History
===============

2.0.4 (2017-10-26)
~~~~~~~~~~~~~~~~~~

**New features**

- Added seed optional parameter to keep simulated peak lists reproducible from run to run.

**Improvements**
- Improved cli option names.
- Additional unit tests.


2.0.3 (2017-08-03)
~~~~~~~~~~~~~~~~~~

**New features**

- Added additional statistical distributions that can be used to generate per-dimension
  noise values during peak list simulations (if numpy is installed additional statistical
  distributions can be used).

**Improvements**

- Added continuous integration with Travis CI.
- Added code coverage reports with Codecov.

**Bugfixes**

- Fixed issue #2: https://github.com/MoseleyBioinformaticsLab/nmrstarlib/issues/2
- Fixed issue #5: https://github.com/MoseleyBioinformaticsLab/nmrstarlib/issues/5
- Fixed issue #6: https://github.com/MoseleyBioinformaticsLab/nmrstarlib/issues/6


2.0.2 (2017-06-09)
~~~~~~~~~~~~~~~~~~

**Bugfixes**

- Fixed bug related to sorting of the sequence ids which caused
  problems during sequence sites creation in peak list simulation.
  Sorting is based on integer sequence id value instead of its string
  representation.


2.0.1 (2017-05-11)
~~~~~~~~~~~~~~~~~~

**Bugfixes**

- Fixed issue #4: https://github.com/MoseleyBioinformaticsLab/nmrstarlib/issues/4
- Fixed issue #7: https://github.com/MoseleyBioinformaticsLab/nmrstarlib/issues/7


2.0.0 (2017-04-11)
~~~~~~~~~~~~~~~~~~
**New features**

- Added ability to create simulated peak lists from assigned chemical shifts values.

**Improvements**

- Added new `User Guide` and `Tutorial` documentation.


1.1.0 (2017-01-11)
~~~~~~~~~~~~~~~~~~
**New features**

- Added support for Python 2.7.
- Added support for ``ujson`` library.
- Added ability to preserve comments.

**Improvements**

- New faster ``bmrblex.py`` lexical analyzer module based on Python generators.
- Added Cythonized version of ``bmrblex`` (``cbmrblex.pyx``) for faster tokenization.
- API change: new ``nmrstarlib.read_files()`` generator that does not require passing list.
- API change: new ``StarFile.chem_shifts_by_residue()`` representation.
- Improved printing layout for original NMR-STAR format when printing from ``StarFile`` object.
- Added automated tests for ``pytest`` framework.


1.0.4 (2016-10-06)
~~~~~~~~~~~~~~~~~~

**Bugfixes**

- Fixed broken configuration file path.


1.0.0 (2016-05-25)
~~~~~~~~~~~~~~~~~~

- Initial public release.