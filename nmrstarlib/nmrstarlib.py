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

    @classmethod
    def from_bmrbfile(cls, filepath):
        """Construct StarFile from local BMRB NMR-STAR file

        :param str filepath: Path to NMR-STAR file
        :return: StarFile dict
        :rtype: dict
        """
        try:
            starfile = cls()
            with open(filepath, 'r') as infile:
                starfile.read(infile)
            return starfile
        except FileNotFoundError:
            raise FileNotFoundError("Check filename or directory name: \"{}\"".format(filepath)) from None

    @classmethod
    def from_url(cls, url):
        """Construct StarFile from URL address of BMRB NMR-STAR file

        :param str url: URL address of BMRB NMR-STAR file
        :return: StarFile dict
        :rtype: dict
        """
        try:
            response = urllib.request.urlopen(url)
            starfile = cls()
            starfile.read(response)
            return starfile
        except urllib.error.HTTPError:
            raise urllib.error.HTTPError("Invalid URL, check that URL is correct") from None

    @classmethod
    def from_bmrbid(cls, bmrbid, base_url = "http://rest.bmrb.wisc.edu/bmrb/NMR-STAR3/"):
        """Construct StarFile using BMRB NMR-STAR file id

        :param str bmrbid: BMRB id of NMR-STAR file, must be integer
        :param str base_url: URL address where BMRB stores NMR-STAR files
        :return: StarFile dict
        :rtype: dict
        """
        try:
            bmrbid = int(bmrbid)
            file_url = base_url + str(bmrbid)
            starfile = cls.from_url(file_url)
            return starfile
        except ValueError:
            raise ValueError ("Couldn't parse BMRB id, BMRB id must be integer") from None

    @classmethod
    def from_json(cls, filepath):
        """Construct StarFile from json file

        :param str filepath: path to JSON file
        :return: instance of `StarFile` dict class
        :rtype: dict
        """
        starfile = cls()
        with open(filepath, 'r') as infile:
            odict = json.load(infile)
        starfile.update(odict)
        return starfile

    def to_json(self, filepath):
        """Save StarFile dict into JSON file

        :param str filepath:
        :return: None
        :rtype: None
        """
        json_str = json.dumps(self, sort_keys=False, indent=4)
        self.write(json_str, filepath)

    def to_bmrb(self, filepath):
        """Save StarFile dict into BMRB file

        :param filepath:
        :return:
        """
        pass

    # @staticmethod
    def iscompressed(self, filehandle):
        """

        :param filehandle:
        :return:
        """
        file_signature = {b'\x1f\x8b\x08': 'gz',
                          b'\x42\x5a\x68': 'bz2',
                          b'\x50\x4b\x03\x04': 'zip'}

        max_len = max(len(x) for x in file_signature)
        file_start = filehandle.read(max_len)
        filehandle.seek(0)

        for signature, filetype in file_signature.items():
            if file_start.startswith(signature):
                return filetype
        return ''

    def uncompress(self, filepath, filetype):
        filehandles = []

        if filetype == 'zip':
            ziparchive = zipfile.ZipFile(filepath)
            for fname in ziparchive.infolist():
                f = ziparchive.open(fname)
                filehandles.append(f)

        elif filetype == 'bz2':
            if tarfile.is_tarfile(filepath):
                tararchive = tarfile.open(filepath)
                for fname in tararchive:
                    f = tararchive.extractfile(fname)
                    filehandles.append(f)
            else:
                filehandles.append(bz2.open(filepath))

        elif filetype == 'gz':
            if tarfile.is_tarfile(filepath):
                tar = tarfile.open(filepath)
                for fname in tar:
                    f = tar.extractfile(fname)
                    filehandles.append(f)
            else:
                filehandles.append(gzip.open(filepath))

        return filehandles

    def read(self, filehandle):
        """Read BMRB NMR-STAR file into `StarFile` dict object

        :param filename: path to input BMRB NMR-STAR file
        :return: instance of `StarFile` dict class
        :rtype: dict
        """
        lexer = bmrblex2.bmrblex(filehandle.read())
        # lexer = bmrblex.bmrblex(filehandle.read()) # return that
        return self._build_file(lexer)

    # def write(self, filename=None, f=None):
    #     """Write `StarFile` dict object into text file
    #
    #     :param str filename: path of input BMRB NMR-STAR file
    #     :param str f: path to output BMRB NMR-STAR file
    #     :return: None
    #     :rtype: None
    #     """
    #     if filename is None:
    #         filename = self._filename
    #
    #     if f is None:
    #         f = open(filename,'w')
    #
    #     self._print_file(f)
    #     f.close()

    def write(self, strrepr, filepath): # filehandle
        """Write StarFile into file in BMRB format

        :param str filepath: path to output file
        :return: None
        :rtype: None
        """
        with open(filepath, 'w') as outfile:
            outfile.write(strrepr)

    def _build_file(self, lexer):
        """Build `StarFile` dict object

        :param lexer: instance of BMRB lexical analyzer class
        :type lexer: nmrstarlib.bmrblex.bmrblex
        :return: instance of `StarFile` object
        :rtype: nmrstarlib.nmrstarlib.StarFile
        """
        odict = self
        token = lexer.get_token()
        # print(token) #DEBUG

        while token != '':
            # print(token) #DEBUG
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
                    print("%s Error: Invalid token %s"%(lexer.error_leader(), token), file=sys.stderr)
                    print("In _build_file try block", file=sys.stderr) #DEBUG
                    raise InvalidToken("%s %s"%(lexer.error_leader(),token))
            except IndexError:
                print("%s Error: Invalid token %s"%(lexer.error_leader(), token), file=sys.stderr)
                print("In _build_file except block", file=sys.stderr) #DEBUG
                raise
            finally:
                token = lexer.get_token()
                #print(token) #DEBUG
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
                    odict['loop_%s'%(loopcount)] = self._build_loop(lexer)
                    loopcount += 1

                else:
                    print("%s Error: Invalid token %s"%(lexer.error_leader(), token), file=sys.stderr)
                    print("In _build_sf try block", file=sys.stderr) #DEBUG
                    raise InvalidToken("%s %s"%(lexer.error_leader(),token))

            except IndexError:
                print("%s Error: Invalid token %s"%(lexer.error_leader(), token), file=sys.stderr)
                print("In _build_sf except block", file=sys.stderr) #DEBUG
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
        :type lexer: nmrstarlib.bmrblex.bmrblex
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
        :type lexer: nmrstarlib.bmrblex.bmrblex
        :return: Fields and values of the loop
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

        # dvalues = [OrderedDict(zip(fields, values[i:i + len(fields)])) for i in range(0, len(values), len(fields))]

        return (fields, values)
        # return dvalues

    def _print_file(self, filepath):
        """Print StarFile."""
        print("data_{}\n".format(self.bmrbid), file=filepath)
        for saveframe in self.keys():
            print("save_{}".format(saveframe), file=filepath)
            self._print_saveframe(filepath, saveframe, 3)
            print("save_\n", file=filepath)

    def _print_saveframe(self, f, sf, tw):
        """Print saveframe.
        We need to keep track of how far over everything is tabbed.
        The "tab width" variable tw does this for us.
        """
        for ind in self[sf].keys():
            # handle the NMR-Star "long string" type
            if self[sf][ind][0] == ';':
                print(tw*' ',"_%s"%(ind), file=f)
                print(";\n%s\n;"%(self[sf][ind][1:-1]), file=f)
            # handle loops
            elif ind[:5] == "loop_":
                print(tw*' ',"loop_", file=f)
                self._print_loop(f,sf,ind,tw+3)
                #print(2*tw*' ',"Not implemented...", file=f)
                print(tw*' ',"stop_\n", file=f)
            else:
                print(tw*' ',"_%s\t%s"%(ind,self[sf][ind]), file=f)

    def _print_loop(self, f, sf, ind, tw):
        """Print loop."""
        # First print the keys
        for key in self[sf][ind][0].keys():
            print(tw*' ','_%s'%(key), file=f)
        print("\n", file=f)

        # Then print the values
        for record in self[sf][ind]:
            line = tw*' ' + ' '.join(record[i] for i in record.keys())
            print(line, file=f)


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


