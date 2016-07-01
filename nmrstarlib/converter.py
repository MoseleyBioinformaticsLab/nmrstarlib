#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Usage:
    converter.py -h | --help
    converter.py --version
    converter.py (<from_path> <to_path>)
    converter.py (<from_path> <to_path>) [--from_format=format] [--to_format=format]

Options:
    -h, --help             Show this screen.
    --version              Show version.
    --from_format=format   Input file format [default: nmrstar]
    --to_format=format     Output file format [default: json]


"""

import os
import io
import zipfile
import tarfile
import bz2
import gzip
from pathlib import Path

from . import docopt
from . import nmrstarlib


def main(args):
    nmrstarconverter = Converter(from_path=args['<from_path>'], to_path=args['<to_path>'],
                                 from_format=args['--from_format'], to_format=args['--to_format'])
    nmrstarconverter.convert()


class Converter(object):
    """Converter class to convert BMRB NMR-STAR files from nmrstar to json or from json to nmrstar."""

    nmrstar_extension = {'json':    '.json',
                         'nmrstar': '.txt'}

    def __init__(self, from_path, to_path, from_format='nmrstar', to_format='json'):
        self.from_path = from_path
        self.to_path = to_path
        self.from_format = from_format
        self.to_format = to_format

        self.from_path_compression = nmrstarlib.GenericFilePath.is_compressed(from_path)
        self.to_path_compression = nmrstarlib.GenericFilePath.is_compressed(to_path)

    def convert(self):
        if not os.path.exists(os.path.dirname(self.to_path)):
            os.makedirs(os.path.dirname(self.to_path))

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
        if not self.to_path_compression:
            self._to_dir()
        elif self.to_path_compression == 'zip':
            self._to_zipfile()
        elif self.to_path_compression in ('tar', 'tar.gz', 'tar.bz2'):
            self._to_tarfile()
        elif self.to_path_compression in ('gz', 'bz2'):
            raise TypeError("Many-to-one conversion, cannot convert {} into {}".format(self.from_path, self.to_path))
        else:
            raise TypeError('Unknown output file format: "{}"'.format(self.to_path))

    def _one_to_one(self):
        if not self.to_path_compression:
            self._to_textfile()
        elif self.to_path_compression == 'gz':
            self._to_gzipfile()
        elif self.to_path_compression == 'bz2':
            self._to_bz2file()
        elif self.to_path_compression in ('tar', 'tar.gz', 'tar.bz2', 'zip'):
            raise TypeError('One-to-many conversion, cannot convert "{}" into "{}"'.format(self.from_path, self.to_path))
        else:
            raise TypeError('Unknown format: "{}"'.format(self.to_path))

    def _to_dir(self):
        for starfile in nmrstarlib.read_files([self.from_path]):
            inpath = Path(starfile.source)
            subdir = os.path.join(*" ".join(inpath.parts[1:-1]).split(" "))
            fname = inpath.name
            outpath = os.path.join(self.to_path, subdir, fname)
            if not os.path.exists(os.path.dirname(outpath)):
                os.makedirs(os.path.dirname(outpath))
            with open(outpath + self.nmrstar_extension[self.to_format], mode='w') as outfile:
                outfile.write(starfile.writestr(self.to_format))

    def _to_zipfile(self):
        with zipfile.ZipFile(self.to_path, mode='w', compression=zipfile.ZIP_DEFLATED) as outfile:
            for starfile in nmrstarlib.read_files([self.from_path]):
                inpath = Path(starfile.source)
                subdir = os.path.join(*" ".join(inpath.parts[1:-1]).split(" "))
                fname = inpath.name
                outpath = os.path.join(subdir, fname)
                outfile.writestr(outpath + self.nmrstar_extension[self.to_format], starfile.writestr(self.to_format))

    def _to_tarfile(self):
        if self.to_path_compression == 'tar':
            tar_mode = 'w'
        elif self.to_path_compression == 'tar.gz':
            tar_mode = 'w:gz'
        elif self.to_path_compression == 'tar.bz2':
            tar_mode = 'w:bz2'
        else:
            tar_mode = 'w'

        with tarfile.open(self.to_path, mode=tar_mode) as outfile:
            for starfile in nmrstarlib.read_files([self.from_path]):
                inpath = Path(starfile.source)
                subdir = os.path.join(*" ".join(inpath.parts[1:-1]).split(" "))
                fname = inpath.name
                outpath = os.path.join(subdir, fname)

                info = tarfile.TarInfo(outpath + self.nmrstar_extension[self.to_format])
                data = starfile.writestr(self.to_format).encode()
                info.size = len(data)
                outfile.addfile(tarinfo=info, fileobj=io.BytesIO(data))

    def _to_bz2file(self):
        with bz2.BZ2File(self.to_path, mode='wb') as outfile:
            for starfile in nmrstarlib.read_files([self.from_path]):
                outfile.write(starfile.writestr(self.to_format).encode())

    def _to_gzipfile(self):
        with gzip.GzipFile(self.to_path, mode='wb') as outfile:
            for starfile in nmrstarlib.read_files([self.from_path]):
                outfile.write(starfile.writestr(self.to_format).encode())

    def _to_textfile(self):
        to_path = self.to_path if self.to_path.endswith(self.nmrstar_extension[self.to_format]) \
                               else self.to_path + self.nmrstar_extension[self.to_format]
        with open(to_path, mode='w') as outfile:
            for starfile in nmrstarlib.read_files([self.from_path]):
                outfile.write(starfile.writestr(self.to_format))

if __name__ == '__main__':
    args = docopt.docopt(__doc__)
    main(args)
