#!/usr/bin/env python3

import sys
import os
import time
import psutil
import nmrstarlib as nmr

d = os.path.abspath(sys.argv[1])
print("Reading from %s.  "%(d),end='')

filenames = os.listdir(d)
print("Found %d files."%(len(filenames)))

ta = time.time()
print("START:\r\t\t", ta)

for f in filenames:
    fta = time.time()
    try:
        sf = nmr.StarFile(os.path.join(d,f))
        ftb = time.time()
        print("OKAY\t" + f + "\t", ftb-fta)
    except KeyboardInterrupt:
        exit()
    except:
        ftb = time.time()
        print("FAIL\t" + f + "\t", ftb-fta)

tb = time.time()
print("END:\r\t\t", tb)
print("Files read in {} seconds".format(tb-ta))