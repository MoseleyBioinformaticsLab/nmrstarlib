#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
nmrstarlib.bmrblex
~~~~~~~~~~~~~~~~~~

A lexical analyzer for BMRB NMR-STAR format syntax.

This module is based on python ``shlex`` module modified to address specifics of BMRB NMR-STAR format.
The ``shlex`` class makes it easy to write lexical analyzers for simple syntaxes resembling
that of the Unix shell. Documentation: https://docs.python.org/3/library/shlex.html


Simplified description of parsing rules:
----------------------------------------
   * Each word or number separated by whitespace characters is a separate BMRB token.
   * Each single quoted (') string is a separate BMRB token, it should start with single quote (')
     and end with single quote *always* followed by whitespace character(s).
   * Each double quoted (") string is a separate BMRB token, it should start with double quote (")
     and end with double quote *always* followed by whitespace character(s).
   * Single quoted and double quoted strings have to be processed separately.
   * Single quoted and double quoted strings are processed one character at a time.
   * Multiline strings starts with semicolon *always* followed by new line character and
     end with semicolon *always* followed by whitespace character(s).
   * Multiline strings are processed one line at a time.

.. note::
   * For full description of NMR-STAR file format see official documentation: http://www.bmrb.wisc.edu/dictionary/
   * For concise description of NMR-STAR file format grammar see: https://github.com/mattfenwick/NMRPyStar#nmr-star-grammar
