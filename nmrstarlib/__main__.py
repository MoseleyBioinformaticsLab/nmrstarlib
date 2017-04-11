#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
nmrstarlib command-line interface

Usage:
    nmrstarlib -h | --help
    nmrstarlib --version
    nmrstarlib convert (<from_path> <to_path>) [--from_format=<format>] [--to_format=<format>] [--bmrb_url=<url>] [--nmrstar_version=<version>] [--verbose]
    nmrstarlib csview <starfile_path> [--amino_acids=<aa>] [--atoms=<at>] [--csview_outfile=<path>] [--csview_format=<format>] [--bmrb_url=<url>] [--nmrstar_version=<version>] [--verbose]
    nmrstarlib plsimulate (<from_path> <to_path> <spectrum>) [--from_format=<format>] [--to_format=<format>] [--plsplit=<%>] [--H_std=<std>] [--C_std=<std>] [--N_std=<std>] [--H_mean=<mean>] [--C_mean=<mean>] [--N_mean=<mean>] [--bmrb_url=<url>] [--nmrstar_version=<version>] [--spectrum_descriptions=<path>] [--verbose]

Options:
    -h, --help                      Show this screen.
    --version                       Show version.
    --verbose                       Print what files are processing.
    --from_format=<format>          Input file format, available formats: nmrstar, json [default: nmrstar].
    --to_format=<format>            Output file format, available formats: nmrstar, json [default: json].
    --nmrstar_version=<version>     Version of NMR-STAR format to use, available: 2, 3 [default: 3].
    --bmrb_url=<url>                URL to BMRB REST interface [default: http://rest.bmrb.wisc.edu/bmrb/NMR-STAR3/].
    --amino_acids=<aa>              Comma-separated amino acid three-letter codes.
    --atoms=<at>                    Comma-separated BMRB atom codes.
    --csview_outfile=<path>         Where to save chemical shifts table.
    --csview_format=<format>        Format to which save chemical shift table [default: svg].
    --plsplit=<%>                   How to split peak list into chunks by percent [default: 100].
    --H_std=<ppm>                   Standard deviation for H dimensions [default: 0].
    --C_std=<ppm>                   Standard deviation for C dimensions [default: 0].
    --N_std=<ppm>                   Standard deviation for N dimensions [default: 0].
    --H_mean=<ppm>                  Mean for H dimensions [default: 0].
    --C_mean=<ppm>                  Mean for C dimensions [default: 0].
    --N_mean=<ppm>                  Mean for N dimensions [default: 0].
    --spectrum_descriptions=<path>  Path to custom spectrum descriptions file.
"""

import docopt

from . import nmrstarlib
from . import converter
from . import csviewer
from . import noise
from . import translator
from . import __version__


def main(cmdargs):

    nmrstarlib.BMRB_REST = cmdargs["--bmrb_url"]
    nmrstarlib.VERBOSE = cmdargs["--verbose"]
    nmrstarlib.NMRSTAR_VERSION = cmdargs["--nmrstar_version"]

    if cmdargs["convert"]:

        nmrstar_file_translator = translator.StarFileToStarFile(from_path=cmdargs["<from_path>"],
                                                                to_path=cmdargs["<to_path>"],
                                                                from_format=cmdargs["--from_format"],
                                                                to_format=cmdargs["--to_format"])

        nmrstar_converter = converter.Converter(file_generator=nmrstar_file_translator)
        nmrstar_converter.convert()

    elif cmdargs["csview"]:
        aminoacids = cmdargs["--amino_acids"].split(",") if cmdargs["--amino_acids"] else []
        atoms = cmdargs["--atoms"].split(",") if cmdargs["--atoms"] else []

        chemshift_viewer = csviewer.CSViewer(from_path=cmdargs["<starfile_path>"],
                                             amino_acids=aminoacids,
                                             atoms=atoms,
                                             filename=cmdargs["--csview_outfile"],
                                             csview_format=cmdargs["--csview_format"])
        chemshift_viewer.csview(view=True)

    elif cmdargs["plsimulate"]:
        if cmdargs["--spectrum_descriptions"]:
            nmrstarlib.update_constants(spectrum_descriptions_cfg=cmdargs["--spectrum_descriptions"])

        plsplit = tuple(float(i) for i in cmdargs["--plsplit"].split(","))
        parameters = {"H_mean": tuple(float(i) for i in cmdargs["--H_mean"].split(",")),
                      "C_mean": tuple(float(i) for i in cmdargs["--C_mean"].split(",")),
                      "N_mean": tuple(float(i) for i in cmdargs["--N_mean"].split(",")),
                      "H_std": tuple(float(i) for i in cmdargs["--H_std"].split(",")),
                      "C_std": tuple(float(i) for i in cmdargs["--C_std"].split(",")),
                      "N_std": tuple(float(i) for i in cmdargs["--N_std"].split(","))}

        # fill with zeros values for parameters that have missing values
        for param_name, param_values in parameters.items():
            given_values = list(param_values)
            missing_values = [0.0 for _ in range(len(plsplit) - len(param_values))]
            param_values = given_values + missing_values
            parameters[param_name] = tuple(param_values)

        noise_generator = noise.RandomNormalNoiseGenerator(parameters)

        peaklist_file_translator = translator.StarFileToPeakList(from_path=cmdargs["<from_path>"],
                                                                 to_path=cmdargs["<to_path>"],
                                                                 from_format=cmdargs["--from_format"],
                                                                 to_format=cmdargs["--to_format"],
                                                                 spectrum_name=cmdargs["<spectrum>"],
                                                                 plsplit=plsplit,
                                                                 noise_generator=noise_generator)

        nmrstar_to_peaklist_converter = converter.Converter(file_generator=peaklist_file_translator)
        nmrstar_to_peaklist_converter.convert()


args = docopt.docopt(__doc__, version=__version__)
main(args)
