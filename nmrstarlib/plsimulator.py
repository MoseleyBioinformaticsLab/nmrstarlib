#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
nmrstarlib.plsimulator
~~~~~~~~~~~~~~~~~~~~~~

This module provides interface classes necessary to create simulated peak list file.
"""

import json
import re
from itertools import product

from . import nmrstarlib


class DimensionComponent(object):
    """Dimensions component interface."""

    def __init__(self, label, position):
        """Dimension component.

        :param str label: Label of a dimension.
        :param int position: Position of dimensions within a peak according to sequence site position, e.g. -1, 0, or +1.
        """
        self.label = label
        self.position = position


class DimensionGroup(DimensionComponent):
    """Composite dimension group."""

    def __init__(self, label, position):
        """Dimension group.

        :param str label: Label of a dimension.
        :param int position: Position of dimensions within a peak according to sequence site position, e.g. -1, 0, or +1.
        """
        super(DimensionGroup, self).__init__(label, position)
        self.dimensions = []


class Dimension(DimensionComponent):
    """Concrete dimension."""

    def __init__(self, label, position, assignment=None, chemshift=None):
        """Concrete dimension intializer.

        :param str label: Label of a dimension.
        :param int position: Position of dimensions within a peak according to sequence site position, e.g. -1, 0, or +1.
        :param str assignment: Chemical shift assignment of a dimension.
        :param float chemshift: Chemical shift value of a dimension.
        """
        super(Dimension, self).__init__(label, position)
        self.assignment = assignment
        self.chemshift = chemshift


class Peak(list):
    """Peak within a peak list."""

    def __init__(self, labels):
        """Peak initializer.

        :param tuple labels: Dimension labels of peak.
        """
        super(Peak, self).__init__()
        self.labels = labels

    @property
    def assignments_list(self):
        """List of assignments per each dimension within a peak.

        :return: List of assignments.
        :rtype: :py:class:`list`
        """
        return [dim.assignment for dim in self]

    @property
    def chemshifts_list(self):
        """List of chemical shift values per each dimensions within a peak.

        :return: List of chemical shifts.
        :rtype: :py:class:`list`
        """
        return [dim.chemshift for dim in self]

    def apply_noise(self, noise_generator, split_idx):
        """Apply noise to dimensions within a peak.

        :param noise_generator: Noise generator object.
        :param int split_idx: Index specifying which peak list split parameters to use.
        :return: None
        :rtype: :py:obj:`None`
        """
        noise = noise_generator.generate(self.labels, split_idx)
        for dim, noise_value in zip(self, noise):
            dim.chemshift += noise_value


class PeakList(list):
    """Peak list contains chemical shift values and assignment information for each peak."""

    def __init__(self, spectrum_name, labels, source, chain_idx):
        """Peak list initializer.

        :param str spectrum_name: Spectrum name from which peak list will be simulated.
        :param list labels: Sequence of labels as they appear in a peak.
        :param str source: :class:`~nmrstarlib.nmrstarlib.StarFile` source.
        :param int chain_idx: :class:`~nmrstarlib.nmrstarlib.StarFile` chain index.
        """
        super(PeakList, self).__init__()
        self.spectrum_name = spectrum_name
        self.labels = labels
        self.source = "{}_{}_{}".format(source, spectrum_name, chain_idx)

    def _to_sparky(self):
        """Save :class:`~nmrstarlib.plsimulator.PeakList` into Sparky-formatted string.

        :return: Peak list representation in Sparky format.
        :rtype: :py:class:`str`
        """
        sparky_str = "Assignment\t\t{}\n\n".format("\t\t".join(["w" + str(i + 1) for i in range(len(self.labels))]))
        for peak in self:
            assignment_str = "-".join(peak.assignments_list)
            dimensions_str = "\t\t".join([str(chemshift) for chemshift in peak.chemshifts_list])
            sparky_str += ("{}\t\t{}\n".format(assignment_str, dimensions_str))
        return sparky_str

    def _to_autoassign(self):
        """Save :class:`~nmrstarlib.plsimulator.PeakList` into AutoAssign-formatted string.

        :return: Peak list representation in AutoAssign format.
        :rtype: :py:class:`str`
        """
        autoassign_str = "#Index\t\t{}\t\tIntensity\t\tWorkbook\n".format(
            "\t\t".join([str(i + 1) + "Dim" for i in range(len(self.labels))]))
        for peak_idx,  peak in enumerate(self):
            dimensions_str = "\t\t".join([str(chemshift) for chemshift in peak.chemshifts_list])
            autoassign_str += "{}\t\t{}\t\t{}\t\t{}\n".format(peak_idx+1, dimensions_str, 0, self.spectrum_name)
        return autoassign_str

    def _to_json(self):
        """Save :class:`~nmrstarlib.plsimulator.PeakList` into JSON string.

        :return: Peak list representation in JSON format.
        :rtype: :py:class:`str`
        """
        json_list = [{"Assignment": peak.assignments_list, "Dimensions": peak.chemshifts_list} for peak in self]
        return json.dumps(json_list, sort_keys=True, indent=4)

    def write(self, filehandle, fileformat):
        """Write :class:`~nmrstarlib.plsimulator.PeakList` data into file.

        :param filehandle: file-like object.
        :type filehandle: :py:class:`io.TextIOWrapper`
        :param str fileformat: Format to use to write data: `nmrstar` or `json`.
        :return: None
        :rtype: :py:obj:`None`
        """
        try:
            if fileformat == "sparky":
                sparky_str = self._to_sparky()
                filehandle.write(sparky_str)
            elif fileformat == "autoassign":
                autoassign_str = self._to_sparky()
                filehandle.write(autoassign_str)
            elif fileformat == "json":
                json_str = self._to_json()
                filehandle.write(json_str)
            else:
                raise TypeError("Unknown file format.")
        except IOError:
            raise IOError('"filehandle" parameter must be writable.')
        filehandle.close()

    def writestr(self, fileformat):
        """Write :class:`~nmrstarlib.plsimulator.PeakList` data into string.

        :param str fileformat: Format to use to write data: `nmrstar` or `json`.
        :return: String representing the :class:`~nmrstarlib.plsimulator.PeakList` instance.
        :rtype: :py:class:`str`
        """
        try:
            if fileformat == "sparky":
                sparky_str = self._to_sparky()
                return sparky_str
            elif fileformat == "autoassign":
                autoassign_str = self._to_autoassign()
                return autoassign_str
            elif fileformat == "json":
                json_str = self._to_json()
                return json_str
            else:
                raise TypeError("Unknown file format.")
        except IOError:
            raise IOError('"filehandle" parameter must be writable.')


class SpinSystem(list):
    """Spin system - collection of related resonances associated with specific atoms in a molecule."""

    def __init__(self):
        """Spin system initializer."""
        super(SpinSystem, self).__init__()


class SequenceSite(list):
    """Sequence site."""

    def __init__(self, residues):
        """Sequence site initializer."""
        super(SequenceSite, self).__init__(residues)

    def is_sequential(self):
        """Check if residues that sequence site is composed of are in sequential order.

        :return: If sequence site is in valid sequential order (True) or not (False).
        :rtype: :py:obj:`True` or :py:obj:`False`
        """
        seq_ids = tuple(int(residue["Seq_ID"]) for residue in self)
        return seq_ids == tuple(range(int(seq_ids[0]), int(seq_ids[-1])+1))


class PeakTemplate(list):
    """Peak templates defined as a list of concrete dimensions."""

    def __init__(self, dimensions):
        """Peak template initializer."""
        super(PeakTemplate, self).__init__(dimensions)

    @property
    def dimension_labels(self):
        """List of dimension labels.

        :return: List of dimension labels of a peak template.
        :rtype: :py:class:`list`
        """
        return [dim.label for dim in self]

    @property
    def dimension_positions(self):
        """List of dimension positions.

        :return: List of dimension positions of a peak template.
        :rtype: :py:class:`list`
        """
        return [dim.position for dim in self]


class PeakDescription(list):
    """Peak descriptions defined as list of general dimension groups."""

    dim_pattern = re.compile("(\w+)([+-]?\d)?")

    def __init__(self, fraction, dimension_labels):
        """Peak description initializer.

        :param float fraction: Describes expected number of peaks.
        :param dimension_labels: List of dimension labels.
        """
        self.fraction = fraction
        self.relative_positions = []
        dimensions = []

        for label in dimension_labels:
            dim_label, position = re.match(self.dim_pattern, label).groups()
            if position:
                self.relative_positions.append(int(position))
            else:
                self.relative_positions.append(0)
            dimensions.append(dim_label)

        if all(position <= 0 for position in self.relative_positions):
            seq_site_positions = [position + abs(min(self.relative_positions)) for position in self.relative_positions]
        elif all(position >= 0 for position in self.relative_positions):
            seq_site_positions = self.relative_positions
        else:
            # TODO: take min and max and detemine window size
            raise NotImplementedError

        dimension_groups = self.create_dimension_groups(zip(dimensions, seq_site_positions))
        super(PeakDescription, self).__init__(dimension_groups)

    @staticmethod
    def create_dimension_groups(dimension_positions):
        """Create list of dimension groups.

        :param zip dimension_positions: List of tuples describing dimension and its position within sequence site.
        :return: List of dimension groups.
        :rtype: :py:class:`list`
        """
        dimension_groups = []
        for dim_group_label, position in dimension_positions:
            dim_group = DimensionGroup(dim_group_label, position)

            for dim_label in nmrstarlib.RESONANCE_CLASSES[dim_group_label]:
                dim_group.dimensions.append(Dimension(dim_label, position))
            dimension_groups.append(dim_group)

        return dimension_groups


class Spectrum(list):
    """Spectrum object described as a list of general peak descriptions."""

    def __init__(self, name, labels, min_spin_system_peaks, amino_acids_and_atoms=None):
        """Spectrum initializer.

        :param str name: Spectrum name.
        :param labels: Sequence of dimension labels as they appear in a peak.
        :param int min_spin_system_peaks: Minimum number of peaks per spin system.
        """
        super(Spectrum, self).__init__()
        self.name = name
        self.labels = labels
        self.min_spin_system_peaks = min_spin_system_peaks
        self.amino_acids_and_atoms = amino_acids_and_atoms


    @property
    def peak_templates(self):
        """Create a list of concrete peak templates from a list of general peak descriptions.

        :return: List of peak templates.
        :rtype: :py:class:`list`
        """
        peak_templates = []
        for peak_descr in self:
            expanded_dims = [dim_group.dimensions for dim_group in peak_descr]
            templates = product(*expanded_dims)
            for template in templates:
                peak_templates.append(PeakTemplate(template))
        return peak_templates

    @property
    def seq_site_length(self):
        """Calculate length of a single sequence site based upon relative positions specified in peak descriptions.

        :return: Length of sequence site.
        :rtype: :py:class:`int`
        """
        relative_positions_set = set()
        for peak_descr in self:
            relative_positions_set.update(peak_descr.relative_positions)
        return len(relative_positions_set)
