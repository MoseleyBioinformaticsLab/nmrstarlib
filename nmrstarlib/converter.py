#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
nmrstarlib.converter
~~~~~~~~~~~~~~~~~~~~

This module provides functionality for converting between the BMRB
NMR-STAR format and its equivalent JSONized NMR-STAR format.

The following conversions are possible:

Local files:
   * One-to-one file conversions:
      * textfile - to - textfile
      * textfile - to - textfile.gz
      * textfile - to - textfile.bz2
      * textfile.gz - to - textfile
      * textfile.gz - to - textfile.gz
      * textfile.gz - to - textfile.bz2
      * textfile.bz2 - to - textfile
      * textfile.bz2 - to - textfile.gz
      * textfile.bz2 - to - textfile.bz2
      * textfile / textfile.gz / textfile.bz2 - to - textfile.zip / textfile.tar / textfile.tar.gz / textfile.tar.bz2 (TypeError: One-to-many conversion)
   * Many-to-many files conversions:
      * Directories:
         * directory - to - directory
         * directory - to - directory.zip
         * directory - to - directory.tar
         * directory - to - directory.tar.bz2
         * directory - to - directory.tar.gz
         * directory - to - directory.gz / directory.bz2 (TypeError: Many-to-one conversion)
      * Zipfiles:
         * zipfile.zip - to - directory
         * zipfile.zip - to - zipfile.zip
         * zipfile.zip - to - tarfile.tar
         * zipfile.zip - to - tarfile.tar.gz
         * zipfile.zip - to - tarfile.tar.bz2
         * zipfile.zip - to - directory.gz / directory.bz2 (TypeError: Many-to-one conversion)
      * Tarfiles:
         * tarfile.tar - to - directory
         * tarfile.tar - to - zipfile.zip
         * tarfile.tar - to - tarfile.tar
         * tarfile.tar - to - tarfile.tar.gz
         * tarfile.tar - to - tarfile.tar.bz2
         * tarfile.tar - to - directory.gz / directory.bz2 (TypeError: Many-to-one conversion)
         * tarfile.tar.gz - to - directory
         * tarfile.tar.gz - to - zipfile.zip
         * tarfile.tar.gz - to - tarfile.tar
         * tarfile.tar.gz - to - tarfile.tar.gz
         * tarfile.tar.gz - to - tarfile.tar.bz2
         * tarfile.tar.gz - to - directory.gz / directory.bz2 (TypeError: Many-to-one conversion)
         * tarfile.tar.bz2 - to - directory
         * tarfile.tar.bz2 - to - zipfile.zip
         * tarfile.tar.bz2 - to - tarfile.tar
         * tarfile.tar.bz2 - to - tarfile.tar.gz
         * tarfile.tar.bz2 - to - tarfile.tar.bz2
         * tarfile.tar.bz2 - to - directory.gz / directory.bz2 (TypeError: Many-to-one conversion)
