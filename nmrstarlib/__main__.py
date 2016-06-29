import sys
import json
import os
import io
import zipfile
import tarfile
import bz2
import gzip
import time
from pathlib import Path

from . import nmrstarlib

script = sys.argv[0]
sources = sys.argv[1:]

class Converter(object):

    file_extension = {'json':    '.json',
                      'nmrstar': '.txt',
                      'zip':     '.zip',
                      'gz':      '.gz',
                      'bz2':     '.bz2',
                      'tar.gz':  '.tar.gz',
                      'tar.bz2': '.tar.bz2',
                      'tar':     '.tar'}

    def __init__(self, from_path, to_path, from_format='nmrstar', to_format='json'):
        self.from_path = from_path
        self.to_path = to_path
        self.from_format = from_format
        self.to_format = to_format

        self.from_path_compression = nmrstarlib.GenericFilePath.is_compressed(from_path)
        self.to_path_compression = nmrstarlib.GenericFilePath.is_compressed(to_path)

    def convert(self):
        if os.path.isdir(self.from_path):
            self._many_to_many()
        elif os.path.isfile(self.from_path) or nmrstarlib.GenericFilePath.is_url(self.from_path):
            if self.from_path_compression in ('zip', 'tar', 'tar.gz', 'tar.bz2'):
                self._many_to_many()
            elif self.from_path_compression in ('gz', 'bz2'):
                self._one_to_one()
            elif not self.from_path_compression:
                self._one_to_one()
        elif self.from_path.isdigit():
            self._one_to_one()
        else:
            raise TypeError('Unknown input file format: "{}"'.format(self.from_path))

    def _many_to_many(self):
        for sf in nmrstarlib.read_files([self.from_path]):
            if not self.to_path_compression:
                self._to_dir(sf)
            elif self.to_path_compression == 'zip':
                self._to_zipfile(sf)
            elif self.to_path_compression in ('tar', 'tar.gz', 'tar.bz2'):
                self._to_tarfile(sf)
            elif self.to_path_compression in ('gz', 'bz2'):
                raise TypeError("Many-to-one conversion, cannot convert {} into {}".format(self.from_path, self.to_path))
            else:
                raise TypeError('Unknown output file format: "{}"'.format(self.to_path))

        if self.to_path_compression == 'tar.gz':
            with open(self.to_path[:-3], 'rb') as infile, gzip.GzipFile(self.to_path, 'wb') as outfile:
                outfile.write(infile.read())
        elif self.to_path_compression == 'tar.bz2':
            with open(self.to_path[:-4], 'rb') as infile, bz2.BZ2File(self.to_path, 'wb') as outfile:
                outfile.write(infile.read())

    def _one_to_one(self):
        for sf in nmrstarlib.read_files([self.from_path]):
            if not self.to_path_compression:
                self._to_textfile(sf)
            elif self.to_path_compression == 'gz':
                self._to_gzipfile(sf)
            elif self.to_path_compression == 'bz2':
                self._to_bz2file(sf)
            elif self.to_path_compression in ('tar', 'tar.gz', 'tar.bz2', 'zip'):
                raise TypeError('One-to-many conversion, cannot convert "{}" into "{}"'.format(self.from_path, self.to_path))
            else:
                raise TypeError('Unknown format: "{}"'.format(self.to_path))

    def _to_dir(self, starfile):
        inpath = Path(starfile.source)
        subdir = os.path.join(*" ".join(inpath.parts[1:-1]).split(" "))
        fname = inpath.name

        outpath = os.path.join(self.to_path, subdir, fname)
        if not os.path.exists(os.path.dirname(outpath)):
            os.makedirs(os.path.dirname(outpath))
        with open(outpath + self.file_extension[self.to_format], mode='w') as outfile:
            outfile.write(starfile.writestr(self.to_format))

    def _to_zipfile(self, starfile):
        inpath = Path(starfile.source)
        subdir = os.path.join(*" ".join(inpath.parts[1:-1]).split(" "))
        fname = inpath.name
        outpath = os.path.join(subdir, fname)
        with zipfile.ZipFile(self.to_path, mode='a', compression=zipfile.ZIP_DEFLATED) as outfile:
            outfile.writestr(outpath + self.file_extension[self.to_format], starfile.writestr(self.to_format))

    def _to_tarfile(self, starfile):
        inpath = Path(starfile.source)
        subdir = os.path.join(*" ".join(inpath.parts[1:-1]).split(" "))
        fname = inpath.name
        outpath = os.path.join(subdir, fname)

        if self.to_path.endswith('.gz'):
            tar_path = self.to_path[:-3]
        elif self.to_path.endswith('.bz2'):
            tar_path = self.to_path[:-4]
        else:
            tar_path = self.to_path

        with tarfile.TarFile(tar_path, mode='a') as outfile:
            info = tarfile.TarInfo(outpath + self.file_extension[self.to_format])
            data = starfile.writestr(self.to_format).encode()
            info.size = len(data)
            outfile.addfile(tarinfo=info, fileobj=io.BytesIO(data))

    def _to_bz2file(self, starfile):
        with bz2.BZ2File(self.to_path, mode='wb') as outfile:
            outfile.write(starfile.writestr(self.to_format).encode())

    def _to_gzipfile(self, starfile):
        with gzip.GzipFile(self.to_path, mode='wb') as outfile:
            outfile.write(starfile.writestr(self.to_format).encode())

    def _to_textfile(self, starfile):
        to_path = self.to_path if self.to_path.endswith(self.file_extension[self.to_format]) \
                               else self.to_path + self.file_extension[self.to_format]
        with open(to_path, mode='w') as outfile:
            outfile.write(starfile.writestr(self.to_format))

for source in sources:
    converter = Converter(from_path=source, to_path='convertertest/urlpizdectestdir')
    converter.convert()





# for sf in nmrstarlib.read_files(sources):
#     print("BMRB ID:", sf.bmrbid)
#     print("Source:", sf.source)
#     print("Basename:", os.path.basename(sf.source))
#     print("Dirname:", os.path.dirname(sf.source))
#     print("Split:", os.path.split(sf.source))

    # path = Path(sf.source)
    # parentdir = os.path.join(path.parts[0])
    # subdir = os.path.join(path.parts[1:-1])
    # fname = path.name
    #
    # print("BMRB ID:", sf.bmrbid)
    # print("Parentdir:", parentdir)
    # print("Subdir:", subdir)
    # print("Basename:", fname)

# def convert(from_path, output_dir='converted_files', from_format='nmrstar', to_format='json', output_dir_compression=''):
#     file_extension = {'json': '.json',
#                       'nmrstar': '.txt'}
#
#     if not os.path.exists(output_dir):
#         os.makedirs(output_dir)
#
#     for sf in nmrstarlib.from_whatever(from_path):
#         if not output_dir_compression:
#             with open(os.path.join(output_dir, sf.bmrbid + file_extension[to_format]), 'w') as outfile:
#                 outfile.write(sf.writestr(to_format))
#         elif output_dir_compression == 'zip':
#             with zipfile.ZipFile(output_dir + '.' + output_dir_compression, mode='a', compression=zipfile.ZIP_DEFLATED) as outfile:
#                 outfile.writestr(sf.bmrbid + file_extension[to_format], sf.writestr(to_format))









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

