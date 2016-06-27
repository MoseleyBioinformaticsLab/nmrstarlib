import sys
import json
import os
import zipfile
import tarfile
import time

from . import nmrstarlib

script = sys.argv[0]
sources = sys.argv[1:]

# sf = nmrstarlib.from_file(bmrbfile)
# sf = nmrstarlib.from_dir(bmrbfile)
# sf = nmrstarlib.from_archive(bmrbfile)
# sf = nmrstarlib.from_url(bmrbfile)
# sf = nmrstarlib.from_bmrbid(bmrbfile)

# with open('jsontest8.json', 'w') as outfile:
#     sf.write(outfile, fileformat='json', compressiontype='tar.bz2')
#
# with open('starformattest.txt', 'w') as outfile:
#     sf.write(outfile, fileformat='nmrstar', compressiontype='bz2')


def convert(from_path, output_dir='converted_files', from_format='nmrstar', to_format='json', output_dir_compression=''):
    file_extension = {'json': '.json',
                      'nmrstar': '.txt'}

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    for sf in nmrstarlib.from_whatever(from_path):
        if not output_dir_compression:
            with open(os.path.join(output_dir, sf.bmrbid + file_extension[to_format]), 'w') as outfile:
                outfile.write(sf.writestr(to_format))
        elif output_dir_compression == 'zip':
            with zipfile.ZipFile(output_dir + '.' + output_dir_compression, mode='a', compression=zipfile.ZIP_DEFLATED) as outfile:
                outfile.writestr(sf.bmrbid + file_extension[to_format], sf.writestr(to_format))

# convert(sources, output_dir_compression='zip')


for sf in nmrstarlib.from_whatever(sources):
    print("BMRB ID:", sf.bmrbid)
    print("Source:", sf.source)
#     print("Basename:", os.path.basename(sf.source))
#     print("Dirname:", os.path.dirname(sf.source))


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