if __name__ == "__main__":
    script = sys.argv.pop(0)
    filename = sys.argv.pop(0)
    sf = StarFile(filename)
    sf.to_json('jsontest2.json')


# class TagParserError(Exception):
#     """Exception class for errors thrown by TagParser."""
#     def __init__(self, message, sheetName, rowIndex, columnIndex) :
#         self.value = message + " at cell \"" + sheetName + "\"[" + TagParserError.columnName(columnIndex) + str(rowIndex+1) + "]"
#
#     @staticmethod
#     def columnName(columnIndex) :
#         """RETURNS Excel-style column name for PARAMETER columnIndex (integer)."""
#         if columnIndex < 0 :
#             return ":"
#         dividend = columnIndex+1
#         name = ""
#         while dividend > 0 :
#             modulo = (dividend - 1 ) % 26
#             name = chr(65+modulo) + name
#             dividend = int((dividend - modulo) / 26)
#         return name
#
#     def __str__(self) :
#         return repr(self.value)

# (11:58:35 AM) Hunter Moseley: .txt, .json, .str, .gz .bz2 .zip
# (12:02:23 PM) Hunter Moseley: toJSON and toBMRB writes to a filehandle.
# (12:03:12 PM) Hunter Moseley: toJSONFile toBMRBFile writes to a file, but checks if it is a compressed format or not by checking the given extension of the provided filename.
# (12:03:33 PM) Hunter Moseley: toFile
# (12:03:40 PM) Hunter Moseley: fromFile