"""

import sys
from collections import deque
from io import StringIO

__all__ = ["bmrblex"]


class bmrblex:
    """A lexical analyzer for BMRB NMR-STAR format syntax."""

    multilinequote = 'ಠ'

    def __init__(self, instream=None):
        """Initialize stream string and attributes.

        :param instream: Input string to be converted into stream object for tokens processing.
        :type instream: str or bytes
        """
        if isinstance(instream, str):
            text = self._transform_text(instream)
        elif isinstance(instream, bytes):
            text = self._transform_text(instream.decode("utf-8"))
        else:
            raise TypeError("Expecting <class 'str'> or <class 'bytes'>, but {} was passed".format(type(instream)))

        instream = StringIO(text)

        if instream is not None:
            self.instream = instream
        else:
            self.instream = sys.stdin

        self.eof = ''
        self.commenters = '#'
        self.wordchars = ('abcdfeghijklmnopqrstuvwxyz'
                          'ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789_'
                          'ßàáâãäåæçèéêëìíîïðñòóôõöøùúûüýþÿ'
                          'ÀÁÂÃÄÅÆÇÈÉÊËÌÍÎÏÐÑÒÓÔÕÖØÙÚÛÜÝÞ'
                          '!@#$%^&*()_+:;?/>.<,~`|\{[}]-=')
        self.whitespace = ' \t\r\n'
        self.escapedquotes = '"'
        self.state = ' '
        self.pushback = deque()
        self.token = ''
        self.singlequote = "'"
        self.doublequote = '"'

        # stream position gets incremented by 1 each time instream.read(1) is called
        # since instream has 0-based numeration, the first emitted character
        # gets streamposition = 0, hence initial streamposition = -1
        self.streamposition = -1
        self.streamlength = len(text)

    def _transform_text(self, text):
        """Replace all lines that start with ';' with special character
        to simplify multiline string processing with bmrblex.

        :param str text: Original text.
        :return: Transformed text where lines starting with ';' replaced by special character.
        :rtype: str
        """
        lines = text.split('\n')
        newtext = ''
        for line in lines:
            if line and line.startswith(';'):
                line = self.multilinequote + line[1:]
            newtext += line + '\n'
        return newtext
 
    def get_token(self):
        """Get a token from the input stream (or from stack if it's nonempty).

        :return: Current token.
        :rtype: str
        """
        if self.pushback:
            token = self.pushback.popleft()
            return token
        # No pushback.  Get a token.
        raw = self._read_token()
        return raw

    def _get_nextchar(self):
        nextchar = self.instream.read(1)
        self.streamposition += 1
        return nextchar

    def _get_nextnextchar(self):
        nextnextchar = self.instream.read(1)
        self.instream.seek(self.streamposition + 1)
        return nextnextchar

    def _read_token(self):
        """Read token based on the parsing rules.

        :return: Current token.
        :rtype: str
        """
        quoted = False

        # next streamposition, i.e. streamposition+1 should not exceed the number of
        # characters inside instream, streamlength-1 ==> stopping criteria for the while loop
        while self.streamposition+1 < self.streamlength-1:
            nextchar = self.instream.read(1)
            self.streamposition += 1
            # nextchar = self._get_nextchar()

            nextnextchar = self.instream.read(1)       # look up 1 char ahead
            self.instream.seek(self.streamposition+1)  # return to current stream position
            # nextnextchar = self._get_nextnextchar()

            if self.state is None:
                self.token = ''        # past end of file
                break

            elif self.state == ' ':
                if not nextchar:
                    self.state = None  # end of file
                    break
                elif nextchar in self.whitespace:
                    if self.token:
                        break   # emit current token
                    else:
                        continue
                elif nextchar in self.commenters:
                    line = self.instream.readline()
                    self.streamposition += len(line)
                elif nextchar in self.wordchars:
                    self.token = nextchar
                    self.state = 'a'
                elif nextchar in self.singlequote:
                    self.token = nextchar
                    self.state = nextchar
                elif nextchar in self.doublequote:
                    self.token = nextchar
                    self.state = nextchar
                elif nextchar in self.multilinequote:
                    # self.token = nextchar
                    self.state = nextchar
                else:
                    self.token = nextchar
                    if self.token:
                        break   # emit current token
                    else:
                        continue

            # Process multiline-quoted text
            elif self.state == self.multilinequote:
                quoted = True
                if not nextchar:      # end of file
                    raise EOFError("No closing quotation")

                line = self.instream.readline()
                self.streamposition += len(line)

                while True:
                    if line.startswith('ಠ'):
                        self.streamposition -= len(line)  # get back to the beginning of line
                        nextchar = self.instream.read(1)  # emit nextchar after 'ಠ'
                        self.streamposition += 1
                        self.token = '\n;\n' + self.token + ';'
                        self.state = ' '
                        break   # emit current token
                    else:
                        self.token = self.token + line
                        line = self.instream.readline()
                        self.streamposition += len(line)

            # process token staring with single quote '
            elif self.state in self.singlequote:
                quoted = True
                if not nextchar:      # end of file
                    raise EOFError("No closing quotation")

                if nextchar == self.state:
                    if nextnextchar not in self.whitespace:
                        self.token = self.token + nextchar
                        self.state = self.singlequote
                    elif nextnextchar in self.whitespace:
                        self.token = self.token + nextchar
                        self.state = ' '
                        break   # emit current token
                else:
                    self.token = self.token + nextchar

            # process token staring with double quote "
            elif self.state in self.doublequote:
                quoted = True
                if not nextchar:      # end of file
                    raise EOFError("No closing quotation")
                if nextchar == self.state:
                    if nextnextchar not in self.whitespace:
                        self.token = self.token + nextchar
                        self.state = self.doublequote
                    elif nextnextchar in self.whitespace:
                        self.token = self.token + nextchar
                        self.state = ' '
                        break
                else:
                    self.token = self.token + nextchar

            #
            elif self.state == 'a':
                if not nextchar:
                    self.state = None   # end of file
                    break
                elif nextchar in self.whitespace:
                    self.state = ' '
                    if self.token or quoted:
                        break   # emit current token
                    else:
                        continue
                else:
                    self.token = self.token + nextchar

        result = self.token
        self.token = ''
        return result

    def __iter__(self):
        return self

    def __next__(self):
        token = self.get_token()
        if token == self.eof:
            raise StopIteration
        return token
