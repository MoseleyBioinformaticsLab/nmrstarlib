#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
nmrstarlib.csviewer
~~~~~~~~~~~~~~~~~~~

This module provides the :func:`~nmrstarlib.csviewer.csviewer` function - Chemical Shifts Viewer
that visualizes chemical shifts values.
"""

from graphviz import Source
from . import nmrstarlib


def csviewer(from_path, aminoacids=None, atoms=None, filename=None, format='svg', view=False):
    """Chemical Shifts Viewer: uses :meth:`nmrstarlib.nmrstarlib.StarFile.chem_shifts_by_residue`
    method chemical shifts organized by residue and visualizes chemical shifts values using the
    Graphviz (http://www.graphviz.org/) DOT Languge description.

    :param str from_path: Path to single NMR-STAR file or BMRB id.
    :param list aminoacids: List of atom types, e.g. 'ALA', 'GLY', 'SER', etc. Leave as `None` to include everything.
    :param list atoms: List of atom types, e.g. 'CA', 'CB', 'HA', etc. Leave as `None` to include everything.
    :param str filename: Output filename chemical shifts graph to be saved.
    :param str format: `svg`, `png`, `pdf`. See http://www.graphviz.org/doc/info/output.html for all available formats.
    :param bool view: Open in default image viewer or save file in current working directory quietly.
    :return: None
    :rtype: None
    """
    dot_template = """digraph {{
        compound=true
        fontname="Inconsolata, Consolas"
        fontsize=10
        margin="0,0"
        ranksep=0.2
        rankdir=LR
        penwidth=0.5

        node [fontname="Inconsolata, Consolas", fontsize=10, penwidth=0.5]
        edge [fontname="Inconsolata, Consolas", fontsize=10]

        subgraph cluster1 {{
            margin="10,10"
            labeljust="left"
            node [shape=Mrecord, style=filled, colorscheme=spectral11]

            {{
    {}
            }}

            edge [arrowhead=none]
    {}
        }}
    }}
    """
    for starfile in nmrstarlib.read_files([from_path]):
        chains = starfile.chem_shifts_by_residue(aminoacids, atoms)
        for idx, chemshifts_dict in enumerate(chains):
            nodes = []
            edges = []

            for aminoacid in chemshifts_dict:
                aaname = '{}_{}'.format(aminoacid[1], aminoacid[0])
                label = '"{{{}|{}}}"'.format(aminoacid[0], aminoacid[1])
                color = 8
                aanode_entry = "            {} [label={}, fillcolor={}]".format(aaname, label, color)
                nodes.append(aanode_entry)
                currnodename = aaname

                for atomtype in chemshifts_dict[aminoacid]:
                    atname = "{}_{}".format(aaname, atomtype)
                    label = '"{{{}|{}}}"'.format(atomtype, chemshifts_dict[aminoacid][atomtype])
                    if atomtype.startswith("H"):
                        color = 4
                    elif atomtype.startswith("C"):
                        color = 6
                    elif atomtype.startswith("N"):
                        color = 10
                    else:
                        color = 8
                    atnode_entry = "{} [label={}, fillcolor={}]".format(atname, label, color)
                    nextnodename = atname
                    nodes.append(atnode_entry)
                    edges.append("{} -> {}".format(currnodename, nextnodename))
                    currnodename = nextnodename

            if filename is None:
                filename = "{}_{}".format(starfile.bmrbid, idx)
            else:
                filename = "{}_{}".format(filename, idx)

            src = Source(dot_template.format("\n".join(nodes), "\n".join(edges)), format=format)
            src.render(filename=filename, view=view)
