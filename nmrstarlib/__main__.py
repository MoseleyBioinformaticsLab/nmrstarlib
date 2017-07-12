#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
nmrstarlib command-line interface

Usage:
    nmrstarlib -h | --help
    nmrstarlib --version
    nmrstarlib convert (<from_path> <to_path>) [--from_format=<format>] [--to_format=<format>] [--bmrb_url=<url>] [--nmrstar_version=<version>] [--verbose]
    nmrstarlib csview <starfile_path> [--amino_acids=<aa>] [--atoms=<at>] [--csview_outfile=<path>] [--csview_format=<format>] [--bmrb_url=<url>] [--nmrstar_version=<version>] [--verbose]
    nmrstarlib plsimulate (<from_path> <to_path> <spectrum>) [--from_format=<format>] [--to_format=<format>] [--plsplit=<%>] [--distribution=<func>] [--H=<value>] [--C=<value>] [--N=<value>] [--bmrb_url=<url>] [--nmrstar_version=<version>] [--spectrum_descriptions=<path>] [--verbose]

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
    --spectrum_descriptions=<path>  Path to custom spectrum descriptions file.
    --distribution=<func>           Statistical distribution function [default: normal].
    --H=<value>                     Statistical distribution parameter(s) for H dimension.
    --C=<value>                     Statistical distribution parameter(s) for C dimension.
    --N=<value>                     Statistical distribution parameter(s) for N dimension.
"""

import itertools
import collections
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
        distribution_name = cmdargs["--distribution"]
        distribution_parameter_names = noise.distributions[distribution_name]["parameters"]

        if not distribution_parameter_names:
            parameters = None
        else:
            parameters = collections.defaultdict(list)

            for dim in ("H", "N", "C"):
                params = cmdargs["--{}".format(dim)]
                if params is None:
                    for param_name in distribution_parameter_names:
                        parameters["{}_{}".format(dim, param_name)].append(None)
                else:
                    params = params.split(",")
                    if len(params) > len(distribution_parameter_names):
                        raise ValueError("Inconsistent number of parameters provided.")

                    for param, param_name in zip(params, distribution_parameter_names):
                        parameters["{}_{}".format(dim, param_name)].extend([float(val) if val else None for val in param.split(":")])

            # fill with None values for parameters that have missing values
            for param_name, param_values in parameters.items():
                given_values = list(param_values)
                missing_values = [None for _ in range(len(plsplit) - len(param_values))]
                param_values = given_values + missing_values
                parameters[param_name] = tuple(param_values)

        noise_generator = noise.NoiseGenerator(parameters=parameters, distribution_name=distribution_name)

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
