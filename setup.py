#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
import re
from setuptools import setup, find_packages, Extension

try:
    from Cython.Distutils import build_ext
    HAVE_CYTHON = True
except ImportError:
    from setuptools.command.build_ext import build_ext
    HAVE_CYTHON = False


if sys.argv[-1] == 'publish':
    os.system('python3 setup.py sdist')
    os.system('twine upload dist/*')
    sys.exit()


def readme():
    with open('README.rst') as readme_file:
        return readme_file.read()


def find_version():
    with open('nmrstarlib/__init__.py', 'r') as fd:
        version = re.search(r'^__version__\s*=\s*[\'"]([^\'"]*)[\'"]',
                            fd.read(), re.MULTILINE).group(1)
    if not version:
        raise RuntimeError('Cannot find version information')
    return version


REQUIRES = [
    'docopt >= 0.6.2',
    'graphviz >= 0.5.2'
]


EXTENSIONS = []


if HAVE_CYTHON:
    EXTENSIONS.append(Extension('nmrstarlib.cbmrblex',
                                sources=['nmrstarlib/cbmrblex.pyx']))
else:
    EXTENSIONS.append(Extension('nmrstarlib.cbmrblex',
                                sources=['nmrstarlib/cbmrblex.c']))

setup(
    name='nmrstarlib',
    version=find_version(),
    author='Andrey Smelter',
    author_email='andrey.smelter@gmail.com',
    description='Python library for parsing data from NMR-STAR format files',
    keywords='BMRB NMR-STAR parsing nmrstarlib',
    license='MIT',
    url='https://github.com/MoseleyBioinformaticsLab/nmrstarlib',
    packages=find_packages(),
    package_data={'nmrstarlib': ['conf/*.json']},
    platforms='any',
    long_description=readme(),
    install_requires=REQUIRES,
    cmdclass={"build_ext": build_ext},
    ext_modules=EXTENSIONS,
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Topic :: Scientific/Engineering :: Bio-Informatics',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
)
