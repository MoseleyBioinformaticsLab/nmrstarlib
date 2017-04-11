#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
nmrstarlib.noise
~~~~~~~~~~~~~~~~

This module provides the :class:`~nmrstarlib.noise.NoiseGenerator`
abstract class and :class:`~nmrstarlib.noise.RandomNormalNoiseGenerator`
for adding noise values to :class:`~nmrstarlib.plsimulator.Peak`
dimensions within a :class:`~nmrstarlib.plsimulator.PeakList`.
"""

import numpy as np


class NoiseGenerator(object):
    """Noise generator abstract class."""

    def __init__(self, parameters):
        """Noise generator initializer.

        :param parameters: Statistical distribution parameters per each peak list split.
        """
        self.parameters = parameters

    def generate(self, labels, split_idx):
        """Generate peak-specific noise abstract method, must be reimplemented in a subclass.

        :param tuple labels: Dimension labels of a peak.
        :param int split_idx: Index specifying which peak list split parameters to use.
        :return: List of noise values for dimensions ordered as they appear in a peak.
        :rtype: :py:class:`list`
        """
        raise NotImplementedError()


class RandomNormalNoiseGenerator(NoiseGenerator):
    """Random normal noise generator concrete class."""

    def __init__(self, parameters):
        """Random normal noise generator initializer.

        :param parameters: Statistical distribution parameters from random normal distribution per each peak list split.
        """
        super(RandomNormalNoiseGenerator, self).__init__(parameters)
        self.parameters_per_split = list(map(dict, zip(*[[(k, v) for v in value] for k, value in parameters.items()])))

    def generate(self, labels, split_idx):
        """Generate peak-specific random noise from normal distribution.

        :param tuple labels: Dimension labels of a peak.
        :param int split_idx: Index specifying which peak list split parameters to use.
        :return: List of noise values for dimensions ordered as they appear in a peak.
        :rtype: :py:class:`list`
        """
        atom_labels = [label[0] for label in labels]
        mean_values = [self.parameters_per_split[split_idx]["{}_{}".format(label, "mean")] for label in atom_labels]
        std_values = [self.parameters_per_split[split_idx]["{}_{}".format(label, "std")] for label in atom_labels]
        noise = [np.random.normal(mean, std) if std > 0 else 0.0 for mean, std in zip(mean_values, std_values)]
        return noise
