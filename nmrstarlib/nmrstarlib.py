#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
nmrstarlib.nmrstarlib
~~~~~~~~~~~~~~~~~~~~~

This module provides the :class:`~nmrstarlib.nmrstarlib.StarFile` class
that stores the data from a single NMR-STAR file in the form of an
:py:class:`~collections.OrderedDict`. Data can be accessed directly from the
:class:`~nmrstarlib.nmrstarlib.StarFile` instance using bracket
accessors.

The NMR-STAR format is a hierachical dictionary containing data on
NMR experiments. The data is divided into a series of "saveframes"
which each contain a number of key-value pairs and "loops".

Each saveframe has a unique name, which is used as the key in
the dictionary, corresponding to another dictionary containing the
information in the saveframe.  Since loops in NMR-Star format do
not have names, the keys for them inside the saveframe dictionary
are simply loop_0, loop_1, etc.
"""

from __future__ import print_function, division

import sys
import os
import io
import zipfile
import bz2
import gzip
import tarfile
from collections import OrderedDict

if sys.version_info.major == 3 and sys.version_info.minor == 6:
    try:
        import ujson as json
        UJSON = True
    except ImportError:
        UJSON = False
        import json
else:
    import json

if sys.version_info.major == 3:
    from urllib.request import urlopen
    from urllib.parse import urlparse
else:
    from urllib2 import urlopen
    from urlparse import urlparse

try:
    from .cbmrblex import bmrblex
except ImportError:
    from .bmrblex import bmrblex


BMRB_REST = "http://rest.bmrb.wisc.edu/bmrb/NMR-STAR3/"
VERBOSE = False
NMRSTAR_VERSION = "3"
NMRSTAR_CONSTANTS = {}


class StarFile(OrderedDict):
    """StarFile class that stores the data from a single NMR-STAR file in the form of an
    :py:class:`~collections.OrderedDict`."""

    def __init__(self, source="", frame_categories=None, *args, **kwds):
        """`StarFile` initializer. Leave `frame_categories` as :py:obj:`None` to
        read everything. Otherwise it can be a list of saveframe categories to read, skipping the rest.

        :param str source: Source `StarFile` instance was created from - local file or URL address.
        :param list frame_categories: List of saveframe names.
        """
        super(StarFile, self).__init__(*args, **kwds)
        self.source = source
        self._frame_categories = frame_categories
        self.bmrbid = ""

    def read(self, filehandle):
        """Read data into a :class:`~nmrstarlib.nmrstarlib.StarFile` instance.

        :param filehandle: file-like object.
        :type filehandle: :py:class:`io.TextIOWrapper`, :py:class:`gzip.GzipFile`,
                          :py:class:`bz2.BZ2File`, :py:class:`zipfile.ZipFile`
        :return: None
        :rtype: :py:obj:`None`
        """
        inputstr = filehandle.read()
        nmrstar_str = self._is_nmrstar(inputstr)
        json_str = self._is_json(inputstr)

        if not inputstr:
            pass
        elif nmrstar_str:
            self._build_starfile(nmrstar_str)
        elif json_str:
            self.update(json_str)
            self.bmrbid = self[u"data"]
        else:
            raise TypeError("Unknown file format")
        filehandle.close()

    def write(self, filehandle, fileformat):
        """Write :class:`~nmrstarlib.nmrstarlib.StarFile` data into file.

        :param filehandle: file-like object.
        :type filehandle: :py:class:`io.TextIOWrapper`
        :param str fileformat: Format to use to write data: `nmrstar` or `json`.
        :return: None
        :rtype: :py:obj:`None`
        """
        try:
            if fileformat == "json":
                json_str = self._to_json()
                filehandle.write(json_str)
            elif fileformat == "nmrstar":
                nmrstar_str = self._to_nmrstar()
                filehandle.write(nmrstar_str)
            else:
                raise TypeError("Unknown file format.")
        except IOError:
            raise IOError('"filehandle" parameter must be writable.')
        filehandle.close()

    def writestr(self, fileformat):
        """Write :class:`~nmrstarlib.nmrstarlib.StarFile` data into string.

        :param str fileformat: Format to use to write data: `nmrstar` or `json`.
        :return: String representing the :class:`~nmrstarlib.nmrstarlib.StarFile` instance.
        :rtype: :py:class:`str`
        """
        try:
            if fileformat == "json":
                json_str = self._to_json()
                return json_str
            elif fileformat == "nmrstar":
                nmrstar_str = self._to_nmrstar()
                return nmrstar_str
            else:
                raise TypeError("Unknown file format.")
        except IOError:
            raise IOError('"filehandle" parameter must be writable.')

    def _build_starfile(self, nmrstar_str):
        """Build :class:`~nmrstarlib.nmrstarlib.StarFile` object.

        :param nmrstar_str: NMR-STAR-formatted string.
        :type nmrstar_str: :py:class:`str` or :py:class:`bytes`
        :return: instance of :class:`~nmrstarlib.nmrstarlib.StarFile`.
        :rtype: :class:`~nmrstarlib.nmrstarlib.StarFile`
        """
        odict = self
        lexer = bmrblex(nmrstar_str)
        token = next(lexer)

        while token != u"":
            try:
                if token[0:5] == u"save_":
                    name = token
                    frame = self._build_saveframe(lexer)
                    if frame:
                        odict[name] = frame
                    
                elif token[0:5] == u"data_":
                    self.bmrbid = token[5:]
                    self[u"data"] = self.bmrbid
                else:
                    print("Error: Invalid token {}".format(token), file=sys.stderr)
                    print("In _build_starfile try block", file=sys.stderr)
                    raise InvalidToken("{}".format(token))

            except IndexError:
                print("Error: Invalid token {}".format(token), file=sys.stderr)
                print("In _build_starfile except block", file=sys.stderr)
                raise
            finally:
                token = next(lexer)
        return self

    def _build_saveframe(self, lexer):
        """Build NMR-STAR file saveframe.

        :param lexer: instance of the BMRB lexical analyzer.
        :type lexer: :func:`~nmrstarlib.bmrblex.bmrblex`
        :return: Saveframe dictionary.
        :rtype: :py:class:`collections.OrderedDict`
        """
        odict = OrderedDict()
        loopcount = 0

        token = next(lexer)
        while token != u"save_":
            try:
                if token[0] == u"_":
                    # This strips off the leading underscore of tagnames for readability 
                    odict[token[1:]] = next(lexer)

                    # Skip the saveframe if it's not in the list of wanted categories
                    if self._frame_categories:
                        if token == "_Saveframe_category" and odict[token[1:]] not in self._frame_categories:
                            raise SkipSaveFrame()

                elif token == u"loop_":
                    odict[u"loop_{}".format(loopcount)] = self._build_loop(lexer)
                    loopcount += 1

                else:
                    print("Error: Invalid token {}".format(token), file=sys.stderr)
                    print("In _build_saveframe try block", file=sys.stderr)
                    raise InvalidToken("{}".format(token))

            except IndexError:
                print("Error: Invalid token {}".format(token), file=sys.stderr)
                print("In _build_saveframe except block", file=sys.stderr)
                raise
            except SkipSaveFrame:
                self._skip_saveframe(lexer)
                odict = None
            finally:
                if odict is None:
                    token = u"save_"
                else:
                    token = next(lexer)
        return odict

    def _build_loop(self, lexer):
        """Build saveframe loop.

        :param lexer: instance of BMRB lexical analyzer.
        :type lexer: :func:`~nmrstarlib.bmrblex.bmrblex`
        :return: Fields and values of the loop.
        :rtype: :py:class:`tuple`
        """
        fields = []
        values = []

        token = next(lexer)
        while token[0] == u"_":
            fields.append(token[1:])
            token = next(lexer)

        while token != u"stop_":
            values.append(token)
            token = next(lexer)

        assert float(len(values)/len(fields)).is_integer(), \
            "Error in loop construction: number of fields must be equal to number of values."

        # divide list of loop values into chunks corresponding to fields
        # values = [values[i:i+len(fields)] for i in range(0, len(values), len(fields))]
        # return fields, values

        values = [OrderedDict(zip(fields, values[i:i + len(fields)])) for i in range(0, len(values), len(fields))]
        return fields, values

    def print_starfile(self, f=sys.stdout, format="nmrstar", tw=3):
        """Print :class:`~nmrstarlib.nmrstarlib.StarFile` into a file or stdout.

        :param io.StringIO f: writable file-like stream.
        :param str format: Format to use: `nmrstar` or `json`.
        :param int tw: Tab width.
        :return: None
        :rtype: :py:obj:`None`
        """
        if format is "nmrstar":
            for saveframe in self.keys():
                if saveframe == "data":
                    print("{}_{}\n".format(saveframe, self[saveframe]), file=f)
                else:
                    print("{}".format(saveframe), file=f)
                    self.print_saveframe(saveframe, f, format, tw)
                    print("save_\n", file=f)

        elif format is "json":
            print(self._to_json(), file=f)

    def print_saveframe(self, sf, f=sys.stdout, format="nmrstar", tw=3):
        """Print saveframe into a file or stdout.
        We need to keep track of how far over everything is tabbed. The "tab width"
        variable tw does this for us.

        :param str sf: Saveframe name.
        :param io.StringIO f: writable file-like stream.
        :param str format: Format to use: `nmrstar` or `json`.
        :param int tw: Tab width.
        :return: None
        :rtype: :py:obj:`None`
        """
        if format is "nmrstar":
            if sf == "data":
                print("{}_{}\n".format(sf, self[sf]), file=f)
            else:
                for sftag in self[sf].keys():
                    # handle the NMR-Star "multiline string"
                    if self[sf][sftag][0] == ";":
                        print(tw*" ", "_{}".format(sftag), file=f)
                        print("{}".format(self[sf][sftag]), file=f)

                    # handle loops
                    elif sftag[:5] == "loop_":
                        print(tw*" ", "loop_", file=f)
                        self.print_loop(sf, sftag, f, format, tw * 2)
                        print(tw*" ", "stop_", file=f)
                    else:
                        print(tw*" ", "_{}\t {}".format(sftag, self[sf][sftag]), file=f)

        elif format is "json":
            print(json.dumps(self[sf], sort_keys=False, indent=4), file=f)

    def print_loop(self, sf, sftag, f=sys.stdout, format="nmrstar", tw=3):
        """Print loop into a file or stdout.

        :param str sf: Saveframe name.
        :param str sftag: Saveframe tag, i.e. field name.
        :param io.StringIO f: writable file-like stream.
        :param str format: Format to use: `nmrstar` or `json`.
        :param int tw: Tab width.
        :return: None
        :rtype: :py:obj:`None`
        """
        if format is "nmrstar":
            # First print the fields
            for field in self[sf][sftag][0]:
                print(tw*" ", "_{}".format(field), file=f)

            # Then print the values
            for valuesdict in self[sf][sftag][1]:
                line = tw*" " + " ".join(valuesdict.values())
                print(line, file=f)

        elif format is "json":
            print(json.dumps(self[sf][sftag], sort_keys=False, indent=4), file=f)

    def _to_json(self):
        """Save :class:`~nmrstarlib.nmrstarlib.StarFile` into JSON string.

        :return: JSON string.
        :rtype: :py:class:`str`
        """
        return json.dumps(self, sort_keys=False, indent=4)

    def _to_nmrstar(self):
        """Save :class:`~nmrstarlib.nmrstarlib.StarFile` NMR-STAR format string.

        :return: NMR-STAR string.
        :rtype: :py:class:`str`
        """
        nmrstar_str = io.StringIO()
        self.print_starfile(nmrstar_str)
        return nmrstar_str.getvalue()

    def _skip_saveframe(self, lexer):
        """Skip entire saveframe - keep emitting tokens until the end of saveframe.

        :param lexer: instance of the BMRB lexical analyzer class.
        :type lexer: :class:`~nmrstarlib.bmrblex.bmrblex`
        :return: None
        :rtype: :py:obj:`None`
        """
        token = u""
        while token != u"save_":
            token = next(lexer)

    @staticmethod
    def _is_nmrstar(string):
        """Test if input string is in NMR-STAR format.

        :param string: Input string.
        :type string: :py:class:`str` or :py:class:`bytes`
        :return: Input string if in NMR-STAR format or False otherwise.
        :rtype: :py:class:`str` or :py:obj:`False`
        """
        if string[0:5] == "data_" or string[0:5] == b"data_":
            return string
        return False

    @staticmethod
    def _is_json(string):
        """Test if input string is in JSON format.

        :param string: Input string.
        :type string: :py:class:`str` or :py:class:`bytes`
        :return: Input string if in JSON format or False otherwise.
        :rtype: :py:class:`str` or :py:obj:`False`
        """
        try:
            if isinstance(string, bytes):
                # json_str = json.loads(string.decode("utf-8"), object_pairs_hook=OrderedDict)
                json_str = json.loads(string.decode("utf-8"))
            elif isinstance(string, str):
                # json_str = json.loads(string, object_pairs_hook=OrderedDict)
                json_str = json.loads(string)
            else:
                raise TypeError("Expecting <class 'str'> or <class 'bytes'>, but {} was passed".format(type(string)))
            return json_str
        except ValueError:
            return False

    def chem_shifts_by_residue(self, aminoacids=None, atoms=None, nmrstarversion="3"):
        """Organize chemical shifts by amino acid residue.

        :param list aminoacids: List of aminoacids three-letter codes.
        :param list atoms: List of BMRB atom type codes.
        :param str nmrstarversion: Version of NMR-STAR format to use for look up chemichal shifts loop.
        :return: List of OrderedDict per each chain
        :rtype: :py:class:`list` of :py:class:`collections.OrderedDict`
        """
        this_directory = os.path.dirname(__file__)
        if nmrstarversion == "2":
            config_filepath = os.path.join(this_directory, 'conf/constants_nmrstar2.json')
        elif nmrstarversion == "3":
            config_filepath = os.path.join(this_directory, 'conf/constants_nmrstar3.json')
        else:
            config_filepath = os.path.join(this_directory, 'conf/constants_nmrstar3.json')
        with open(config_filepath, "r") as infile:
            update_constants(infile)

        chemshifts_loop = NMRSTAR_CONSTANTS["chemshifts_loop"]
        aminoacid_seq_id = NMRSTAR_CONSTANTS["aminoacid_seq_id"]
        aminoacid_code = NMRSTAR_CONSTANTS["aminoacid_code"]
        atom_code = NMRSTAR_CONSTANTS["atom_code"]
        chemshift_value = NMRSTAR_CONSTANTS["chemshift_value"]

        chains = []
        for saveframe in self:
            if saveframe == "data":
                continue
            else:
                for ind in self[saveframe].keys():
                    if ind.startswith("loop_"):
                        if list(self[saveframe][ind][0]) == chemshifts_loop:
                            chemshifts_dict = OrderedDict()
                            for entry in self[saveframe][ind][1]:
                                residueid = int(entry[aminoacid_seq_id])
                                chemshifts_dict.setdefault(residueid, OrderedDict())
                                chemshifts_dict[residueid]["AACode_3"] = entry[aminoacid_code]
                                chemshifts_dict[residueid]["Seq_ID"] = residueid
                                chemshifts_dict[residueid][entry[atom_code]] = entry[chemshift_value]
                            chains.append(chemshifts_dict)

        if aminoacids:
            for chemshifts_dict in chains:
                for aa in list(chemshifts_dict.keys()):
                    if aa[1].upper() not in aminoacids:
                        chemshifts_dict.pop(aa)

        if atoms:
            for chemshifts_dict in chains:
                for resonances_dict in chemshifts_dict.values():
                    for at in list(resonances_dict.keys()):
                        if at.upper() not in atoms:
                            resonances_dict.pop(at)
        return chains


def update_constants(filehandle):
    """Update constants related to NMR-STAR format, e.g. field names.

    :param str filehandle: JSON file that contains information about NMR-STAR format.
    :return: None
    :rtype: :py:obj:`None`
    """
    newconstants = json.loads(filehandle.read())
    NMRSTAR_CONSTANTS.update(newconstants)


def _generate_filenames(sources):
    """Generate filenames.

    :param list sources: List of strings representing path to file(s).
    :return: Path to file(s).
    :rtype: :py:class:`str`
    """
    for source in sources:
        if os.path.isdir(source):
            for path, dirlist, filelist in os.walk(source):
                for fname in filelist:
                    if GenericFilePath.is_compressed(fname):
                        if VERBOSE:
                            print("Skipping compressed file: {}".format(os.path.abspath(fname)))
                        continue
                    else:
                        yield os.path.join(path, fname)
        elif os.path.isfile(source):
            yield source
        elif source.isdigit():
            yield BMRB_REST + source
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
        if VERBOSE:
            print("Processing file: {}".format(os.path.abspath(fname)))
        path = GenericFilePath(fname)
        for filehandle, source in path.open():
            yield filehandle, source
            filehandle.close()


def read_files(*sources):
    """Construct a generator that yields :class:`~nmrstarlib.nmrstarlib.StarFile` instances.

    :param list sources: List of strings representing path to file(s).
    :return: :class:`~nmrstarlib.nmrstarlib.StarFile` instance(s).
    :rtype: :class:`~nmrstarlib.nmrstarlib.StarFile`
    """
    filenames = _generate_filenames(sources)
    filehandles = _generate_handles(filenames)
    for fh, source in filehandles:
        starfile = StarFile(source)
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
                filehandle = bz2.open(io.BytesIO(path)) if is_url else bz2.open(path)
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


class InvalidToken(Exception):
    def __init__(self, value):
        self.parameter = value

    def __str__(self):
        return repr(self.parameter)


class SkipSaveFrame(Exception):
    def __init__(self):
        pass

    def __str__(self):
        return "Skipping save frame"