URL files:
   * One-to-one file conversions:
      * bmrbid - to - textfile
      * bmrbid - to - textfile.gz
      * bmrbid - to - textfile.bz2
      * bmrbid - to - textfile.zip / textfile.tar / textfile.tar.gz / textfile.tar.bz2 (TypeError: One-to-many conversion)
      * textfileurl - to - textfile
      * textfileurl - to - textfile.gz
      * textfileurl - to - textfile.bz2
      * textfileurl.gz - to - textfile
      * textfileurl.gz - to - textfile.gz
      * textfileurl.gz - to - textfile.bz2
      * textfileurl.bz2 - to - textfile
      * textfileurl.bz2 - to - textfile.gz
      * textfileurl.bz2 - to - textfile.bz2
      * textfileurl / textfileurl.gz / textfileurl.bz2 - to - textfile.zip / textfile.tar / textfile.tar.gz / textfile.tar.bz2 (TypeError: One-to-many conversion)
   * Many-to-many files conversions:
      * Zipfiles:
         * zipfileurl.zip - to - directory
         * zipfileurl.zip - to - zipfile.zip
         * zipfileurl.zip - to - tarfile.tar
         * zipfileurl.zip - to - tarfile.tar.gz
         * zipfileurl.zip - to - tarfile.tar.bz2
         * zipfileurl.zip - to - directory.gz / directory.bz2 (TypeError: Many-to-one conversion)
      * Tarfiles:
         * tarfileurl.tar - to - directory
         * tarfileurl.tar - to - zipfile.zip
         * tarfileurl.tar - to - tarfile.tar
         * tarfileurl.tar - to - tarfile.tar.gz
         * tarfileurl.tar - to - tarfile.tar.bz2
         * tarfileurl.tar - to - directory.gz / directory.bz2 (TypeError: Many-to-one conversion)
         * tarfileurl.tar.gz - to - directory
         * tarfileurl.tar.gz - to - zipfile.zip
         * tarfileurl.tar.gz - to - tarfile.tar
         * tarfileurl.tar.gz - to - tarfile.tar.gz
         * tarfileurl.tar.gz - to - tarfile.tar.bz2
         * tarfileurl.tar.gz - to - directory.gz / directory.bz2 (TypeError: Many-to-one conversion)
         * tarfileurl.tar.bz2 - to - directory
         * tarfileurl.tar.bz2 - to - zipfile.zip
         * tarfileurl.tar.bz2 - to - tarfile.tar
         * tarfileurl.tar.bz2 - to - tarfile.tar.gz
         * tarfileurl.tar.bz2 - to - tarfile.tar.bz2
         * tarfileurl.tar.bz2 - to - directory.gz / directory.bz2 (TypeError: Many-to-one conversion)
