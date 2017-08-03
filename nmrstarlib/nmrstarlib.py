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
from collections import OrderedDict

import sys
import os
import io
import zipfile
import bz2
import gzip
import tarfile
import pprint


UJSON = False

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
RESONANCE_CLASSES = {}
SPECTRUM_DESCRIPTIONS = {}


def update_constants(nmrstar2cfg="", nmrstar3cfg="", resonance_classes_cfg="", spectrum_descriptions_cfg=""):
    """Update constant variables.

    :return: None
    :rtype: :py:obj:`None`
    """
    nmrstar_constants = {}
    resonance_classes = {}
    spectrum_descriptions = {}

    this_directory = os.path.dirname(__file__)

    nmrstar2_config_filepath = os.path.join(this_directory, "conf/constants_nmrstar2.json")
    nmrstar3_config_filepath = os.path.join(this_directory, "conf/constants_nmrstar3.json")
    resonance_classes_config_filepath = os.path.join(this_directory, "conf/resonance_classes.json")
    spectrum_descriptions_config_filepath = os.path.join(this_directory, "conf/spectrum_descriptions.json")

    with open(nmrstar2_config_filepath, "r") as nmrstar2config, open(nmrstar3_config_filepath, "r") as nmrstar3config:
        nmrstar_constants["2"] = json.load(nmrstar2config)
        nmrstar_constants["3"] = json.load(nmrstar3config)

    with open(resonance_classes_config_filepath, "r") as config:
        resonance_classes.update(json.load(config))

    with open(spectrum_descriptions_config_filepath, "r") as config:
        spectrum_descriptions.update(json.load(config))

    if nmrstar2cfg:
        with open(nmrstar2cfg, "r") as nmrstar2config:
            nmrstar_constants["2"].update(json.load(nmrstar2config))

    if nmrstar3cfg:
        with open(nmrstar2cfg, "r") as nmrstar3config:
            nmrstar_constants["3"].update(json.load(nmrstar3config))

    if resonance_classes_cfg:
        with open(nmrstar2cfg, "r") as config:
            resonance_classes.update(json.load(config))

    if spectrum_descriptions_cfg:
        with open(spectrum_descriptions_cfg, "r") as config:
            spectrum_descriptions.update(json.load(config))

    NMRSTAR_CONSTANTS.update(nmrstar_constants)
    RESONANCE_CLASSES.update(resonance_classes)
    SPECTRUM_DESCRIPTIONS.update(spectrum_descriptions)

