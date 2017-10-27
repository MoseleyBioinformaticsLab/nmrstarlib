#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
nmrstarlib.bmrblex
~~~~~~~~~~~~~~~~~~

This module provides :func:`~nmrstarlib.bmrblex.bmrblex` lexical analyzer for
BMRB NMR-STAR format syntax. It is implemented as Python generator-based
state machine which generates (yields) token one at a time when
:py:func:`next()` is invoked on :func:`~nmrstarlib.bmrblex.bmrblex` instance.


Simplified description of parsing rules:
----------------------------------------
   * Each word or number separated by whitespace characters is a separate BMRB token.
   * Each single quoted (') string is a separate BMRB token, it should start with a single quote (')
     and end with a single quote *always* followed by whitespace character(s).
   * Each double quoted (") string is a separate BMRB token, it should start with a double quote (")
     and end with a double quote *always* followed by whitespace character(s).
   * Single quoted and double quoted strings have to be processed separately.
   * Single quoted and double quoted strings are processed one character at a time.
   * Multiline strings start with a semicolon *always* followed by new line character and
     ending with a semicolon *always* followed by whitespace character(s).
   * Multiline strings are processed one line at a time.

.. note::
   * For a full description of NMR-STAR file format, see official documentation:
     http://www.bmrb.wisc.edu/dictionary/
   * For a concise description of the NMR-STAR file format grammar see:
     https://github.com/mattfenwick/NMRPyStar#nmr-star-grammar
"""

from collections import deque


def transform_text(input_txt):
    """Transforms text into :py:class:`~collections.deque`, pre-processes
    multiline strings.

    :param str or bytes input_txt: Input text.
    :return: Double-ended queue of single characters and multiline strings.
    :rtype: :py:class:`~collections.deque`
    """
    if isinstance(input_txt, str):
        text = u"{}".format(input_txt)
    elif isinstance(input_txt, bytes):
        text = input_txt.decode("utf-8")
    else:
        raise TypeError("Expecting <class 'str'> or <class 'bytes'>, but {} was passed".format(type(input_txt)))

    inputq = deque(text.split(u"\n"))
    outputq = deque()

    cdef unicode line
    cdef unicode character
    cdef unicode multiline
    cdef unicode comment

    while len(inputq) > 0:
        line = inputq.popleft()

        if line.lstrip().startswith(u"#"):
            comment = u"" + line + u"\n"
            line = inputq.popleft()

            while line.lstrip().startswith(u"#"):
                comment += line + u"\n"
                line = inputq.popleft()

            outputq.append(comment)

            for character in line:
                outputq.append(character)

        elif line.startswith(u";"):
            multiline = u"\n;\n"
            line = inputq.popleft()

            while not line.startswith(u";"):
                multiline += line + u"\n"
                line = inputq.popleft()

            multiline += line[:1]
            outputq.append(multiline[3:-1])  # remove NMR-STAR syntax from multiline string

            for character in line[1:]:
                outputq.append(character)

        else:
            for character in line:
                outputq.append(character)

        outputq.append(u"\n")

    outputq.extend([u"\n", u""])  # end of file signal

    return outputq


def bmrblex(text):
    """A lexical analyzer for the BMRB NMR-STAR format syntax.

    :param text: Input text.
    :type text: :py:class:`str` or :py:class:`bytes`
    :return: Current token.
    :rtype: :py:class:`str`
    """
    stream = transform_text(text)

    cdef unicode wordchars = (u"abcdfeghijklmnopqrstuvwxyz"
                              u"ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789_"
                              u"ßàáâãäåæçèéêëìíîïðñòóôõöøùúûüýþÿ"
                              u"ÀÁÂÃÄÅÆÇÈÉÊËÌÍÎÏÐÑÒÓÔÕÖØÙÚÛÜÝÞ"
                              u"!@$%^&*()_+:;?/>.<,~`|\{[}]-=")

    cdef unicode whitespace = u" \t\v\r\n"
    cdef unicode comment = u"#"
    cdef unicode state = u" "
    cdef unicode token = u""
    cdef unicode single_line_comment = u""
    cdef unicode nextchar
    cdef unicode nextnextchar

    while len(stream) > 0:
        nextnextchar = stream.popleft()

        while True:
            nextchar = nextnextchar

            if len(stream) > 0:
                nextnextchar = stream.popleft()
            else:
                nextnextchar = u""

            # Process multiline string, comment, or single line comment
            if len(nextchar) > 1:
                state = u" "
                token = nextchar
                break  # emit current token

            elif nextchar in whitespace and nextnextchar in comment and state not in (u"'", u'"'):
                single_line_comment = u""
                state = u"#"

            if state is None:
                token = u""  # past end of file
                break

            elif state == u" ":
                if not nextchar:
                    state = None
                    break

                elif nextchar in whitespace:
                    if token:
                        state = u" "
                        break  # emit current token
                    else:
                        continue

                elif nextchar in wordchars:
                    token = nextchar
                    state = u"a"

                elif nextchar == u"'" or nextchar == u'"':
                    token = nextchar
                    state = nextchar

                else:
                    token = nextchar
                    if token:
                        state = u" "
                        break  # emit current token
                    else:
                        continue

            # Process single-quoted or double-quoted token
            elif state == u"'" or state == u'"':
                token += nextchar
                if nextchar == state:
                    if nextnextchar in whitespace:
                        state = u" "
                        token = token[1:-1]  # remove single or double quotes from the ends
                        break

            # Process single line comment
            elif state == u"#":
                single_line_comment += nextchar
                if nextchar == u"\n":
                    state = u" "
                    break

            # Process regular (unquoted) token
            elif state == u"a":
                if not nextchar:
                    state = None
                    break
                elif nextchar in whitespace:
                    state = u" "
                    if token:
                        break  # emit current token
                    else:
                        continue
                else:
                    token += nextchar

        if nextnextchar:
            stream.appendleft(nextnextchar)

        yield token
        token = u""