"""

import os
import io
import zipfile
import tarfile
import bz2
import gzip

from . import nmrstarlib


class Converter(object):
    """Converter class to convert BMRB NMR-STAR files from NMR-STAR to JSON or from JSON to NMR-STAR format."""

    nmrstar_extension = {"json":    ".json",
                         "nmrstar": ".str"}

    def __init__(self, from_path, to_path, from_format="nmrstar", to_format="json"):
        """Converter initializer.

        :param str from_path: Path to input file(s).
        :param str to_path: Path to output file(s).
        :param str from_format: Input format: `nmrstar` or `json`.
        :param str to_format: Output format: `nmrstar` or `json`.
        :return: None
        :rtype: None
        """
        self.from_path = os.path.normpath(from_path)
        self.to_path = os.path.normpath(to_path)
        self.from_format = from_format
        self.to_format = to_format

        self.from_path_compression = nmrstarlib.GenericFilePath.is_compressed(from_path)
        self.to_path_compression = nmrstarlib.GenericFilePath.is_compressed(to_path)

    def convert(self):
        """Convert file(s) from NMR-STAR format to JSON format or from JSON format to NMR-STAR format.

        :return: None
        :rtype: None
        """
        if not os.path.exists(os.path.dirname(self.to_path)):
            dirname = os.path.dirname(self.to_path)
            if dirname:
                os.makedirs(dirname)

        if os.path.isdir(self.from_path):
            self._many_to_many()
        elif os.path.isfile(self.from_path) or nmrstarlib.GenericFilePath.is_url(self.from_path):
            if self.from_path_compression in ("zip", "tar", "tar.gz", "tar.bz2"):
                self._many_to_many()
            elif self.from_path_compression in ("gz", "bz2"):
                self._one_to_one()
            elif not self.from_path_compression:
                self._one_to_one()
        elif self.from_path.isdigit():
            self._one_to_one()
        else:
            raise TypeError('Unknown input file format: "{}"'.format(self.from_path))

    def _many_to_many(self):
        """Perform many-to-many files conversion.

        :return: None
        :rtype: None
        """
        if not self.to_path_compression:
            self._to_dir()
        elif self.to_path_compression == "zip":
            self._to_zipfile()
        elif self.to_path_compression in ("tar", "tar.gz", "tar.bz2"):
            self._to_tarfile()
        elif self.to_path_compression in ("gz", "bz2"):
            raise TypeError('Many-to-one conversion, cannot convert "{}" into "{}"'.format(self.from_path,
                                                                                           self.to_path))
        else:
            raise TypeError('Unknown output file format: "{}"'.format(self.to_path))

    def _one_to_one(self):
        """Perform one-to-one file conversion.

        :return: None
        :rtype: None
        """
        if not self.to_path_compression:
            self._to_textfile()
        elif self.to_path_compression == "gz":
            self._to_gzipfile()
        elif self.to_path_compression == "bz2":
            self._to_bz2file()
        elif self.to_path_compression in ("tar", "tar.gz", "tar.bz2", "zip"):
            raise TypeError('One-to-many conversion, cannot convert "{}" into "{}"'.format(self.from_path,
                                                                                           self.to_path))
        else:
            raise TypeError('Unknown format: "{}"'.format(self.to_path))

    def _to_dir(self):
        """Convert files to directory.

        :return: None
        :rtype: None
        """
        for starfile in nmrstarlib.read_files([self.from_path]):
            outpath = self._outputpath(starfile.source)

            if not os.path.exists(os.path.dirname(outpath)):
                os.makedirs(os.path.dirname(outpath))

            with open(outpath, mode="w") as outfile:
                starfile.write(outfile, self.to_format)

    def _to_zipfile(self):
        """Convert files to zip archive.

        :return: None
        :rtype: None
        """
        with zipfile.ZipFile(self.to_path, mode="w", compression=zipfile.ZIP_DEFLATED) as outfile:
            for starfile in nmrstarlib.read_files([self.from_path]):
                outpath = self._outputpath(starfile.source, archive=True)
                outfile.writestr(outpath, starfile.writestr(self.to_format))

    def _to_tarfile(self):
        """Convert files to tar archive.

        :return: None
        :rtype: None
        """
        if self.to_path_compression == "tar":
            tar_mode = "w"
        elif self.to_path_compression == "tar.gz":
            tar_mode = "w:gz"
        elif self.to_path_compression == 'tar.bz2':
            tar_mode = "w:bz2"
        else:
            tar_mode = "w"

        with tarfile.open(self.to_path, mode=tar_mode) as outfile:
            for starfile in nmrstarlib.read_files([self.from_path]):
                outpath = self._outputpath(starfile.source, archive=True)
                info = tarfile.TarInfo(outpath)
                data = starfile.writestr(self.to_format).encode()
                info.size = len(data)
                outfile.addfile(tarinfo=info, fileobj=io.BytesIO(data))

    def _to_bz2file(self):
        """Convert file to bz2-compressed file.

        :return: None
        :rtype: None
        """
        with bz2.BZ2File(self.to_path, mode="wb") as outfile:
            for starfile in nmrstarlib.read_files([self.from_path]):
                outfile.write(starfile.writestr(self.to_format).encode())

    def _to_gzipfile(self):
        """Convert file to gzip-compressed file.

        :return: None
        :rtype: None
        """
        with gzip.GzipFile(self.to_path, mode="wb") as outfile:
            for starfile in nmrstarlib.read_files([self.from_path]):
                outfile.write(starfile.writestr(self.to_format).encode())

    def _to_textfile(self):
        """Convert file to regular text file.

        :return: None
        :rtype: None
        """
        to_path = self.to_path if self.to_path.endswith(self.nmrstar_extension[self.to_format]) \
            else self.to_path + self.nmrstar_extension[self.to_format]
        with open(to_path, mode="w") as outfile:
            for starfile in nmrstarlib.read_files([self.from_path]):
                outfile.write(starfile.writestr(self.to_format))

    def _outputpath(self, inputpath, archive=False):
        """Construct an output path string from an input path string.

        :param str inputpath: Input path string.
        :return: Output path string.
        :rtype: str
        """
        indirpath, fname = os.path.split(os.path.abspath(os.path.normpath(inputpath)))

        commonprefix = os.path.commonprefix([os.path.abspath(self.from_path),
                                             os.path.abspath(indirpath)])

        commonparts = commonprefix.split(os.sep)
        inparts = indirpath.split(os.sep)
        outparts = inparts[len(commonparts):]

        if archive:
            outdirpath = os.path.join(*outparts)
        else:
            outdirpath = os.path.join(self.to_path, *outparts)

        return os.path.join(outdirpath, fname + self.nmrstar_extension[self.to_format])
