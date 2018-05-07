#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
nmrstarlib.noise
~~~~~~~~~~~~~~~~

This module provides the :class:`~nmrstarlib.noise.NoiseGenerator`
class for adding noise values to :class:`~nmrstarlib.plsimulator.Peak`
dimensions within a :class:`~nmrstarlib.plsimulator.PeakList`.
"""

import random


distributions = {"uniform": {"function": random.uniform,
                             "parameters": ["low", "high"]},
                 "triangular": {"function": random.triangular,
                                "parameters": ["left", "right", "mode"]},
                 "beta": {"function": random.betavariate,
                          "parameters": ["a", "b"]},
                 "exponential": {"function": random.expovariate,
                                 "parameters": ["scale"]},
                 "gamma": {"function": random.gammavariate,
                           "parameters": ["shape", "scale"]},
                 "gauss": {"function": random.gauss,
                           "parameters": ["mu", "sigma"]},
                 "normal": {"function": random.gauss,
                            "parameters": ["loc", "scale"]},
                 "lognormal": {"function": random.lognormvariate,
                               "parameters": ["mean", "sigma"]},
                 "vonmises": {"function": random.vonmisesvariate,
                              "parameters": ["mu", "kappa"]},
                 "pareto": {"function": random.paretovariate,
                            "parameters": ["a"]}}

try:
    import numpy as np
    NUMPY_AVAILABLE = True

    np_distributions = {"normal": {"function": np.random.normal,
                                   "parameters": ["loc", "scale"]},
                        "beta": {"function": np.random.beta,
                                 "parameters": ["a", "b"]},
                        "binomial": {"function": np.random.binomial,
                                     "parameters": ["n", "p"]},
                        "chisquare": {"function": np.random.chisquare,
                                      "parameters": ["df"]},
                        "exponential": {"function": np.random.exponential,
                                        "parameters": ["scale"]},
                        "f": {"function": np.random.f,
                              "parameters": ["dfnum", "dfden"]},
                        "gamma": {"function": np.random.gamma,
                                  "parameters": ["shape", "scale"]},
                        "geometric": {"function": np.random.geometric,
                                      "parameters": ["p"]},
                        "gumbel": {"function": np.random.gumbel,
                                   "parameters": ["loc", "scale"]},
                        "hypergeometric": {"function": np.random.hypergeometric,
                                           "parameters": ["ngood", "nbad", "nsample"]},
                        "laplace": {"function": np.random.laplace,
                                    "parameters": ["loc", "scale"]},
                        "logistic": {"function": np.random.logistic,
                                     "parameters": ["loc", "scale"]},
                        "lognormal": {"function": np.random.lognormal,
                                      "parameters": ["mean", "sigma"]},
                        "logseries": {"function": np.random.logseries,
                                      "parameters": ["p"]},
                        "negative_binomial": {"function": np.random.negative_binomial,
                                              "parameters": ["n", "p"]},
                        "noncentral_chisquare": {"function": np.random.noncentral_chisquare,
                                                 "parameters": ["df", "nonc"]},
                        "noncentral_f": {"function": np.random.noncentral_f,
                                         "parameters": ["dfnum", "dfden", "nonc"]},
                        "pareto": {"function": np.random.pareto,
                                   "parameters": ["a"]},
                        "poisson": {"function": np.random.poisson,
                                    "parameters": ["lam"]},
                        "power": {"function": np.random.power,
                                  "parameters": ["a"]},
                        "rayleigh": {"function": np.random.rayleigh,
                                     "parameters": ["scale"]},
                        "triangular": {"function": np.random.triangular,
                                       "parameters": ["left", "mode", "right"]},
                        "uniform": {"function": np.random.uniform,
                                    "parameters": ["low", "high"]},
                        "vonmises": {"function": np.random.vonmises,
                                     "parameters": ["mu", "kappa"]},
                        "wald": {"function": np.random.wald,
                                 "parameters": ["mean", "scale"]},
                        "weibull": {"function": np.random.weibull,
                                    "parameters": ["a"]},
                        "zipf": {"function": np.random.zipf,
                                 "parameters": ["a"]}}

    distributions.update(np_distributions)

except ImportError:
    NUMPY_AVAILABLE = False


class NoiseGenerator(object):
    """Noise generator class."""

    def __init__(self, parameters=None, distribution_name="normal", seed=None):
        """Noise generator initializer.

        :param dict parameters: Statistical distribution parameters per each peak list split.
        :param str distribution_name: Name of the statistical distribution function.
        """
        if parameters is None:
            parameters = dict()

        if distribution_name not in distributions:
            raise KeyError('Distribution: "{}" not in a list of allowed distributions'.format(distribution_name))

        if seed is not None:
            random.seed(seed)

            if NUMPY_AVAILABLE:
                np.random.seed(seed)

        self.parameter_names = {name[2:] for name in parameters.keys()}
        self.distribution_parameter_names = distributions[distribution_name]["parameters"]

        if set(self.distribution_parameter_names) != self.parameter_names:
            raise ValueError('Parameter names not consistent with the chosen distribution, parameters needed: {},'
                             'parameters provided: {}'.format(repr(self.distribution_parameter_names),
                                                              repr(self.parameter_names)))

        self.parameters = parameters
        self.distribution_name = distribution_name

    def generate(self, labels, split_idx):
        """Generate peak-specific noise abstract method, must be reimplemented in a subclass.

        :param tuple labels: Dimension labels of a peak.
        :param int split_idx: Index specifying which peak list split parameters to use.
        :return: List of noise values for dimensions ordered as they appear in a peak.
        :rtype: :py:class:`list`
        """
        atom_labels = [label[0] for label in labels]

        noise = []
        distribution_function = distributions[self.distribution_name]["function"]
        for label in atom_labels:
            params = [self.parameters["{}_{}".format(label, param)][split_idx]
                      for param in self.distribution_parameter_names]

            if None in params:
                dim_noise = 0.0
            else:
                try:
                    dim_noise = distribution_function(*params)
                except ValueError:
                    raise ValueError

            noise.append(dim_noise)

        return noise
