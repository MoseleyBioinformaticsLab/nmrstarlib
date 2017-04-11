#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
nmrstarlib.translator
~~~~~~~~~~~~~~~~~~~~~

This module provides the :class:`~nmrstarlib.translator.Translator` abstract class
and concrete classes: :class:`~nmrstarlib.translator.StarFileToStarFile` for converting between
NMR-STAR and JSONized NMR-STAR formats and :class:`~nmrstarlib.translator.StarFileToPeakList`
for converting NMR-STAR formatted file into simulated peak list file.
"""

import itertools

from . import nmrstarlib
from . import plsimulator


class Translator(object):
    """Translator abstract class."""

    def __init__(self, from_path, to_path, from_format=None, to_format=None):
        """Translator initializer.

        :param str from_path: Path to input file(s).
        :param str to_path: Path to output file(s).
        :param str from_format: Input format.
        :param str to_format: Output format.
        """
        self.from_path = from_path
        self.to_path = to_path
        self.from_format = from_format
        self.to_format = to_format
        self.from_path_compression = nmrstarlib.GenericFilePath.is_compressed(from_path)
        self.to_path_compression = nmrstarlib.GenericFilePath.is_compressed(to_path)

    def __iter__(self):
        """Abstract iterator must be implemented in a subclass."""
        raise NotImplementedError()


class StarFileToStarFile(Translator):
    """Translator concrete class that can convert between NMR-STAR and JSONized NMR-STAR formats."""

    file_extension = {"json": ".json",
                      "nmrstar": ".str"}

    def __init__(self, from_path, to_path, from_format=None, to_format=None):
        """StarFileToStarFile translator initializer.

        :param str from_path: Path to input file(s).
        :param str to_path: Path to output file(s).
        :param str from_format: Input format: `nmrstar` or `json`.
        :param str to_format: Output format: `nmrstar` or `json`.
        """
        super(StarFileToStarFile, self).__init__(from_path, to_path, from_format, to_format)

    def __iter__(self):
        """Iterator that yields instances of :class:`~nmrstarlib.nmrstarlib.StarFile` instances.

        :return: instance of :class:`~nmrstarlib.nmrstarlib.StarFile` object instance.
        :rtype: :class:`~nmrstarlib.nmrstarlib.StarFile`
        """
        for starfile in nmrstarlib.read_files(self.from_path):
            yield starfile


class StarFileToPeakList(Translator):
    """Translator concrete class that can convert NMR-STAR of JSONized NMR-STAR formatted file
    into peak list file."""

    file_extension = {"json": ".json",
                      "sparky": ".txt",
                      "autoassign": ".pks"}

    def __init__(self, from_path, to_path, from_format, to_format, spectrum_name, plsplit=None, noise_generator=None):
        """StarFileToPeakList initializer.

        :param str from_path: Path to input file(s).
        :param str to_path: Path to output file(s).
        :param str from_format: Input format: `nmrstar` or `json`.
        :param str to_format: Output format: `json` or `sparky`.
        :param str spectrum_name: Name of spectrum from which to simulate peak list.
        :param tuple plsplit: How to split peak list in order to account for multiple sources of variance.
        :param noise_generator: Subclasses of :class:`~nmrstarlib.noise.NoiseGenerator` object.
        :type noise_generator: :class:`~nmrstarlib.noise.NoiseGenerator`
        """
        super(StarFileToPeakList, self).__init__(from_path, to_path, from_format, to_format)

        if plsplit is None:
            plsplit = (100,)

        if all(0 <= i <= 1 for i in plsplit):
            plsplit = tuple(i*100 for i in plsplit)
        elif all(0 <= i <= 100 for i in plsplit):
            plsplit = tuple(i for i in plsplit)
        else:
            raise ValueError("All percentages must be in interval from 0 to 1 or from 0 % to 100 %.")

        if sum(plsplit) == 100:
            pass
        else:
            raise ValueError('"plsplit" percentages must sum up to 100%, current sum is {}%'.format(sum(plsplit)))

        if noise_generator is not None:
            for param_name, param_values in noise_generator.parameters.items():
                if len(param_values) == len(plsplit):
                    continue
                else:
                    raise ValueError('Length of noise values of "{}" parameter must be equal to length of peak list split.'.format(param_name))

        self.plsplit = plsplit
        self.noise_generator = noise_generator
        self.spectrum = self.create_spectrum(spectrum_name)

    @staticmethod
    def create_spectrum(spectrum_name):
        """Initialize spectrum and peak descriptions.

        :param str spectrum_name: Name of the spectrum from which peak list will be simulated.
        :return: Spectrum object.
        :rtype: :class:`~nmrstarlib.plsimulator.Spectrum`
        """
        try:
            spectrum_description = nmrstarlib.SPECTRUM_DESCRIPTIONS[spectrum_name]
        except KeyError:
            raise NotImplementedError("Experiment type is not defined.")

        spectrum = plsimulator.Spectrum(spectrum_name, spectrum_description["Labels"],
                                        spectrum_description["MinNumberPeaksPerSpinSystem"],
                                        spectrum_description.get("ResonanceLimit", None))

        for peak_descr in spectrum_description["PeakDescriptions"]:
            spectrum.append(plsimulator.PeakDescription(peak_descr["fraction"], peak_descr["dimensions"]))

        return spectrum

    @staticmethod
    def create_sequence_sites(chain, seq_site_length):
        """Create sequence sites using sequence ids.

        :param dict chain: Chain object that contains chemical shift values and assignment information.
        :param int seq_site_length: Length of a single sequence site.
        :return: List of sequence sites.
        :rtype: :py:class:`list`
        """
        seq_ids = sorted(list(chain.keys()))  # make sure that sequence is sorted by sequence id
        slices = [itertools.islice(seq_ids, i, None) for i in range(seq_site_length)]
        seq_site_ids = list(zip(*slices))

        sequence_sites = []
        for seq_site_id in seq_site_ids:
            seq_site = plsimulator.SequenceSite(chain[seq_id] for seq_id in seq_site_id)
            if seq_site.is_sequential():
                sequence_sites.append(seq_site)
            else:
                continue

        return sequence_sites

    @staticmethod
    def calculate_intervals(chunk_sizes):
        """Calculate intervals for a given chunk sizes.

        :param list chunk_sizes: List of chunk sizes.
        :return: Tuple of intervals.
        :rtype: :py:class:`tuple`
        """
        start_indexes = [sum(chunk_sizes[:i]) for i in range(0, len(chunk_sizes))]
        end_indexes = [sum(chunk_sizes[:i+1]) for i in range(0, len(chunk_sizes))]
        return tuple(zip(start_indexes, end_indexes))

    def split_by_percent(self, spin_systems_list):
        """Split list of spin systems by specified percentages.

        :param list spin_systems_list: List of spin systems.
        :return: List of spin systems divided into sub-lists corresponding to specified split percentages.
        :rtype: :py:class:`list`
        """
        chunk_sizes = [int((i*len(spin_systems_list))/100) for i in self.plsplit]
        if sum(chunk_sizes) < len(spin_systems_list):
            difference = len(spin_systems_list) - sum(chunk_sizes)
            chunk_sizes[chunk_sizes.index(min(chunk_sizes))] += difference

        assert sum(chunk_sizes) == len(spin_systems_list), \
            "sum of chunk sizes must be equal to spin systems list length."

        intervals = self.calculate_intervals(chunk_sizes)
        chunks_of_spin_systems_by_percentage = [itertools.islice(spin_systems_list, *interval) for interval in intervals]
        return chunks_of_spin_systems_by_percentage

    def create_peaklist(self, spectrum, chain, chain_idx, source):
        """Create peak list file.

        :param spectrum: Spectrum object instance.
        :type spectrum: :class:`~nmrstarlib.plsimulator.Spectrum`
        :param dict chain: Chain object that contains chemical shift values and assignment information.
        :param int chain_idx: Protein chain index.
        :param str source: :class:`~nmrstarlib.nmrstarlib.StarFile` source.
        :return: Peak list object.
        :rtype: :class:`~nmrstarlib.plsimulator.PeakList`
        """
        sequence_sites = self.create_sequence_sites(chain, spectrum.seq_site_length)
        spin_systems = []
        peaklist = plsimulator.PeakList(spectrum.name, spectrum.labels, source, chain_idx)

        for seq_site in sequence_sites:
            spin_system = plsimulator.SpinSystem()
            for template in spectrum.peak_templates:
                peak = plsimulator.Peak(template.dimension_labels)
                for dim in template:
                    chemshift = seq_site[dim.position].get(dim.label, None)
                    assignment = "{}{}{}".format(seq_site[dim.position]["AA3Code"],
                                                 seq_site[dim.position]["Seq_ID"],
                                                 dim.label)
                    if chemshift and assignment:
                        peak_dim = plsimulator.Dimension(dim.label, dim.position, assignment, float(chemshift))
                        peak.append(peak_dim)
                    else:
                        continue

                if len(peak) == len(template):
                    spin_system.append(peak)
                    peaklist.append(peak)
                else:
                    continue

            spin_systems.append(spin_system)

        if all(len(i) < spectrum.min_spin_system_peaks for i in spin_systems):
            return None

        if self.noise_generator is not None:
            spin_systems_chunks = self.split_by_percent(spin_systems)
            for split_idx, chunk in enumerate(spin_systems_chunks):
                for spin_system in chunk:
                    for peak in spin_system:
                        peak.apply_noise(self.noise_generator, split_idx)

        return peaklist

    def __iter__(self):
        """Iterator that yields instances of :class:`~nmrstarlib.plsimulator.PeakList` instances.

        :return: instance of :class:`~nmrstarlib.plsimulator.PeakList` object instance.
        :rtype: :class:`~nmrstarlib.plsimulator.PeakList`
        """
        for starfile in nmrstarlib.read_files(self.from_path):
            chains = starfile.chem_shifts_by_residue(amino_acids_and_atoms=self.spectrum.amino_acids_and_atoms)

            for chain_idx, chain in enumerate(chains):
                peaklist = self.create_peaklist(self.spectrum, chain, chain_idx, starfile.source)

                if peaklist:
                    yield peaklist
                else:
                    continue
