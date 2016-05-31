#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
nmrstarlib.nmrstarlib
~~~~~~~~~~~~~~~~~~~~~

"""

import sys
import bmrblex

class StarFile(dict):
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
    def __init__(self, filename, frame_categories=None):
        super().__init__(self)
        # Leave frame_categories as None to read everything.  Otherwise it can be
        # a list of saveframe categories to read, skipping the rest
        self._frame_categories = frame_categories
        self.read(filename)

    def read(self, filename):
        """Read BMRB NMR-STAR file into `StarFile` dict object

        :param filename: path to input BMRB NMR-STAR file
        :return: instance of `StarFile` dict class
        :rtype: nmrstarlib.nmrstarlib.StarFile
        """
        self._filename = filename

        with open(filename, 'r') as infile:
            text = self._transform_text(infile.read())
            # text = infile.read()

        lexer = bmrblex.bmrblex(text)
        lexer.whitespace_split = True # whitespace_split is required for parsing floating point numbers
        lexer.infile = filename
        return self._build_file(lexer)

    def write(self, filename=None, f=None):
        """Write `StarFile` dict object into text file

        :param str filename: path of input BMRB NMR-STAR file
        :param str f: path to output BMRB NMR-STAR file
        :return: None
        :rtype: None
        """
        if filename is None:
            filename = self._filename

        if f is None:
            f = open(filename,'w')

        self._print_file(f)
        f.close()

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
                    name = token[5:]
                    frame = self._build_sf(lexer)
                    if frame:
                        odict[name] = frame
                    
                elif token[0:5] == 'data_':
                    self.datanum = token[5:]
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
        odict = dict()
        loopcount = 0

        token = lexer.get_token()
        while token != 'save_':
            print("TOKEN inside build_sf:", token)
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

        return (fields, values)
        # dlist = []
        #
        # fields = []
        # values = []
        #
        # token = lexer.get_token()
        # #print(token) #DEBUG
        # while token[0] == '_':
        #     fields.append(token[1:])
        #     token = lexer.get_token()
        #     #print(token) #DEBUG
        #
        # proto_dict = dict(zip(fields, it.repeat(None)))
        #
        # while token != 'stop_':
        #     values.append(token)
        #     token = lexer.get_token()
        #     #print(token) #DEBUG
        #
        # #TODO Clean this up, ideally using iterators.
        # try:
        #     for i in range(len(values) // len(fields)):
        #         dlist.append(copy(proto_dict))
        #     for d in dlist:
        #         for key in d:
        #             d[key] = values.pop(0)
        # except:
        #     print("%s Error: Wrong number of values in loop"%(lexer.error_leader()), file=sys.stderr)
        #     exit(1)
        #
        # return dlist
    
    def _transform_text(self, text):
        """Replace all lines that start with ';' with special character 'ಠ'
        to simplify multiline string processing with bmrblex.

        :param str text: Original text
        :return: Transformed text where lines starting with ';' replaced by 'ಠ'
        :rtype: str
        """
        lines = text.split('\n')
        newtext = ''
        for line in lines:
            if line and line.startswith(';'):
                line = self.LongStringQuote
            newtext += ('\n' + line)
        return newtext

    def _print_file(self, f):
        """Print `StarFile` object.
        sf means saveframe, f means file.
        """
        print("data_%s\n"%(self.datanum), file=f)
        for sf in self.keys():
            print("save_%s"%(sf), file=f)
            self._print_saveframe(f, sf, 3)
            print("save_\n", file=f)

    def _print_saveframe(self, f, sf, tw):
        """Print saveframe.
        We need to keep track of how far over everything is tabbed.
        The "tab width" variable tw does this for us.
        """
        for ind in self[sf].keys():
            # handle the NMR-Star "long string" type
            if self[sf][ind][0] == self.LongStringQuote:
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

    # We need a hack for handling multiline strings, since they are allowed
    # to contain the multiline string quote mark (";"). I arbitrarily
    # selected unicode U+0CA0 (KANNADA LETTER TTHA) because it should never
    # appear naturally in a STAR file.
    LongStringQuote = 'ಠ'


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