update_constants()


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

    def write(self, filehandle, file_format):
        """Write :class:`~nmrstarlib.nmrstarlib.StarFile` data into file.

        :param filehandle: file-like object.
        :type filehandle: :py:class:`io.TextIOWrapper`
        :param str file_format: Format to use to write data: `nmrstar` or `json`.
        :return: None
        :rtype: :py:obj:`None`
        """
        try:
            if file_format == "json":
                json_str = self._to_json()
                filehandle.write(json_str)
            elif file_format == "nmrstar":
                nmrstar_str = self._to_nmrstar()
                filehandle.write(nmrstar_str)
            else:
                raise TypeError("Unknown file format.")
        except IOError:
            raise IOError('"filehandle" parameter must be writable.')
        filehandle.close()

    def writestr(self, file_format):
        """Write :class:`~nmrstarlib.nmrstarlib.StarFile` data into string.

        :param str file_format: Format to use to write data: `nmrstar` or `json`.
        :return: String representing the :class:`~nmrstarlib.nmrstarlib.StarFile` instance.
        :rtype: :py:class:`str`
        """
        try:
            if file_format == "json":
                json_str = self._to_json()
                return json_str
            elif file_format == "nmrstar":
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
        comment_count = 0
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

                elif token.lstrip().startswith(u"#"):
                    odict[u"comment_{}".format(comment_count)] = token
                    comment_count += 1

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
        loop_count = 0
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
                    odict[u"loop_{}".format(loop_count)] = self._build_loop(lexer)
                    loop_count += 1

                elif token.lstrip().startswith(u"#"):
                    continue

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

        values = [OrderedDict(zip(fields, values[i:i + len(fields)])) for i in range(0, len(values), len(fields))]
        return fields, values

    def print_starfile(self, f=sys.stdout, file_format="nmrstar", tw=3):
        """Print :class:`~nmrstarlib.nmrstarlib.StarFile` into a file or stdout.

        :param io.StringIO f: writable file-like stream.
        :param str file_format: Format to use: `nmrstar` or `json`.
        :param int tw: Tab width.
        :return: None
        :rtype: :py:obj:`None`
        """
        if file_format is "nmrstar":
            for saveframe in self.keys():
                if saveframe == u"data":
                    print(u"{}_{}\n".format(saveframe, self[saveframe]), file=f)
                elif saveframe.startswith(u"comment"):
                    print(u"{}".format(self[saveframe]), file=f)
                else:
                    print(u"{}".format(saveframe), file=f)
                    self.print_saveframe(saveframe, f, file_format, tw)
                    print(u"\nsave_\n\n", file=f)

        elif file_format is "json":
            print(self._to_json(), file=f)

    def print_saveframe(self, sf, f=sys.stdout, file_format="nmrstar", tw=3):
        """Print saveframe into a file or stdout.
        We need to keep track of how far over everything is tabbed. The "tab width"
        variable tw does this for us.

        :param str sf: Saveframe name.
        :param io.StringIO f: writable file-like stream.
        :param str file_format: Format to use: `nmrstar` or `json`.
        :param int tw: Tab width.
        :return: None
        :rtype: :py:obj:`None`
        """
        if file_format is "nmrstar":
            if sf == u"data":
                print(u"{}_{}\n".format(sf, self[sf]), file=f)
            else:
                for sftag in self[sf].keys():
                    # handle loops
                    if sftag[:5] == "loop_":
                        print(u"\n{}loop_".format(tw * u" "), file=f)
                        self.print_loop(sf, sftag, f, file_format, tw * 2)
                        print(u"\n{}stop_".format(tw * u" "), file=f)

                    # handle the NMR-Star "multiline string"
                    # if self[sf][sftag][0] == u";":
                    elif self[sf][sftag].endswith(u"\n"):
                        print(u"{}_{}".format(tw * u" ", sftag), file=f)
                        print(u";\n{};\n".format(self[sf][sftag]), file=f)

                    elif len(self[sf][sftag].split()) > 1:
                        print(u"{}_{}\t {}".format(tw * u" ", sftag, repr(self[sf][sftag])), file=f)

                    else:
                        print(u"{}_{}\t {}".format(tw * u" ", sftag, self[sf][sftag]), file=f)

        elif file_format is "json":
            print(json.dumps(self[sf], sort_keys=False, indent=4), file=f)

    def print_loop(self, sf, sftag, f=sys.stdout, file_format="nmrstar", tw=3):
        """Print loop into a file or stdout.

        :param str sf: Saveframe name.
        :param str sftag: Saveframe tag, i.e. field name.
        :param io.StringIO f: writable file-like stream.
        :param str file_format: Format to use: `nmrstar` or `json`.
        :param int tw: Tab width.
        :return: None
        :rtype: :py:obj:`None`
        """
        if file_format is "nmrstar":
            # First print the fields
            for field in self[sf][sftag][0]:
                print(u"{}_{}".format(tw * u" ", field), file=f)

            print(u"", file=f)  # new line between fields and values

            # Then print the values
            for valuesdict in self[sf][sftag][1]:
                # need to escape value with quotes (i.e. repr(value)) if value consists of two or more words
                print(u"{}{}".format(tw * u" ", u" ".join([repr(value) if len(value.split()) > 1 else value for value
                                                           in valuesdict.values()])), file=f)
        elif file_format is "json":
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
        if string[0:5] == u"data_" or string[0:5] == b"data_":
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
                if UJSON:
                    json_str = json.loads(string.decode("utf-8"))
                else:
                    json_str = json.loads(string.decode("utf-8"), object_pairs_hook=OrderedDict)
            elif isinstance(string, str):
                if UJSON:
                    json_str = json.loads(string)
                else:
                    json_str = json.loads(string, object_pairs_hook=OrderedDict)
            else:
                raise TypeError("Expecting <class 'str'> or <class 'bytes'>, but {} was passed".format(type(string)))
            return json_str
        except ValueError:
            return False

    def chem_shifts_by_residue(self, amino_acids=None, atoms=None, amino_acids_and_atoms=None, nmrstar_version="3"):
        """Organize chemical shifts by amino acid residue.

        :param list amino_acids: List of amino acids three-letter codes.
        :param list atoms: List of BMRB atom type codes.
        :param dict amino_acids_and_atoms: Amino acid and its atoms key-value pairs. 
        :param str nmrstar_version: Version of NMR-STAR format to use for look up chemical shifts loop.
        :return: List of OrderedDict per each chain
        :rtype: :py:class:`list` of :py:class:`collections.OrderedDict`
        """
        if (amino_acids_and_atoms and amino_acids) or (amino_acids_and_atoms and atoms):
            raise ValueError('"amino_acids_and_atoms" parameter cannot be used simultaneously with '
                             '"amino_acids" and "atoms" parameters, one or another must be provided.')

        chemshifts_loop = NMRSTAR_CONSTANTS[nmrstar_version]["chemshifts_loop"]
        aminoacid_seq_id = NMRSTAR_CONSTANTS[nmrstar_version]["aminoacid_seq_id"]
        aminoacid_code = NMRSTAR_CONSTANTS[nmrstar_version]["aminoacid_code"]
        atom_code = NMRSTAR_CONSTANTS[nmrstar_version]["atom_code"]
        chemshift_value = NMRSTAR_CONSTANTS[nmrstar_version]["chemshift_value"]

        chains = []
        for saveframe in self:
            if saveframe == u"data" or saveframe.startswith(u"comment"):
                continue
            else:
                for ind in self[saveframe].keys():
                    if ind.startswith(u"loop_"):
                        if list(self[saveframe][ind][0]) == chemshifts_loop:
                            chem_shifts_dict = OrderedDict()
                            for entry in self[saveframe][ind][1]:
                                residue_id = entry[aminoacid_seq_id]
                                chem_shifts_dict.setdefault(residue_id, OrderedDict())
                                chem_shifts_dict[residue_id][u"AA3Code"] = entry[aminoacid_code]
                                chem_shifts_dict[residue_id][u"Seq_ID"] = residue_id
                                chem_shifts_dict[residue_id][entry[atom_code]] = entry[chemshift_value]
                            chains.append(chem_shifts_dict)

        if amino_acids_and_atoms:
            for chem_shifts_dict in chains:
                for aa_dict in list(chem_shifts_dict.values()):
                    if aa_dict[u"AA3Code"].upper() not in list(amino_acids_and_atoms.keys()):
                        chem_shifts_dict.pop(aa_dict[u"Seq_ID"])
                    else:
                        for resonance in list(aa_dict.keys()):
                            if resonance in (u"AA3Code", u"Seq_ID") or resonance.upper() in amino_acids_and_atoms[aa_dict[u"AA3Code"]]:
                                continue
                            else:
                                aa_dict.pop(resonance)
        else:
            if amino_acids:
                for chem_shifts_dict in chains:
                    for aa_dict in list(chem_shifts_dict.values()):
                        if aa_dict[u"AA3Code"].upper() not in amino_acids:
                            chem_shifts_dict.pop(aa_dict[u"Seq_ID"])

            if atoms:
                for chem_shifts_dict in chains:
                    for aa_dict in chem_shifts_dict.values():
                        for resonance in list(aa_dict.keys()):
                            if resonance in (u"AA3Code", u"Seq_ID") or resonance.upper() in atoms:
                                continue
                            else:
                                aa_dict.pop(resonance)
        return chains


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

    :param sources: One or more strings representing path to file(s).
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


def list_spectrums():
    """List all available spectrum names that can be used for peak list simulation.

    :return: None
    :rtype: :py:obj:`None`
    """
    for spectrum_name in sorted(SPECTRUM_DESCRIPTIONS.keys()):
        print(spectrum_name)


def list_spectrum_descriptions(*args):
    """List all available spectrum descriptions that can be used for peak list simulation.

    :param str args: Spectrum name(s), e.g. list_spectrum_descriptions("HNCO", "HNcoCACB"), leave empty to list everything.
    :return: None
    :rtype: :py:obj:`None`
    """
    if args:
        for spectrum_name in args:
            pprint.pprint({spectrum_name: SPECTRUM_DESCRIPTIONS.get(spectrum_name, None)}, width=120)
    else:
        pprint.pprint(SPECTRUM_DESCRIPTIONS, width=120)
