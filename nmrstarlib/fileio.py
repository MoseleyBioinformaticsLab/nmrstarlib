#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
nmrstarlib.fileio
~~~~~~~~~~~~~~~~~

This module provides routines for reading ``NMR-STAR`` formatted files
from difference kinds of sources:
   * Single ``NMR-STAR`` formatted file on a local machine.
   * Directory containing multiple ``NMR-STAR`` formatted files.
   * Compressed zip/tar archive of ``NMR-STAR`` formatted files.
   * URL address of ``NMR-STAR`` formatted file.
   * ``BMRB ID`` of ``NMR-STAR`` formatted file. 
"""

import os
import io
import sys
import zipfile
import tarfile
import bz2
import gzip

from . import nmrstarlib

if sys.version_info.major == 3:
    from urllib.request import urlopen
    from urllib.parse import urlparse
else:
    from urllib2 import urlopen
    from urlparse import urlparse


def _generate_filenames(sources):
    """Generate filenames.

    :param tuple sources: Sequence of strings representing path to file(s).
    :return: Path to file(s).
    :rtype: :py:class:`str`
    """
    for source in sources:
        if os.path.isdir(source):
            for path, dirlist, filelist in os.walk(source):
                for fname in filelist:
                    print("Processing...", fname)
                    if GenericFilePath.is_compressed(fname):
                        if nmrstarlib.VERBOSE:
                            print("Skipping compressed file: {}".format(os.path.abspath(fname)))
                        continue
                    else:
                        yield os.path.join(path, fname)
        elif os.path.isfile(source):
            yield source
        elif source.isdigit():
            yield nmrstarlib.BMRB_REST + source
        elif GenericFilePath.is_url(source):
            yield source
        else:
            raise TypeError("Unknown file source.")


def _generate_handles(filenames):
    """Open a sequence of filenames one at time producing file objects.
    The file is closed immediately when proceeding to the next iteration.

    :param generator filenames: Generator object that yields the path to each file, one at a time.
    :return: Filehandle to be processed into a :class:`~nmrstarlib.nmrstarlib.StarFile` instance.
    """
    for fname in filenames:
        if nmrstarlib.VERBOSE:
            print("Processing file: {}".format(os.path.abspath(fname)))
        path = GenericFilePath(fname)
        for filehandle, source in path.open():
            yield filehandle, source
            filehandle.close()


def read_files(*sources):
    """Construct a generator that yields :class:`~nmrstarlib.nmrstarlib.StarFile` instances.

    :param sources: One or more strings representing path to file(s).
    :return: :class:`~nmrstarlib.nmrstarlib.StarFile` instance(s).
    :rtype: :class:`~nmrstarlib.nmrstarlib.StarFile`
    """
    filenames = _generate_filenames(sources)
    filehandles = _generate_handles(filenames)
    for fh, source in filehandles:
        starfile = nmrstarlib.StarFile(source)
        starfile.read(fh)
        yield starfile


class GenericFilePath(object):
    """`GenericFilePath` class knows how to open local files or files over URL."""

    def __init__(self, path):
        """Initialize path.

        :param str path: String representing a path to local file(s) or valid URL address of file(s).
        """
        self.path = path

    def open(self):
        """Generator that opens and yields filehandles using appropriate facilities:
        test if path represents a local file or file over URL, if file is compressed
        or not.

        :return: Filehandle to be processed into a :class:`~nmrstarlib.nmrstarlib.StarFile` instance.
        """
        is_url = self.is_url(self.path)
        compressiontype = self.is_compressed(self.path)

        if not compressiontype:
            if is_url:
                filehandle = urlopen(self.path)
            else:
                filehandle = open(self.path, "r")
            source = self.path
            yield filehandle, source
            filehandle.close()

        elif compressiontype:
            if is_url:
                response = urlopen(self.path)
                path = response.read()
                response.close()
            else:
                path = self.path

            if compressiontype == "zip":
                ziparchive = zipfile.ZipFile(io.BytesIO(path), "r") if is_url else zipfile.ZipFile(path)
                for name in ziparchive.infolist():
                    if not name.filename.endswith("/"):
                        filehandle = ziparchive.open(name)
                        source = self.path + "/" + name.filename
                        yield filehandle, source
                        filehandle.close()

            elif compressiontype in ("tar", "tar.bz2", "tar.gz"):
                tararchive = tarfile.open(fileobj=io.BytesIO(path)) if is_url else tarfile.open(path)
                for name in tararchive:
                    if name.isfile():
                        filehandle = tararchive.extractfile(name)
                        source = self.path + "/" + name.name
                        yield filehandle, source
                        filehandle.close()

            elif compressiontype == "bz2":
                filehandle = bz2.BZ2File(io.BytesIO(path)) if is_url else bz2.BZ2File(path)
                source = self.path
                yield filehandle, source
                filehandle.close()

            elif compressiontype == "gz":
                filehandle = gzip.open(io.BytesIO(path)) if is_url else gzip.open(path)
                source = self.path
                yield filehandle, source
                filehandle.close()

    @staticmethod
    def is_compressed(path):
        """Test if path represents compressed file(s).

        :param str path: Path to file(s).
        :return: String specifying compression type if compressed, "" otherwise.
        :rtype: :py:class:`str`
        """
        if path.endswith(".zip"):
            return "zip"
        elif path.endswith(".tar.gz"):
            return "tar.gz"
        elif path.endswith(".tar.bz2"):
            return "tar.bz2"
        elif path.endswith(".gz"):
            return "gz"
        elif path.endswith(".bz2"):
            return "bz2"
        elif path.endswith(".tar"):
            return "tar"
        return ""

    @staticmethod
    def is_url(path):
        """Test if path represents a valid URL.

        :param str path: Path to file.
        :return: True if path is valid url string, False otherwise.
        :rtype: :py:obj:`True` or :py:obj:`False`
        """
        try:
            parse_result = urlparse(path)
            return all((parse_result.scheme, parse_result.netloc, parse_result.path))
        except ValueError:
            return False
