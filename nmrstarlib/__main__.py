#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
nmrstarlib command-line interface

Usage:
    nmrstarlib -h | --help
    nmrstarlib --version
    nmrstarlib convert (<from_path> <to_path>) [--from_format=<format>] [--to_format=<format>] [--bmrb_url=<url>]
    nmrstarlib csview <starfile_path> [--aminoacids=<aa>] [--atoms=<at>] [--csview_outfile=<path>] [--csview_format=<format>]

Options:
    -h, --help                   Show this screen.
    --version                    Show version.
    --from_format=<format>       Input file format, available formats: nmrstar, json [default: nmrstar]
    --to_format=<format>         Output file format, available formats: nmrstar, json [default: json]
    --bmrb_url=<url>             URL to BMRB REST interface [default: http://rest.bmrb.wisc.edu/bmrb/NMR-STAR3/]
    --aminoacids=<aa>            Comma-separated amino acid three-letter codes
    --atoms=<at>                 Comma-separated BMRB atom codes
    --csview_outfile=<path>      Where to save chemical shifts table
    --csview_format=<format>     Format to which save chamical shift table [default: svg]
"""

import docopt
from . import nmrstarlib
from .converter import Converter
from .csviewer import csviewer

def main(args):

    if args['convert']:
        nmrstarlib.BMRB_REST = args['--bmrb_url']
        nmrstarconverter = Converter(from_path=args['<from_path>'], to_path=args['<to_path>'],
                                     from_format=args['--from_format'], to_format=args['--to_format'])
        nmrstarconverter.convert()

    elif args['csview']:
        aminoacids = args['--aminoacids'].split(',') if args['--aminoacids'] else []
        atoms = args['--atoms'].split(',') if args['--atoms'] else []
        csviewer(from_path=args['<starfile_path>'], aminoacids=aminoacids, atoms=atoms,
                 filename=args['--csview_outfile'], format=args['--csview_format'], view=True)

args = docopt.docopt(__doc__)
main(args)


#
# import sys
# script = sys.argv[0]
# sources = sys.argv[1:]
#
# for sf in nmrstarlib.read_files(sources):
#     print("BMRB ID:", sf.bmrbid)
#     chains = sf.chem_shifts_by_residue(aminoacids=['MET', "SER"], atoms=['CA', 'CB'])
#     for csdict in chains:
#         print(type(csdict))
#         for k, v in csdict.items():
#             print(k, ":", v)

    # import json
    # with open('byresdict.json', 'w') as outfile:
    #     json.dump(d, outfile, indent=4)
#     print("Saveframes:", dict(sf).keys(), '\n\n')


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
#     nmrstar_extension = {'json': '.json',
#                       'nmrstar': '.txt'}
#
#     if not os.path.exists(output_dir):
#         os.makedirs(output_dir)
#
#     for sf in nmrstarlib.from_whatever(from_path):
#         if not output_dir_compression:
#             with open(os.path.join(output_dir, sf.bmrbid + nmrstar_extension[to_format]), 'w') as outfile:
#                 outfile.write(sf.writestr(to_format))
#         elif output_dir_compression == 'zip':
#             with zipfile.ZipFile(output_dir + '.' + output_dir_compression, mode='a', compression=zipfile.ZIP_DEFLATED) as outfile:
#                 outfile.writestr(sf.bmrbid + nmrstar_extension[to_format], sf.writestr(to_format))









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

