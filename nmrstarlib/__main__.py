#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
nmrstarlib command-line interface

Usage:
    nmrstarlib -h | --help
    nmrstarlib --version
    nmrstarlib convert (<from_path> <to_path>) [--from_format=<format>] [--to_format=<format>] [--bmrb_url=<url>] [--nmrstar_version=<version>] [--verbose]
    nmrstarlib csview <starfile_path> [--amino_acids=<aa>] [--atoms=<at>] [--csview_outfile=<path>] [--csview_format=<format>] [--nmrstar_version=<version>] [--verbose]

Options:
    -h, --help                   Show this screen.
    --version                    Show version.
    --verbose                    Print what files are processing.
    --from_format=<format>       Input file format, available formats: nmrstar, json [default: nmrstar]
    --to_format=<format>         Output file format, available formats: nmrstar, json [default: json]
    --nmrstar_version=<version>  Version of NMR-STAR format to use, available: 3, 2 [default: 3]
    --bmrb_url=<url>             URL to BMRB REST interface [default: http://rest.bmrb.wisc.edu/bmrb/NMR-STAR3/]
    --amino_acids=<aa>           Comma-separated amino acid three-letter codes
    --atoms=<at>                 Comma-separated BMRB atom codes
    --csview_outfile=<path>      Where to save chemical shifts table
    --csview_format=<format>     Format to which save chamical shift table [default: svg]
"""

import docopt

from . import nmrstarlib
from .converter import Converter
from .csviewer import CSViewer
from nmrstarlib import __version__


def main(cmdargs):

    if cmdargs["convert"]:
        nmrstarlib.BMRB_REST = cmdargs["--bmrb_url"]
        nmrstarlib.VERBOSE = cmdargs["--verbose"]
        nmrstarlib.NMRSTAR_VERSION = cmdargs["--nmrstar_version"]

        nmrstarconverter = Converter(from_path=cmdargs["<from_path>"], to_path=cmdargs["<to_path>"],
                                     from_format=cmdargs['--from_format'], to_format=cmdargs["--to_format"])
        nmrstarconverter.convert()

    elif cmdargs["csview"]:
        aminoacids = cmdargs["--amino_acids"].split(",") if cmdargs["--amino_acids"] else []
        atoms = cmdargs["--atoms"].split(",") if cmdargs["--atoms"] else []

        csviewer = CSViewer(from_path=cmdargs["<starfile_path>"], amino_acids=aminoacids, atoms=atoms,
                            filename=cmdargs["--csview_outfile"], csview_format=cmdargs["--csview_format"])
        csviewer.csview(view=True)


args = docopt.docopt(__doc__, version=__version__)
main(args)
