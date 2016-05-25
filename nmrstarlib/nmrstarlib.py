#!/usr/bin/env python3
#
# Copyright 2011 Patrick Mullaney (pajmullaney@gmail.com)
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import sys
import re
import bmrblexx as shlex
import logging

import itertools as it
import functools as ft

from copy import copy
#from collections import dict

class StarFile(dict):
    """The StarFile class stores the data from a single NMR-Star file in the
    form of an dict. Data can be accessed directly from the
    StarFile instance using bracket accessors.

    The NMR-Star format is a hierachical dictionary containing data on
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

#    def __str__(self):
#        s = 'data_%s\n'%(self.datanum)
#        for sf in self:
#            s + (self._print_sf(sf)+'\n')
#
#        return s

    def read(self, filename):
        self._filename = filename

        with open(filename, 'r') as infile:
            text = self._transform_text(infile.read())
            # text = infile.read()

        lexer = shlex.shlex(text)
        # lexer.quotes += self.LongStringQuote
        lexer.whitespace_split = True # whitespace_split is required for parsing floating point numbers
        lexer.infile = filename

        # for token in lexer:
        #     print("token from lexer:", token)

        return self._build_file(lexer)

    def write(self, filename=None, f=None):
        if filename is None:
            filename = self._filename

        if f is None:
            f = open(filename,'w')

        self._print_file(f)
        f.close()


    def _build_file(self,lexer):
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

    def _build_sf(self,lexer):
        odict = dict()

        loopcount = 0

        token = lexer.get_token()
        while token != 'save_':
            # print("TOKEN inside build_sf:", token)
            try:
                if token[0] == '_':
                    # This strips off the leading underscore of tagnames for readability 
                    odict[token[1:]] = lexer.get_token()
                    # print("token starts from _:", token)

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

    def _skip_sf(self,lexer):
        token = ''
        while  token != 'save_':
            token = lexer.get_token()
#            print(token) #DEBUG

    def _build_loop(self,lexer):
        fields = []
        values = []

        token = lexer.get_token()
        while token[0] == '_':
            fields.append(token[1:])
            token = lexer.get_token()

        while token != 'stop_':
            values.append(token)
            token = lexer.get_token()

        return (fields,values)
#        dlist = []
#
#        fields = []
#        values = []
#
#        token = lexer.get_token() 
##        #print(token) #DEBUG
#        while token[0] == '_':
#            fields.append(token[1:])
#            token = lexer.get_token()
#            #print(token) #DEBUG
#
#        proto_dict = dict(zip(fields, it.repeat(None)))
#
#        while token != 'stop_':
#            values.append(token)
#            token = lexer.get_token()
#            #print(token) #DEBUG
#
#        #TODO Clean this up, ideally using iterators.
#        try:
#            for i in range(len(values) // len(fields)):
#                dlist.append(copy(proto_dict))
#            for d in dlist:
#                for key in d:
#                    d[key] = values.pop(0)
#        except:
#            print("%s Error: Wrong number of values in loop"%(lexer.error_leader()), file=sys.stderr)
#            exit(1)
#
#        return dlist
    
    def _transform_text(self,text):
        leftsinglequote = re.compile("(\s\')([\w.,\[\(\{\'\-%<\?\+])")
        rightsinglequote = re.compile("([.,\w\]\)\}\'\"/])(\'[\s])")
        leftdoublequote = re.compile("(\s\")([\w.,\[\(\{\'\-%<\?\+])")
        rightdoublequote = re.compile("([.,\w\]\)\}\'\"/])(\"[\s])")

        lines = text.split('\n')

        newtext = ''
        for line in lines:
            if line and line[0] == ';':
                line = self.LongStringQuote

            # if line and "'" in line:
            #     print("before", line)
            #     left = re.search(leftsinglequote, line)
            #     right = re.search(rightsinglequote, line)
            #     if left is None or right is None:
            #         pass
            #     else:
            #         # print(left.group(2))
            #         # print(right.group(1))
            #         line = re.sub(leftsinglequote, ' "'+left.group(2), line)
            #         line = re.sub(rightsinglequote, right.group(1)+'" ', line)
            #     print("after", line)

            # if line and "\'" in line:
            #     singlequotes = re.compile("\'")
            #     print(line)
            #     for match in re.finditer(singlequotes, line):
            #         print(match.start(), match.group())

            newtext += ('\n' + line)
        return newtext

    # sf means saveframe; f means file
    def _print_file(self, f):
        print("data_%s\n"%(self.datanum), file=f)
        for sf in self.keys():
            print("save_%s"%(sf), file=f)
            self._print_saveframe(f,sf,3)
            print("save_\n", file=f)

    # We need to keep track of how far over everything is tabbed. The
    # "tab width" variable tw does this for us.
    def _print_saveframe(self, f, sf, tw):
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
    import json
    import os
    script = sys.argv.pop(0)
    filename = sys.argv.pop(0)
    sf = StarFile(filename)

    # for k in sf.keys(): print(k)
    # print(sf["assembly"])

    # with open("test.json", "w") as outfile:
    #     json.dump(sf, outfile, indent=4)

    # filenames = os.listdir("failed_bmrbs")
    # print(filenames)
    #
    # i = 1
    # for f in filenames:
    #     try:
    #         print("===================================================>", f)
    #         sf = StarFile("failed_bmrbs/"+f)
    #     except:
    #         print(f, "FAILED")
    #         i += 1
    #         continue


    # # Copy failed bmrbs
    # import os
    # import shutil
    #
    # filenames = ['bmr11026.str', 'bmr11038.str', 'bmr15178.str', 'bmr15442.str', 'bmr15511.str', 'bmr15757.str', 'bmr15965.str', 'bmr15969.str', 'bmr16021.str', 'bmr16273.str', 'bmr16373.str', 'bmr16622.str', 'bmr16895.str', 'bmr17054.str', 'bmr17089.str', 'bmr17445.str', 'bmr17645.str', 'bmr17647.str', 'bmr17685.str', 'bmr17973.str', 'bmr18159.str', 'bmr18160.str', 'bmr18380.str', 'bmr18731.str', 'bmr18873.str', 'bmr19131.str', 'bmr19220.str', 'bmr19315.str', 'bmr19505.str', 'bmr19752.str', 'bmr19844.str', 'bmr19878.str', 'bmr21022.str', 'bmr21023.str', 'bmr21024.str', 'bmr21025.str', 'bmr21026.str', 'bmr21027.str', 'bmr21028.str', 'bmr21041.str', 'bmr21042.str', 'bmr25066.str', 'bmr25070.str', 'bmr25278.str', 'bmr25459.str', 'bmr25460.str', 'bmr4397.str', 'bmr4418.str', 'bmr4428.str', 'bmr4429.str', 'bmr4706.str', 'bmr4802.str', 'bmr5042.str', 'bmr5156.str', 'bmr5183.str', 'bmr5770.str', 'bmr6018.str', 'bmr6123.str', 'bmr6591.str', 'bmr6637.str', 'bmr6639.str', 'bmr6647.str', 'bmr6656.str', 'bmr6657.str', 'bmr6890.str', 'bmr7084.str', 'bmr7126.str', 'bmr7139.str', 'bmr7191.str', 'bmr7194.str']
    # dst_dir = os.path.join(os.getcwd() + "/failed_bmrbs1")
    # os.mkdir(dst_dir)
    # for f in filenames:
    #     shutil.copy("../../bmrbscraper/NMR-STAR3/"+f, dst_dir)