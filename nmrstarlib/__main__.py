import sys
import json
import os
import time

from . import nmrstarlib

script = sys.argv.pop(0)
source = sys.argv.pop(0)

# sf = nmrstarlib.from_file(bmrbfile)
# sf = nmrstarlib.from_dir(bmrbfile)
# sf = nmrstarlib.from_archive(bmrbfile)
# sf = nmrstarlib.from_url(bmrbfile)
# sf = nmrstarlib.from_bmrbid(bmrbfile)
# for k in sf.keys():
#     print(k)

# print(sf["save_assigned_chem_shift_list_1"])

# with open('jsontest8.json', 'w') as outfile:
#     sf.write(outfile, fileformat='json', compressiontype='tar.bz2')
#
# with open('starformattest.txt', 'w') as outfile:
#     sf.write(outfile, fileformat='nmrstar', compressiontype='bz2')


# from_path, to_path
# def converter(path, from_format='nmrstar', to_format='json'):
#     if os.path.isdir(path):
#         for root, dirs, files in os.walk(path):
#             for fname in files:
#                 print(fname)
#                 starfile = nmrstarlib.from_file(os.path.abspath(fname))
#     else:
#         starfile = nmrstarlib.from_file(path)
#         with open(path + '.json', 'w') as outfile:
#             starfile.write(outfile, to_format)

# converter(bmrbfile)

filenames = nmrstarlib.generate_filenames(source)
filehandles = nmrstarlib.generate_handles(filenames)
for sf in nmrstarlib.from_whatever(filehandles):
    print("StarFile ID:", sf.bmrbid)






# # ============================= timetest
# d = os.path.abspath(sys.argv[1])
# print("Reading from %s.  "%(d),end='')
#
# filenames = os.listdir(d)
# print("Found %d files."%(len(filenames)))
# # print(filenames)
#
# ta = time.time()
# print("START:\r\t\t", ta)
#
# for i, f in enumerate(filenames):
#     fta = time.time()
#     try:
#         sf = nmrstarlib.StarFile.from_bmrbfile(os.path.join(d,f))
#         ftb = time.time()
#         print("OKAY\t" + f + "\t", ftb-fta, i)
#     except KeyboardInterrupt:
#         exit()
#     except:
#         ftb = time.time()
#         print("FAIL\t" + f + "\t", ftb-fta, i)
#
# tb = time.time()
# print("END:\r\t\t", tb)
# print("Files read in {} seconds".format(tb-ta))