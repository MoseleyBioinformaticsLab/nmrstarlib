#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
nmrstarlib.csviewer
~~~~~~~~~~~~~~~~~~~

This module provides the :class:`~nmrstarlib.csviewer.CSViewer` class - Chemical Shifts Viewer
that visualizes chemical shifts values.
"""

from graphviz import Source
from . import fileio

class CSViewer(object):
    """Chemical Shifts Viewer uses :meth:`~nmrstarlib.nmrstarlib.StarFile.chem_shifts_by_residue`
    method to get chemical shifts organized by residue and visualizes chemical shifts values using the
    Graphviz (http://www.graphviz.org/) DOT Languge description.
    """
    dot_template = '''digraph {{
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
    '''

    def __init__(self, from_path, amino_acids=None, atoms=None, amino_acids_and_atoms=None, filename=None, csview_format="svg", nmrstar_version="3"):
        """CSViewer initializer.

        :param str from_path: Path to single NMR-STAR file or BMRB id.
        :param amino_acids: Sequence of amino acids three letter codes, e.g. 'ALA', 'GLY', 'SER', etc. Leave as `None` to include everything.
        :type amino_acids: :py:class:`list` or :py:class:`tuple`
        :param atoms: Sequence of atom types, e.g. 'CA', 'CB', 'HA', etc. Leave as `None` to include everything.
        :type atoms: :py:class:`list` or :py:class:`tuple`
        :param dict amino_acids_and_atoms: Amino acid and its atoms key-value pairs.
        :param str filename: Output filename chemical shifts graph to be saved.
        :param str csview_format: `svg`, `png`, `pdf`. See http://www.graphviz.org/doc/info/output.html for all available formats.
        :param str nmrstar_version: Version of NMR-STAR format to use for look up chemichal shifts loop.
        :return: None
        :rtype: :py:obj:`None`
        """
        self.from_path = from_path
        self.amino_acids = amino_acids
        self.atoms = atoms
        self.amino_acids_and_atoms = amino_acids_and_atoms
        self.filename = filename
        self.csview_format = csview_format
        self.nmrstar_version = nmrstar_version

    def csview(self, view=False):
        """View chemical shift values organized by amino acid residue.

        :param view: Open in default image viewer or save file in current working directory quietly.
        :type view: :py:obj:`True` or :py:obj:`False`
        :return: None
        :rtype: :py:obj:`None`
        """
        for starfile in fileio.read_files(self.from_path):
            chains = starfile.chem_shifts_by_residue(amino_acids=self.amino_acids,
                                                     atoms=self.atoms,
                                                     amino_acids_and_atoms=self.amino_acids_and_atoms,
                                                     nmrstar_version=self.nmrstar_version)

            for idx, chemshifts_dict in enumerate(chains):
                nodes = []
                edges = []

                for seq_id in chemshifts_dict:
                    aaname = "{}_{}".format(chemshifts_dict[seq_id]["AA3Code"], seq_id)
                    label = '"{{{}|{}}}"'.format(seq_id, chemshifts_dict[seq_id]["AA3Code"])
                    color = 8
                    aanode_entry = "            {} [label={}, fillcolor={}]".format(aaname, label, color)
                    nodes.append(aanode_entry)
                    currnodename = aaname

                    for atom_type in chemshifts_dict[seq_id]:
                        if atom_type in ["AA3Code", "Seq_ID"]:
                            continue
                        else:
                            atname = "{}_{}".format(aaname, atom_type)
                            label = '"{{{}|{}}}"'.format(atom_type, chemshifts_dict[seq_id][atom_type])
                            if atom_type.startswith("H"):
                                color = 4
                            elif atom_type.startswith("C"):
                                color = 6
                            elif atom_type.startswith("N"):
                                color = 10
                            else:
                                color = 8
                            atnode_entry = "{} [label={}, fillcolor={}]".format(atname, label, color)
                            nextnodename = atname
                            nodes.append(atnode_entry)
                            edges.append("{} -> {}".format(currnodename, nextnodename))
                            currnodename = nextnodename

                if self.filename is None:
                    filename = "{}_{}".format(starfile.bmrbid, idx)
                else:
                    filename = "{}_{}".format(self.filename, idx)

                src = Source(self.dot_template.format("\n".join(nodes), "\n".join(edges)), format=self.csview_format)
                src.render(filename=filename, view=view)
