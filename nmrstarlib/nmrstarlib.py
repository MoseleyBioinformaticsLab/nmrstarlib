#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
nmrstarlib.nmrstarlib
~~~~~~~~~~~~~~~~~~~~~

"""

import sys
import os
import zipfile
import bz2
import gzip
import tarfile
import json
import urllib.request
import urllib.error
from collections import OrderedDict

# from . import bmrblex
from . import bmrblex2


class StarFile(OrderedDict):
    """The StarFile class stores the data from a single NMR-STAR file in the
    form of an dict. Data can be accessed directly from the
    `StarFile` instance using bracket accessors.

    The NMR-STAR format is a hierachical dictionary containing data on
    NMR experiments.  The data is divided into a series of "saveframes"
    which each contain a number of key-value pairs and/or "loops" or
    lists of value records associated with a given set of keys.

    Each saveframe has a unique name, which is used here as the key in
    the dictionary, corresponding to another dictionary containing the
    information in the saveframe.  Since loops in NMR-Star format do
    not have names, the keys for them inside the saveframe dictionary
    are simply loop_0, loop_1, etc.
    """
    def __init__(self, frame_categories=None):
        super().__init__(self)
        # Leave frame_categories as None to read everything.  Otherwise it can be
        # a list of saveframe categories to read, skipping the rest
        self._frame_categories = frame_categories

    def read(self, filehandle):
        """Read into :class:`~nmrstarlib.nmrstarlib.StarFile` object

        :param filehandle: file-like object
        :type filehandle: :py:class:`io.TextIOWrapper`, :py:class:`gzip.GzipFile`,
                          :py:class:`bz2.BZ2File`, :py:class:`zipfile.ZipFile`
        :return: instance of :class:`~nmrstarlib.nmrstarlib.StarFile`
        :rtype: :class:`~nmrstarlib.nmrstarlib.StarFile`
        """
        streamstr = filehandle.read()
        nmrstar_str = self._is_nmrstar(streamstr)
        json_str = self._is_json(streamstr)

        if streamstr == '' or streamstr == b'':
            pass
        elif nmrstar_str:
            lexer = bmrblex2.bmrblex(nmrstar_str)
            # lexer = bmrblex.bmrblex(filehandle.read()) # return that
            return self._build_file(lexer)
        elif json_str:
            return self.update(json_str)
        else:
            raise TypeError("Unknown file format")

        filehandle.close()

    def write(self, filehandle, fileformat, compressiontype=None):
        """Write :class:`~nmrstarlib.nmrstarlib.StarFile` into file in BMRB format

        :param filehandle: file-like object
        :type filehandle: :py:class:`io.TextIOWrapper`
        :param str fileformat:
        :param str compressiontype:
        :return: None
        :rtype: None
        """
        try:
            if fileformat == 'json':
                self._to_json(filehandle)
            elif fileformat == 'nmrstar':
                self._to_nmrstar(filehandle)
            else:
                raise TypeError('Unknown file format.')
        except IOError:
            raise IOError('"filehandle" parameter must be writable.')

        if compressiontype:
            _compress(filepath=filehandle.name, compressiontype=compressiontype)

        filehandle.close()

    def _build_file(self, lexer):
        """Build `StarFile` dict object

        :param lexer: instance of BMRB lexical analyzer class
        :type lexer: nmrstarlib.bmrblex.bmrblex
        :return: instance of `StarFile` object
        :rtype: nmrstarlib.nmrstarlib.StarFile
        """
        odict = self
        token = lexer.get_token()

        while token != '':
            try:
                if token[0:5] == 'save_':
                    # name = token[5:]
                    name = token
                    frame = self._build_sf(lexer)
                    if frame:
                        odict[name] = frame
                    
                elif token[0:5] == 'data_':
                    self.bmrbid = token[5:]
                else:
                    print("{} Error: Invalid token {}".format(lexer.error_leader(), token), file=sys.stderr)
                    print("In _build_file try block", file=sys.stderr)  # DEBUG
                    raise InvalidToken("{} {}".format(lexer.error_leader(), token))
            except IndexError:
                print("{} Error: Invalid token {}".format(lexer.error_leader(), token), file=sys.stderr)
                print("In _build_file except block", file=sys.stderr)  # DEBUG
                raise
            finally:
                token = lexer.get_token()
        return self

    def _build_sf(self, lexer):
        """Build NMR-STAR file saveframe

        :param lexer: instance of BMRB lexical analyzer class
        :type lexer: nmrstarlib.bmrblex.bmrblex
        :return: Saveframe dict
        :rtype: dict
        """
        # odict = dict()
        odict = OrderedDict()
        loopcount = 0

        token = lexer.get_token()
        while token != 'save_':
            # print("TOKEN inside build_sf:", token)
            try:
                if token[0] == '_':
                    # This strips off the leading underscore of tagnames for readability 
                    odict[token[1:]] = lexer.get_token()

                    # Skip the saveframe if it's not in the list of wanted categories
                    if self._frame_categories:
                        if token == "_Saveframe_category" and odict[token[1:]] not in self._frame_categories:
                            raise SkipSaveFrame()

                elif token == 'loop_':
                    odict['loop_{}'.format(loopcount)] = self._build_loop(lexer)
                    loopcount += 1

                else:
                    print("{} Error: Invalid token {}".format(lexer.error_leader(), token), file=sys.stderr)
                    print("In _build_sf try block", file=sys.stderr)  # DEBUG
                    raise InvalidToken("{} {}".format(lexer.error_leader(), token))

            except IndexError:
                print("{} Error: Invalid token {}".format(lexer.error_leader(), token), file=sys.stderr)
                print("In _build_sf except block", file=sys.stderr)  # DEBUG
                raise
            except SkipSaveFrame:
                self._skip_sf(lexer)
                odict = None
            finally:
                if odict is None:
                    token = 'save_'
                else:
                    token = lexer.get_token()
                # print(token) #DEBUG

        return odict

    def _skip_sf(self, lexer):
        """Skip entire saveframe - keep emitting tokens until the end of saveframe

        :param lexer: instance of BMRB lexical analyzer class
        :type lexer: :class:`~nmrstarlib.bmrblex.bmrblex`
        :return: None
        :rtype: None
        """
        token = ''
        while  token != 'save_':
            token = lexer.get_token()
            # print(token) #DEBUG

    def _build_loop(self, lexer):
        """Build loop inside of saveframe

        :param lexer: instance of BMRB lexical analyzer class
        :type lexer: :class:`~nmrstarlib.bmrblex.bmrblex`
        :return: fields and values of the loop
        :rtype: tuple
        """
        fields = []
        values = []

        token = lexer.get_token()
        while token[0] == '_':
            fields.append(token[1:])
            token = lexer.get_token()

        while token != 'stop_':
            values.append(token)
            token = lexer.get_token()

        assert (len(values)/len(fields)).is_integer(), \
            "Error in loop construction: number of fields must be equal to number of values."

        # divide list of loop values into chunks corresponding to fields
        values = [values[i:i+len(fields)] for i in range(0, len(values), len(fields))]
        return (fields, values)

        # dvalues = [OrderedDict(zip(fields, values[i:i + len(fields)])) for i in range(0, len(values), len(fields))]
        # return dvalues

    def _print_nmrstar(self, filehandle=sys.stdout):
        """Print `StarFile` dict into file or stdout.

        :param filepath:
        :return:
        """
        print("data_{}\n".format(self.bmrbid), file=filehandle)

        for saveframe in self.keys():
            print("{}".format(saveframe), file=filehandle)
            self._print_saveframe(filehandle, saveframe, 3)

    def _print_saveframe(self, f, sf, tw):
        """Print saveframe.
        We need to keep track of how far over everything is tabbed.
        The "tab width" variable tw does this for us.
        """
        for ind in self[sf].keys():
            # handle the NMR-Star "long string" type
            if self[sf][ind][0] == ';':
                print(tw*' ',"_{}".format(ind), file=f)
                print('{}'.format(self[sf][ind]), file=f)

            # handle loops
            elif ind[:5] == "loop_":
                print(tw*' ',"loop_", file=f)
                self._print_loop(f,sf,ind,tw*2)
                print(tw*' ',"stop_", file=f)

            else:
                print(tw*' ',"_{}\t{}".format(ind,self[sf][ind]), file=f)

    def _print_loop(self, f, sf, ind, tw):
        """Print loop."""
        # First print the fields
        for field in self[sf][ind][0]:
            print(tw*' ', '_{}'.format(field), file=f)

        # Then print the values
        for values in self[sf][ind][1]:
            line = tw*' ' + ' '.join(values)
            print(line, file=f)

    def _to_json(self, filehandle):
        """Save :class:`nmrstarlib.nmrstarlib.StarFile` into JSON file

        :param filehandle:
        :return: None
        :rtype: None
        """
        json.dump(self, filehandle, sort_keys=False, indent=4)

    def _to_nmrstar(self, filehandle):
        """Save `StarFile` dict into BMRB NMR_STAR format

        :param filepath:
        :return:
        """
        self._print_nmrstar(filehandle)

    @staticmethod
    def _is_nmrstar(streamstr):
        """Test if streamstr in NMR-STAR format

        :param streamstr: stream string
        :type streamstr: str, bytes
        :return: str or False
        :rtype: str or False
        """
        if streamstr[0:5] == 'data_' or streamstr[0:5] == b'data_':
            return streamstr
        return False

    @staticmethod
    def _is_json(streamstr):
        """Test if streamstr in JSON format

        :param streamstr: stream string
        :type streamstr: str, bytes
        :return: JSON str or False
        :rtype: JSON str if successful, False otherwise
        """
        try:
            if isinstance(streamstr, bytes):
                json_str = json.loads(streamstr.decode('utf-8'))
            elif isinstance(streamstr, str):
                json_str = json.loads(streamstr)
            else:
                raise TypeError("Expecting <class 'str'> or <class 'bytes'>, but {} was passed".format(type(streamstr)))
            return json_str
        except ValueError:
            return False

class InvalidToken(Exception):
    def __init__(self,value):
        self.parameter = value

    def __str__(self):
        return repr(self.parameter)


class SkipSaveFrame(Exception):
    def __init__(self):
        pass
    def __str__(self):
        return 'Skipping save frame'


def from_file(filepath):
    """Read into :class:`~nmrstarlib.nmrstarlib.StaFile` from file.

    :param str filepath: path to file
    :return: :class:`~nmrstarlib.nmrstarlib.StarFile`
    :rtype: :class:`~nmrstarlib.nmrstarlib.StarFile`
    """
    starfile = StarFile()
    with open(filepath, 'r') as infile:
        is_compressed = _is_compressed(filepath)
        if is_compressed:
           filehandles = _decompress(filepath=filepath, compressiontype=is_compressed)
           if len(filehandles) == 1:
               starfile.read(filehandles[0])
           else:
               raise TypeError("Expecting single file, got list of {} files instead.".format(len(filehandles)))
        else:
            starfile.read(infile)
    return starfile


def from_archive(archivepath):
    """Read into :class:`~nmrstarlib.nmrstarlib.StaFile` from archive.

    :param str archivepath: path to archive
    :return: list of :class:`~nmrstarlib.nmrstarlib.StarFile` objects
    :rtype: list
    """
    starfiles = []
    is_compressed = _is_compressed(archivepath)
    if is_compressed:
        filehandles = _decompress(filepath=archivepath, compressiontype=is_compressed)
        for fh in filehandles:
            starfile = StarFile()
            starfile.read(fh)
            if starfile:
                starfiles.append(starfile)
    else:
        # need to through error here
        print(archivepath, "is not archive file")
    return starfiles


def from_dir(dirpath):
    """Read into :class:`~nmrstarlib.nmrstarlib.StaFile` from directory of files.

    :param str dirpath: path to directory of files
    :return: list of :class:`~nmrstarlib.nmrstarlib.StarFile` objects
    :rtype: list
    """
    starfiles = []
    if os.path.isdir(dirpath):
        for root, dirs, files in os.walk(dirpath):
            for fpath in files:
                if _is_archive(fpath):
                    starfiles.extend(from_archive(fpath))
                else:
                    starfiles.append(from_file(os.path.abspath(fpath)))
    else:
        # need to through error here
        print(dirpath, "is not a directory")
    return starfiles


def from_url(url):
    """Construct :class:`~nmrstarlib.nmrstarlib.StaFile` from URL address of BMRB NMR-STAR file

    :param str url: URL address of BMRB NMR-STAR file
    :return: :class:`~nmrstarlib.nmrstarlib.StarFile`
    :rtype: :class:`~nmrstarlib.nmrstarlib.StarFile`
    """
    try:
        response = urllib.request.urlopen(url)
        starfile = StarFile()
        starfile.read(response)
        return starfile
    except urllib.error.HTTPError:
        raise urllib.error.HTTPError("Invalid URL, check that URL is correct")


def from_bmrbid(bmrbid, base_url="http://rest.bmrb.wisc.edu/bmrb/NMR-STAR3/"):
    """Construct :class:`~nmrstarlib.nmrstarlib.StaFile` using BMRB NMR-STAR file id

    :param str bmrbid: BMRB id of NMR-STAR file, must be integer
    :param str base_url: URL address where BMRB stores NMR-STAR files
    :return: :class:`~nmrstarlib.nmrstarlib.StarFile`
    :rtype: :class:`~nmrstarlib.nmrstarlib.StarFile`
    """
    try:
        bmrbid = int(bmrbid)
        file_url = base_url + str(bmrbid)
        starfile = from_url(file_url)
        return starfile
    except ValueError:
        raise ValueError("Couldn't parse BMRB id, BMRB id must be integer")


def _is_compressed(filepath):
    """Check if file is compressed by reading beginning of file and checking
    against known file signatures.

    :param str filepath: path to file
    :return: compression type str or empty str if file is not compressed
    :rtype: str
    """
    file_signature = {b'\x1f\x8b\x08':     'gz',
                      b'\x42\x5a\x68':     'bz2',
                      b'\x50\x4b\x03\x04': 'zip'}

    max_len = max(len(x) for x in file_signature)
    with open(filepath, 'rb') as infile:
        file_start = infile.read(max_len)

    for signature, filetype in file_signature.items():
        if file_start.startswith(signature):
            return filetype
    return ''


def _decompress(filepath, compressiontype):
    """Decompress compressed filer or archive into file-like object

    :param str filepath: path to file
    :param str compressiontype: compression type (gz, bz2, zip)
    :return: list of filehandles
    :rtype: list of file-like objects (:py:class:`gzip.GzipFile`, :py:class:`bz2.BZ2File`, :py:class:`zipfile.ZipFile`)
    """
    filehandles = []

    if compressiontype == 'zip':
        ziparchive = zipfile.ZipFile(filepath)
        for fname in ziparchive.infolist():
            filehandle = ziparchive.open(fname)
            filehandles.append(filehandle)
            # yield filehandle

    elif compressiontype == 'bz2' or compressiontype == 'gz':
        if tarfile.is_tarfile(filepath):
            tararchive = tarfile.open(filepath)
            for fname in tararchive:
                filehandle = tararchive.extractfile(fname)
                if filehandle:
                    filehandles.append(filehandle)
        elif compressiontype == 'bz2':
            filehandles.append(bz2.open(filepath))
        elif compressiontype == 'gz':
            filehandles.append(gzip.open(filepath))
    else:
        raise TypeError("Unknown compression type: {}".format(compressiontype))

    return filehandles

def _compress(filepath, compressiontype):
    """Compress file using specified compression type

    :param str filepath: path to uncompressed file
    :param str compressiontype: compression type
    :return: None
    :rtype: None
    """
    if compressiontype == 'bz2':
        with open(filepath, 'rb') as infile, bz2.open(filepath + '.bz2', 'wb') as outfile:
            outfile.writelines(infile)
    elif compressiontype == 'gz':
        with open(filepath, 'rb') as infile, gzip.open(filepath + '.gz', 'wb') as outfile:
            outfile.writelines(infile)
    elif compressiontype == 'zip':
        with zipfile.ZipFile(filepath + '.zip', 'w') as outfile:
            outfile.write(filepath)
    elif compressiontype == 'tar.bz2':
        with tarfile.open(filepath + '.tar.bz2', 'w:bz2') as outfile:
            outfile.add(filepath)
    elif compressiontype == 'tar.gz':
        with tarfile.open(filepath + '.tar.gz', 'w:gz') as outfile:
            outfile.add(filepath)
    else:
        raise TypeError("Unknown compression type: {}".format(compressiontype))
    # os.remove(filepath)


def _is_archive(filepath):
    if zipfile.is_zipfile(filepath):
        return True
    elif tarfile.is_tarfile(filepath):
        return True
    return False