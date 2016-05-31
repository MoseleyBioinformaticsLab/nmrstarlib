import sys
from . import nmrstarlib

script = sys.argv.pop(0)
filename = sys.argv.pop(0)
sf = nmrstarlib.StarFile(filename)