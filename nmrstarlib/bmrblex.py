"""A lexical analyzer class for simple shell-like syntaxes."""

# Module and documentation by Eric S. Raymond, 21 Dec 1998
# Input stacking and error message cleanup added by ESR, March 2000
# push_source() and pop_source() made explicit by ESR, January 2001.
# Posix compliance, split(), string arguments, and
# iterator interface by Gustavo Niemeyer, April 2003.

# Modified to address specifics of bmrb STAR format.

import os.path
import sys
from collections import deque

from io import StringIO

__all__ = ["shlex", "split"]

class shlex:
    "A lexical analyzer class for simple shell-like syntaxes."
    def __init__(self, instream=None, infile=None):
        if isinstance(instream, str):
            instream = StringIO(instream)
        if instream is not None:
            self.instream = instream
            self.infile = infile
        else:
            self.instream = sys.stdin
            self.infile = None

        self.eof = ''
        self.commenters = '#'
        self.wordchars = ('abcdfeghijklmnopqrstuvwxyz'
                          'ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789_'
                          'ßàáâãäåæçèéêëìíîïðñòóôõöøùúûüýþÿ'
                          'ÀÁÂÃÄÅÆÇÈÉÊËÌÍÎÏÐÑÒÓÔÕÖØÙÚÛÜÝÞ'
                          '!@#$%^&*()_+:;?/>.<,~`|\{[}]-=')
        self.whitespace = ' \t\r\n'
        self.quotes = '\'"'
        self.escapedquotes = '"'
        self.state = ' '
        self.pushback = deque()
        self.token = ''
 
#    def push_token(self, tok):
#        "Push a token onto the stack popped by the get_token method"
#        self.pushback.appendleft(tok)

    def get_token(self):
        """Get a token from the input stream (or from stack if it's nonempty)."""
        if self.pushback:
            tok = self.pushback.popleft()
            return tok
        # No pushback.  Get a token.
        raw = self.read_token()
        return raw

    def get_unquoted_token(self):
        """Get a token from the input stream (or from stack if it's nonempty)."""
        if self.pushback:
            tok = self.pushback.popleft()
            return tok
        # No pushback.  Get a token.
        raw = self.read_unquoted_token()
        return raw

    def read_token(self):
        quoted = False
        escapedstate = ' '
        while True:
            nextchar = self.instream.read(1)
            print("nextchar from lexer:", nextchar)


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
                    self.instream.readline()
                elif nextchar in self.wordchars:
                    self.token = nextchar
                    self.state = 'a'
                elif nextchar in self.quotes:
                    self.token = nextchar
                    self.state = nextchar
                else:
                    self.token = nextchar
                    if self.token:
                        break   # emit current token
                    else:
                        continue

            elif self.state in self.quotes:
                quoted = True
                if not nextchar:      # end of file
                    # XXX what error should be raised here?
                    raise ValueError("No closing quotation")
                if nextchar == self.state:
                    self.token = self.token + nextchar
                    self.state = ' '
                    break
                else:
                    self.token = self.token + nextchar
            elif self.state == 'a':
                if not nextchar:
                    self.state = None   # end of file
                    break
                elif nextchar in self.whitespace:
                    self.state = ' '
                    if self.token or (self.posix and quoted):
                        break   # emit current token
                    else:
                        continue
                # elif nextchar in self.wordchars or nextchar in self.quotes \
                #     or self.whitespace_split:
                else:
                    self.token = self.token + nextchar
        result = self.token
        self.token = ''
        return result

    def read_unquoted_token(self):
        while not self.pushback:
            line = self.instream.readline()
            for word in line.split():
                if word[0] in self.commenters:
                    break
                else:
                    self.instream.append(word)
        result = self.pushback.popleft()
        return result

    def error_leader(self, infile=None, lineno=None):
        """Emit a C-compiler-like, Emacs-friendly error-message leader."""
        if infile is None:
            infile = self.infile
        # if lineno is None:
        #     lineno = self.lineno
        # return "\"%s\", line %d: " % (infile, lineno)
        return ''

    def __iter__(self):
        return self

    def __next__(self):
        token = self.get_token()
        if token == self.eof:
            raise StopIteration
        return token

if __name__ == '__main__':
    if len(sys.argv) == 1:
        lexer = shlex()
    else:
        file = sys.argv[1]
        lexer = shlex(open(file), file)
    while 1:
        tt = lexer.get_token()
        if tt:
            print("Token: " + repr(tt))
        else:
            break
