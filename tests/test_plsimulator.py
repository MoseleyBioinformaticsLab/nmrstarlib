import os
import shutil
import random
import pytest

try:
    import numpy as np
    np.random.seed(0)
except ImportError:
    pass

random.seed(0)

from nmrstarlib.converter import Converter
from nmrstarlib.translator import StarFileToPeakList
from nmrstarlib.noise import NoiseGenerator


def teardown_module(module):
    if os.path.exists("tests/example_data/NMRSTAR3/tmp"):
        shutil.rmtree("tests/example_data/NMRSTAR3/tmp")
    if os.path.exists("tests/example_data/NMRSTAR2/tmp"):
        shutil.rmtree("tests/example_data/NMRSTAR2/tmp")


noise_generator_single_source = NoiseGenerator({"H_loc": [0], "C_loc": [0], "N_loc": [0],
                                                "H_scale": [0.001], "C_scale": [0.01], "N_scale": [0.01]})

noise_generator_two_source = NoiseGenerator({"H_loc": [0, 0], "C_loc": [0, 0], "N_loc": [0, 0],
                                             "H_scale": [0.001, 0.005], "C_scale": [0.01, 0.05], "N_scale": [0.01, 0.05]})


@pytest.mark.parametrize("from_path,to_path,test_path, spectrum_name,noise_generator,plsplit,nmrstar_version", [
    # no variance
    ("tests/example_data/NMRSTAR{}/bmr18569.str", "tests/example_data/NMRSTAR{}/tmp/peaklists/no_variance/18569_{}.txt", "tests/example_data/NMRSTAR{}/peaklists/no_variance/18569_{}.txt", "CANCO", None, None, "3"),
    ("tests/example_data/NMRSTAR{}/bmr18569.str", "tests/example_data/NMRSTAR{}/tmp/peaklists/no_variance/18569_{}.txt", "tests/example_data/NMRSTAR{}/peaklists/no_variance/18569_{}.txt", "CANCOCX", None, None, "3"),
    ("tests/example_data/NMRSTAR{}/bmr18569.str", "tests/example_data/NMRSTAR{}/tmp/peaklists/no_variance/18569_{}.txt", "tests/example_data/NMRSTAR{}/peaklists/no_variance/18569_{}.txt", "CBCANH", None, None, "3"),
    ("tests/example_data/NMRSTAR{}/bmr18569.str", "tests/example_data/NMRSTAR{}/tmp/peaklists/no_variance/18569_{}.txt", "tests/example_data/NMRSTAR{}/peaklists/no_variance/18569_{}.txt", "CBCAcoNH", None, None, "3"),
    ("tests/example_data/NMRSTAR{}/bmr18569.str", "tests/example_data/NMRSTAR{}/tmp/peaklists/no_variance/18569_{}.txt", "tests/example_data/NMRSTAR{}/peaklists/no_variance/18569_{}.txt", "CCcoNH", None, None, "3"),
    ("tests/example_data/NMRSTAR{}/bmr18569.str", "tests/example_data/NMRSTAR{}/tmp/peaklists/no_variance/18569_{}.txt", "tests/example_data/NMRSTAR{}/peaklists/no_variance/18569_{}.txt", "HBHAcoNH", None, None, "3"),
    ("tests/example_data/NMRSTAR{}/bmr18569.str", "tests/example_data/NMRSTAR{}/tmp/peaklists/no_variance/18569_{}.txt", "tests/example_data/NMRSTAR{}/peaklists/no_variance/18569_{}.txt", "HNCA", None, None, "3"),
    ("tests/example_data/NMRSTAR{}/bmr18569.str", "tests/example_data/NMRSTAR{}/tmp/peaklists/no_variance/18569_{}.txt", "tests/example_data/NMRSTAR{}/peaklists/no_variance/18569_{}.txt", "HNCACB", None, None, "3"),
    ("tests/example_data/NMRSTAR{}/bmr18569.str", "tests/example_data/NMRSTAR{}/tmp/peaklists/no_variance/18569_{}.txt", "tests/example_data/NMRSTAR{}/peaklists/no_variance/18569_{}.txt", "HNCO", None, None, "3"),
    ("tests/example_data/NMRSTAR{}/bmr18569.str", "tests/example_data/NMRSTAR{}/tmp/peaklists/no_variance/18569_{}.txt", "tests/example_data/NMRSTAR{}/peaklists/no_variance/18569_{}.txt", "HNcaCO", None, None, "3"),
    ("tests/example_data/NMRSTAR{}/bmr18569.str", "tests/example_data/NMRSTAR{}/tmp/peaklists/no_variance/18569_{}.txt", "tests/example_data/NMRSTAR{}/peaklists/no_variance/18569_{}.txt", "HNcoCA", None, None, "3"),
    ("tests/example_data/NMRSTAR{}/bmr18569.str", "tests/example_data/NMRSTAR{}/tmp/peaklists/no_variance/18569_{}.txt", "tests/example_data/NMRSTAR{}/peaklists/no_variance/18569_{}.txt", "HNcoCACB", None, None, "3"),
    ("tests/example_data/NMRSTAR{}/bmr18569.str", "tests/example_data/NMRSTAR{}/tmp/peaklists/no_variance/18569_{}.txt", "tests/example_data/NMRSTAR{}/peaklists/no_variance/18569_{}.txt", "HSQC", None, None, "3"),
    ("tests/example_data/NMRSTAR{}/bmr18569.str", "tests/example_data/NMRSTAR{}/tmp/peaklists/no_variance/18569_{}.txt", "tests/example_data/NMRSTAR{}/peaklists/no_variance/18569_{}.txt", "HccoNH", None, None, "3"),
    ("tests/example_data/NMRSTAR{}/bmr18569.str", "tests/example_data/NMRSTAR{}/tmp/peaklists/no_variance/18569_{}.txt", "tests/example_data/NMRSTAR{}/peaklists/no_variance/18569_{}.txt", "NCA", None, None, "3"),
    ("tests/example_data/NMRSTAR{}/bmr18569.str", "tests/example_data/NMRSTAR{}/tmp/peaklists/no_variance/18569_{}.txt", "tests/example_data/NMRSTAR{}/peaklists/no_variance/18569_{}.txt", "NCACX", None, None, "3"),
    ("tests/example_data/NMRSTAR{}/bmr18569.str", "tests/example_data/NMRSTAR{}/tmp/peaklists/no_variance/18569_{}.txt", "tests/example_data/NMRSTAR{}/peaklists/no_variance/18569_{}.txt", "NCO", None, None, "3"),
    ("tests/example_data/NMRSTAR{}/bmr18569.str", "tests/example_data/NMRSTAR{}/tmp/peaklists/no_variance/18569_{}.txt", "tests/example_data/NMRSTAR{}/peaklists/no_variance/18569_{}.txt", "NCOCX", None, None, "3"),
    ("tests/example_data/NMRSTAR{}/bmr18569.str", "tests/example_data/NMRSTAR{}/tmp/peaklists/no_variance/18569_{}.txt", "tests/example_data/NMRSTAR{}/peaklists/no_variance/18569_{}.txt", "CANCO", None, None, "2"),
    ("tests/example_data/NMRSTAR{}/bmr18569.str", "tests/example_data/NMRSTAR{}/tmp/peaklists/no_variance/18569_{}.txt", "tests/example_data/NMRSTAR{}/peaklists/no_variance/18569_{}.txt", "CANCOCX", None, None, "2"),
    ("tests/example_data/NMRSTAR{}/bmr18569.str", "tests/example_data/NMRSTAR{}/tmp/peaklists/no_variance/18569_{}.txt", "tests/example_data/NMRSTAR{}/peaklists/no_variance/18569_{}.txt", "CBCANH", None, None, "2"),
    ("tests/example_data/NMRSTAR{}/bmr18569.str", "tests/example_data/NMRSTAR{}/tmp/peaklists/no_variance/18569_{}.txt", "tests/example_data/NMRSTAR{}/peaklists/no_variance/18569_{}.txt", "CBCAcoNH", None, None, "2"),
    ("tests/example_data/NMRSTAR{}/bmr18569.str", "tests/example_data/NMRSTAR{}/tmp/peaklists/no_variance/18569_{}.txt", "tests/example_data/NMRSTAR{}/peaklists/no_variance/18569_{}.txt", "CCcoNH", None, None, "2"),
    ("tests/example_data/NMRSTAR{}/bmr18569.str", "tests/example_data/NMRSTAR{}/tmp/peaklists/no_variance/18569_{}.txt", "tests/example_data/NMRSTAR{}/peaklists/no_variance/18569_{}.txt", "HBHAcoNH", None, None, "2"),
    ("tests/example_data/NMRSTAR{}/bmr18569.str", "tests/example_data/NMRSTAR{}/tmp/peaklists/no_variance/18569_{}.txt", "tests/example_data/NMRSTAR{}/peaklists/no_variance/18569_{}.txt", "HNCA", None, None, "2"),
    ("tests/example_data/NMRSTAR{}/bmr18569.str", "tests/example_data/NMRSTAR{}/tmp/peaklists/no_variance/18569_{}.txt", "tests/example_data/NMRSTAR{}/peaklists/no_variance/18569_{}.txt", "HNCACB", None, None, "2"),
    ("tests/example_data/NMRSTAR{}/bmr18569.str", "tests/example_data/NMRSTAR{}/tmp/peaklists/no_variance/18569_{}.txt", "tests/example_data/NMRSTAR{}/peaklists/no_variance/18569_{}.txt", "HNCO", None, None, "2"),
    ("tests/example_data/NMRSTAR{}/bmr18569.str", "tests/example_data/NMRSTAR{}/tmp/peaklists/no_variance/18569_{}.txt", "tests/example_data/NMRSTAR{}/peaklists/no_variance/18569_{}.txt", "HNcaCO", None, None, "2"),
    ("tests/example_data/NMRSTAR{}/bmr18569.str", "tests/example_data/NMRSTAR{}/tmp/peaklists/no_variance/18569_{}.txt", "tests/example_data/NMRSTAR{}/peaklists/no_variance/18569_{}.txt", "HNcoCA", None, None, "2"),
    ("tests/example_data/NMRSTAR{}/bmr18569.str", "tests/example_data/NMRSTAR{}/tmp/peaklists/no_variance/18569_{}.txt", "tests/example_data/NMRSTAR{}/peaklists/no_variance/18569_{}.txt", "HNcoCACB", None, None, "2"),
    ("tests/example_data/NMRSTAR{}/bmr18569.str", "tests/example_data/NMRSTAR{}/tmp/peaklists/no_variance/18569_{}.txt", "tests/example_data/NMRSTAR{}/peaklists/no_variance/18569_{}.txt", "HSQC", None, None, "2"),
    ("tests/example_data/NMRSTAR{}/bmr18569.str", "tests/example_data/NMRSTAR{}/tmp/peaklists/no_variance/18569_{}.txt", "tests/example_data/NMRSTAR{}/peaklists/no_variance/18569_{}.txt", "HccoNH", None, None, "2"),
    ("tests/example_data/NMRSTAR{}/bmr18569.str", "tests/example_data/NMRSTAR{}/tmp/peaklists/no_variance/18569_{}.txt", "tests/example_data/NMRSTAR{}/peaklists/no_variance/18569_{}.txt", "NCA", None, None, "2"),
    ("tests/example_data/NMRSTAR{}/bmr18569.str", "tests/example_data/NMRSTAR{}/tmp/peaklists/no_variance/18569_{}.txt", "tests/example_data/NMRSTAR{}/peaklists/no_variance/18569_{}.txt", "NCACX", None, None, "2"),
    ("tests/example_data/NMRSTAR{}/bmr18569.str", "tests/example_data/NMRSTAR{}/tmp/peaklists/no_variance/18569_{}.txt", "tests/example_data/NMRSTAR{}/peaklists/no_variance/18569_{}.txt", "NCO", None, None, "2"),
    ("tests/example_data/NMRSTAR{}/bmr18569.str", "tests/example_data/NMRSTAR{}/tmp/peaklists/no_variance/18569_{}.txt", "tests/example_data/NMRSTAR{}/peaklists/no_variance/18569_{}.txt", "NCOCX", None, None, "2"),
    # single source of variance
    ("tests/example_data/NMRSTAR{}/bmr18569.str", "tests/example_data/NMRSTAR{}/tmp/peaklists/single_source_variance/18569_{}.txt", "tests/example_data/NMRSTAR{}/peaklists/single_source_variance/18569_{}.txt", "CANCO", noise_generator_single_source, None, "3"),
    ("tests/example_data/NMRSTAR{}/bmr18569.str", "tests/example_data/NMRSTAR{}/tmp/peaklists/single_source_variance/18569_{}.txt", "tests/example_data/NMRSTAR{}/peaklists/single_source_variance/18569_{}.txt", "CANCOCX", noise_generator_single_source, None, "3"),
    ("tests/example_data/NMRSTAR{}/bmr18569.str", "tests/example_data/NMRSTAR{}/tmp/peaklists/single_source_variance/18569_{}.txt", "tests/example_data/NMRSTAR{}/peaklists/single_source_variance/18569_{}.txt", "CBCANH", noise_generator_single_source, None, "3"),
    ("tests/example_data/NMRSTAR{}/bmr18569.str", "tests/example_data/NMRSTAR{}/tmp/peaklists/single_source_variance/18569_{}.txt", "tests/example_data/NMRSTAR{}/peaklists/single_source_variance/18569_{}.txt", "CBCAcoNH", noise_generator_single_source, None, "3"),
    ("tests/example_data/NMRSTAR{}/bmr18569.str", "tests/example_data/NMRSTAR{}/tmp/peaklists/single_source_variance/18569_{}.txt", "tests/example_data/NMRSTAR{}/peaklists/single_source_variance/18569_{}.txt", "CCcoNH", noise_generator_single_source, None, "3"),
    ("tests/example_data/NMRSTAR{}/bmr18569.str", "tests/example_data/NMRSTAR{}/tmp/peaklists/single_source_variance/18569_{}.txt", "tests/example_data/NMRSTAR{}/peaklists/single_source_variance/18569_{}.txt", "HBHAcoNH", noise_generator_single_source, None, "3"),
    ("tests/example_data/NMRSTAR{}/bmr18569.str", "tests/example_data/NMRSTAR{}/tmp/peaklists/single_source_variance/18569_{}.txt", "tests/example_data/NMRSTAR{}/peaklists/single_source_variance/18569_{}.txt", "HNCA", noise_generator_single_source, None, "3"),
    ("tests/example_data/NMRSTAR{}/bmr18569.str", "tests/example_data/NMRSTAR{}/tmp/peaklists/single_source_variance/18569_{}.txt", "tests/example_data/NMRSTAR{}/peaklists/single_source_variance/18569_{}.txt", "HNCACB", noise_generator_single_source, None, "3"),
    ("tests/example_data/NMRSTAR{}/bmr18569.str", "tests/example_data/NMRSTAR{}/tmp/peaklists/single_source_variance/18569_{}.txt", "tests/example_data/NMRSTAR{}/peaklists/single_source_variance/18569_{}.txt", "HNCO", noise_generator_single_source, None, "3"),
    ("tests/example_data/NMRSTAR{}/bmr18569.str", "tests/example_data/NMRSTAR{}/tmp/peaklists/single_source_variance/18569_{}.txt", "tests/example_data/NMRSTAR{}/peaklists/single_source_variance/18569_{}.txt", "HNcaCO", noise_generator_single_source, None, "3"),
    ("tests/example_data/NMRSTAR{}/bmr18569.str", "tests/example_data/NMRSTAR{}/tmp/peaklists/single_source_variance/18569_{}.txt", "tests/example_data/NMRSTAR{}/peaklists/single_source_variance/18569_{}.txt", "HNcoCA", noise_generator_single_source, None, "3"),
    ("tests/example_data/NMRSTAR{}/bmr18569.str", "tests/example_data/NMRSTAR{}/tmp/peaklists/single_source_variance/18569_{}.txt", "tests/example_data/NMRSTAR{}/peaklists/single_source_variance/18569_{}.txt", "HNcoCACB", noise_generator_single_source, None, "3"),
    ("tests/example_data/NMRSTAR{}/bmr18569.str", "tests/example_data/NMRSTAR{}/tmp/peaklists/single_source_variance/18569_{}.txt", "tests/example_data/NMRSTAR{}/peaklists/single_source_variance/18569_{}.txt", "HSQC", noise_generator_single_source, None, "3"),
    ("tests/example_data/NMRSTAR{}/bmr18569.str", "tests/example_data/NMRSTAR{}/tmp/peaklists/single_source_variance/18569_{}.txt", "tests/example_data/NMRSTAR{}/peaklists/single_source_variance/18569_{}.txt", "HccoNH", noise_generator_single_source, None, "3"),
    ("tests/example_data/NMRSTAR{}/bmr18569.str", "tests/example_data/NMRSTAR{}/tmp/peaklists/single_source_variance/18569_{}.txt", "tests/example_data/NMRSTAR{}/peaklists/single_source_variance/18569_{}.txt", "NCA", noise_generator_single_source, None, "3"),
    ("tests/example_data/NMRSTAR{}/bmr18569.str", "tests/example_data/NMRSTAR{}/tmp/peaklists/single_source_variance/18569_{}.txt", "tests/example_data/NMRSTAR{}/peaklists/single_source_variance/18569_{}.txt", "NCACX", noise_generator_single_source, None, "3"),
    ("tests/example_data/NMRSTAR{}/bmr18569.str", "tests/example_data/NMRSTAR{}/tmp/peaklists/single_source_variance/18569_{}.txt", "tests/example_data/NMRSTAR{}/peaklists/single_source_variance/18569_{}.txt", "NCO", noise_generator_single_source, None, "3"),
    ("tests/example_data/NMRSTAR{}/bmr18569.str", "tests/example_data/NMRSTAR{}/tmp/peaklists/single_source_variance/18569_{}.txt", "tests/example_data/NMRSTAR{}/peaklists/single_source_variance/18569_{}.txt", "NCOCX", noise_generator_single_source, None, "3"),
    ("tests/example_data/NMRSTAR{}/bmr18569.str", "tests/example_data/NMRSTAR{}/tmp/peaklists/single_source_variance/18569_{}.txt", "tests/example_data/NMRSTAR{}/peaklists/single_source_variance/18569_{}.txt", "CANCO", noise_generator_single_source, None, "2"),
    ("tests/example_data/NMRSTAR{}/bmr18569.str", "tests/example_data/NMRSTAR{}/tmp/peaklists/single_source_variance/18569_{}.txt", "tests/example_data/NMRSTAR{}/peaklists/single_source_variance/18569_{}.txt", "CANCOCX", noise_generator_single_source, None, "2"),
    ("tests/example_data/NMRSTAR{}/bmr18569.str", "tests/example_data/NMRSTAR{}/tmp/peaklists/single_source_variance/18569_{}.txt", "tests/example_data/NMRSTAR{}/peaklists/single_source_variance/18569_{}.txt", "CBCANH", noise_generator_single_source, None, "2"),
    ("tests/example_data/NMRSTAR{}/bmr18569.str", "tests/example_data/NMRSTAR{}/tmp/peaklists/single_source_variance/18569_{}.txt", "tests/example_data/NMRSTAR{}/peaklists/single_source_variance/18569_{}.txt", "CBCAcoNH", noise_generator_single_source, None, "2"),
    ("tests/example_data/NMRSTAR{}/bmr18569.str", "tests/example_data/NMRSTAR{}/tmp/peaklists/single_source_variance/18569_{}.txt", "tests/example_data/NMRSTAR{}/peaklists/single_source_variance/18569_{}.txt", "CCcoNH", noise_generator_single_source, None, "2"),
    ("tests/example_data/NMRSTAR{}/bmr18569.str", "tests/example_data/NMRSTAR{}/tmp/peaklists/single_source_variance/18569_{}.txt", "tests/example_data/NMRSTAR{}/peaklists/single_source_variance/18569_{}.txt", "HBHAcoNH", noise_generator_single_source, None, "2"),
    ("tests/example_data/NMRSTAR{}/bmr18569.str", "tests/example_data/NMRSTAR{}/tmp/peaklists/single_source_variance/18569_{}.txt", "tests/example_data/NMRSTAR{}/peaklists/single_source_variance/18569_{}.txt", "HNCA", noise_generator_single_source, None, "2"),
    ("tests/example_data/NMRSTAR{}/bmr18569.str", "tests/example_data/NMRSTAR{}/tmp/peaklists/single_source_variance/18569_{}.txt", "tests/example_data/NMRSTAR{}/peaklists/single_source_variance/18569_{}.txt", "HNCACB", noise_generator_single_source, None, "2"),
    ("tests/example_data/NMRSTAR{}/bmr18569.str", "tests/example_data/NMRSTAR{}/tmp/peaklists/single_source_variance/18569_{}.txt", "tests/example_data/NMRSTAR{}/peaklists/single_source_variance/18569_{}.txt", "HNCO", noise_generator_single_source, None, "2"),
    ("tests/example_data/NMRSTAR{}/bmr18569.str", "tests/example_data/NMRSTAR{}/tmp/peaklists/single_source_variance/18569_{}.txt", "tests/example_data/NMRSTAR{}/peaklists/single_source_variance/18569_{}.txt", "HNcaCO", noise_generator_single_source, None, "2"),
    ("tests/example_data/NMRSTAR{}/bmr18569.str", "tests/example_data/NMRSTAR{}/tmp/peaklists/single_source_variance/18569_{}.txt", "tests/example_data/NMRSTAR{}/peaklists/single_source_variance/18569_{}.txt", "HNcoCA", noise_generator_single_source, None, "2"),
    ("tests/example_data/NMRSTAR{}/bmr18569.str", "tests/example_data/NMRSTAR{}/tmp/peaklists/single_source_variance/18569_{}.txt", "tests/example_data/NMRSTAR{}/peaklists/single_source_variance/18569_{}.txt", "HNcoCACB", noise_generator_single_source, None, "2"),
    ("tests/example_data/NMRSTAR{}/bmr18569.str", "tests/example_data/NMRSTAR{}/tmp/peaklists/single_source_variance/18569_{}.txt", "tests/example_data/NMRSTAR{}/peaklists/single_source_variance/18569_{}.txt", "HSQC", noise_generator_single_source, None, "2"),
    ("tests/example_data/NMRSTAR{}/bmr18569.str", "tests/example_data/NMRSTAR{}/tmp/peaklists/single_source_variance/18569_{}.txt", "tests/example_data/NMRSTAR{}/peaklists/single_source_variance/18569_{}.txt", "HccoNH", noise_generator_single_source, None, "2"),
    ("tests/example_data/NMRSTAR{}/bmr18569.str", "tests/example_data/NMRSTAR{}/tmp/peaklists/single_source_variance/18569_{}.txt", "tests/example_data/NMRSTAR{}/peaklists/single_source_variance/18569_{}.txt", "NCA", noise_generator_single_source, None, "2"),
    ("tests/example_data/NMRSTAR{}/bmr18569.str", "tests/example_data/NMRSTAR{}/tmp/peaklists/single_source_variance/18569_{}.txt", "tests/example_data/NMRSTAR{}/peaklists/single_source_variance/18569_{}.txt", "NCACX", noise_generator_single_source, None, "2"),
    ("tests/example_data/NMRSTAR{}/bmr18569.str", "tests/example_data/NMRSTAR{}/tmp/peaklists/single_source_variance/18569_{}.txt", "tests/example_data/NMRSTAR{}/peaklists/single_source_variance/18569_{}.txt", "NCO", noise_generator_single_source, None, "2"),
    ("tests/example_data/NMRSTAR{}/bmr18569.str", "tests/example_data/NMRSTAR{}/tmp/peaklists/single_source_variance/18569_{}.txt", "tests/example_data/NMRSTAR{}/peaklists/single_source_variance/18569_{}.txt", "NCOCX", noise_generator_single_source, None, "2"),
    # two sources of variance
    ("tests/example_data/NMRSTAR{}/bmr18569.str", "tests/example_data/NMRSTAR{}/tmp/peaklists/two_source_variance/18569_{}.txt", "tests/example_data/NMRSTAR{}/peaklists/two_source_variance/18569_{}.txt", "CANCO", noise_generator_two_source, (70,30), "3"),
    ("tests/example_data/NMRSTAR{}/bmr18569.str", "tests/example_data/NMRSTAR{}/tmp/peaklists/two_source_variance/18569_{}.txt", "tests/example_data/NMRSTAR{}/peaklists/two_source_variance/18569_{}.txt", "CANCOCX", noise_generator_two_source, (70,30), "3"),
    ("tests/example_data/NMRSTAR{}/bmr18569.str", "tests/example_data/NMRSTAR{}/tmp/peaklists/two_source_variance/18569_{}.txt", "tests/example_data/NMRSTAR{}/peaklists/two_source_variance/18569_{}.txt", "CBCANH", noise_generator_two_source, (70,30), "3"),
    ("tests/example_data/NMRSTAR{}/bmr18569.str", "tests/example_data/NMRSTAR{}/tmp/peaklists/two_source_variance/18569_{}.txt", "tests/example_data/NMRSTAR{}/peaklists/two_source_variance/18569_{}.txt", "CBCAcoNH", noise_generator_two_source, (70,30), "3"),
    ("tests/example_data/NMRSTAR{}/bmr18569.str", "tests/example_data/NMRSTAR{}/tmp/peaklists/two_source_variance/18569_{}.txt", "tests/example_data/NMRSTAR{}/peaklists/two_source_variance/18569_{}.txt", "CCcoNH", noise_generator_two_source, (70,30), "3"),
    ("tests/example_data/NMRSTAR{}/bmr18569.str", "tests/example_data/NMRSTAR{}/tmp/peaklists/two_source_variance/18569_{}.txt", "tests/example_data/NMRSTAR{}/peaklists/two_source_variance/18569_{}.txt", "HBHAcoNH", noise_generator_two_source, (70,30), "3"),
    ("tests/example_data/NMRSTAR{}/bmr18569.str", "tests/example_data/NMRSTAR{}/tmp/peaklists/two_source_variance/18569_{}.txt", "tests/example_data/NMRSTAR{}/peaklists/two_source_variance/18569_{}.txt", "HNCA", noise_generator_two_source, (70,30), "3"),
    ("tests/example_data/NMRSTAR{}/bmr18569.str", "tests/example_data/NMRSTAR{}/tmp/peaklists/two_source_variance/18569_{}.txt", "tests/example_data/NMRSTAR{}/peaklists/two_source_variance/18569_{}.txt", "HNCACB", noise_generator_two_source, (70,30), "3"),
    ("tests/example_data/NMRSTAR{}/bmr18569.str", "tests/example_data/NMRSTAR{}/tmp/peaklists/two_source_variance/18569_{}.txt", "tests/example_data/NMRSTAR{}/peaklists/two_source_variance/18569_{}.txt", "HNCO", noise_generator_two_source, (70,30), "3"),
    ("tests/example_data/NMRSTAR{}/bmr18569.str", "tests/example_data/NMRSTAR{}/tmp/peaklists/two_source_variance/18569_{}.txt", "tests/example_data/NMRSTAR{}/peaklists/two_source_variance/18569_{}.txt", "HNcaCO", noise_generator_two_source, (70,30), "3"),
    ("tests/example_data/NMRSTAR{}/bmr18569.str", "tests/example_data/NMRSTAR{}/tmp/peaklists/two_source_variance/18569_{}.txt", "tests/example_data/NMRSTAR{}/peaklists/two_source_variance/18569_{}.txt", "HNcoCA", noise_generator_two_source, (70,30), "3"),
    ("tests/example_data/NMRSTAR{}/bmr18569.str", "tests/example_data/NMRSTAR{}/tmp/peaklists/two_source_variance/18569_{}.txt", "tests/example_data/NMRSTAR{}/peaklists/two_source_variance/18569_{}.txt", "HNcoCACB", noise_generator_two_source, (70,30), "3"),
    ("tests/example_data/NMRSTAR{}/bmr18569.str", "tests/example_data/NMRSTAR{}/tmp/peaklists/two_source_variance/18569_{}.txt", "tests/example_data/NMRSTAR{}/peaklists/two_source_variance/18569_{}.txt", "HSQC", noise_generator_two_source, (70,30), "3"),
    ("tests/example_data/NMRSTAR{}/bmr18569.str", "tests/example_data/NMRSTAR{}/tmp/peaklists/two_source_variance/18569_{}.txt", "tests/example_data/NMRSTAR{}/peaklists/two_source_variance/18569_{}.txt", "HccoNH", noise_generator_two_source, (70,30), "3"),
    ("tests/example_data/NMRSTAR{}/bmr18569.str", "tests/example_data/NMRSTAR{}/tmp/peaklists/two_source_variance/18569_{}.txt", "tests/example_data/NMRSTAR{}/peaklists/two_source_variance/18569_{}.txt", "NCA", noise_generator_two_source, (70,30), "3"),
    ("tests/example_data/NMRSTAR{}/bmr18569.str", "tests/example_data/NMRSTAR{}/tmp/peaklists/two_source_variance/18569_{}.txt", "tests/example_data/NMRSTAR{}/peaklists/two_source_variance/18569_{}.txt", "NCACX", noise_generator_two_source, (70,30), "3"),
    ("tests/example_data/NMRSTAR{}/bmr18569.str", "tests/example_data/NMRSTAR{}/tmp/peaklists/two_source_variance/18569_{}.txt", "tests/example_data/NMRSTAR{}/peaklists/two_source_variance/18569_{}.txt", "NCO", noise_generator_two_source, (70,30), "3"),
    ("tests/example_data/NMRSTAR{}/bmr18569.str", "tests/example_data/NMRSTAR{}/tmp/peaklists/two_source_variance/18569_{}.txt", "tests/example_data/NMRSTAR{}/peaklists/two_source_variance/18569_{}.txt", "NCOCX", noise_generator_two_source, (70,30), "3"),
    ("tests/example_data/NMRSTAR{}/bmr18569.str", "tests/example_data/NMRSTAR{}/tmp/peaklists/two_source_variance/18569_{}.txt", "tests/example_data/NMRSTAR{}/peaklists/two_source_variance/18569_{}.txt", "CANCO", noise_generator_two_source, (70,30), "2"),
    ("tests/example_data/NMRSTAR{}/bmr18569.str", "tests/example_data/NMRSTAR{}/tmp/peaklists/two_source_variance/18569_{}.txt", "tests/example_data/NMRSTAR{}/peaklists/two_source_variance/18569_{}.txt", "CANCOCX", noise_generator_two_source, (70,30), "2"),
    ("tests/example_data/NMRSTAR{}/bmr18569.str", "tests/example_data/NMRSTAR{}/tmp/peaklists/two_source_variance/18569_{}.txt", "tests/example_data/NMRSTAR{}/peaklists/two_source_variance/18569_{}.txt", "CBCANH", noise_generator_two_source, (70,30), "2"),
    ("tests/example_data/NMRSTAR{}/bmr18569.str", "tests/example_data/NMRSTAR{}/tmp/peaklists/two_source_variance/18569_{}.txt", "tests/example_data/NMRSTAR{}/peaklists/two_source_variance/18569_{}.txt", "CBCAcoNH", noise_generator_two_source, (70,30), "2"),
    ("tests/example_data/NMRSTAR{}/bmr18569.str", "tests/example_data/NMRSTAR{}/tmp/peaklists/two_source_variance/18569_{}.txt", "tests/example_data/NMRSTAR{}/peaklists/two_source_variance/18569_{}.txt", "CCcoNH", noise_generator_two_source, (70,30), "2"),
    ("tests/example_data/NMRSTAR{}/bmr18569.str", "tests/example_data/NMRSTAR{}/tmp/peaklists/two_source_variance/18569_{}.txt", "tests/example_data/NMRSTAR{}/peaklists/two_source_variance/18569_{}.txt", "HBHAcoNH", noise_generator_two_source, (70,30), "2"),
    ("tests/example_data/NMRSTAR{}/bmr18569.str", "tests/example_data/NMRSTAR{}/tmp/peaklists/two_source_variance/18569_{}.txt", "tests/example_data/NMRSTAR{}/peaklists/two_source_variance/18569_{}.txt", "HNCA", noise_generator_two_source, (70,30), "2"),
    ("tests/example_data/NMRSTAR{}/bmr18569.str", "tests/example_data/NMRSTAR{}/tmp/peaklists/two_source_variance/18569_{}.txt", "tests/example_data/NMRSTAR{}/peaklists/two_source_variance/18569_{}.txt", "HNCACB", noise_generator_two_source, (70,30), "2"),
    ("tests/example_data/NMRSTAR{}/bmr18569.str", "tests/example_data/NMRSTAR{}/tmp/peaklists/two_source_variance/18569_{}.txt", "tests/example_data/NMRSTAR{}/peaklists/two_source_variance/18569_{}.txt", "HNCO", noise_generator_two_source, (70,30), "2"),
    ("tests/example_data/NMRSTAR{}/bmr18569.str", "tests/example_data/NMRSTAR{}/tmp/peaklists/two_source_variance/18569_{}.txt", "tests/example_data/NMRSTAR{}/peaklists/two_source_variance/18569_{}.txt", "HNcaCO", noise_generator_two_source, (70,30), "2"),
    ("tests/example_data/NMRSTAR{}/bmr18569.str", "tests/example_data/NMRSTAR{}/tmp/peaklists/two_source_variance/18569_{}.txt", "tests/example_data/NMRSTAR{}/peaklists/two_source_variance/18569_{}.txt", "HNcoCA", noise_generator_two_source, (70,30), "2"),
    ("tests/example_data/NMRSTAR{}/bmr18569.str", "tests/example_data/NMRSTAR{}/tmp/peaklists/two_source_variance/18569_{}.txt", "tests/example_data/NMRSTAR{}/peaklists/two_source_variance/18569_{}.txt", "HNcoCACB", noise_generator_two_source, (70,30), "2"),
    ("tests/example_data/NMRSTAR{}/bmr18569.str", "tests/example_data/NMRSTAR{}/tmp/peaklists/two_source_variance/18569_{}.txt", "tests/example_data/NMRSTAR{}/peaklists/two_source_variance/18569_{}.txt", "HSQC", noise_generator_two_source, (70,30), "2"),
    ("tests/example_data/NMRSTAR{}/bmr18569.str", "tests/example_data/NMRSTAR{}/tmp/peaklists/two_source_variance/18569_{}.txt", "tests/example_data/NMRSTAR{}/peaklists/two_source_variance/18569_{}.txt", "HccoNH", noise_generator_two_source, (70,30), "2"),
    ("tests/example_data/NMRSTAR{}/bmr18569.str", "tests/example_data/NMRSTAR{}/tmp/peaklists/two_source_variance/18569_{}.txt", "tests/example_data/NMRSTAR{}/peaklists/two_source_variance/18569_{}.txt", "NCA", noise_generator_two_source, (70,30), "2"),
    ("tests/example_data/NMRSTAR{}/bmr18569.str", "tests/example_data/NMRSTAR{}/tmp/peaklists/two_source_variance/18569_{}.txt", "tests/example_data/NMRSTAR{}/peaklists/two_source_variance/18569_{}.txt", "NCACX", noise_generator_two_source, (70,30), "2"),
    ("tests/example_data/NMRSTAR{}/bmr18569.str", "tests/example_data/NMRSTAR{}/tmp/peaklists/two_source_variance/18569_{}.txt", "tests/example_data/NMRSTAR{}/peaklists/two_source_variance/18569_{}.txt", "NCO", noise_generator_two_source, (70,30), "2"),
    ("tests/example_data/NMRSTAR{}/bmr18569.str", "tests/example_data/NMRSTAR{}/tmp/peaklists/two_source_variance/18569_{}.txt", "tests/example_data/NMRSTAR{}/peaklists/two_source_variance/18569_{}.txt", "NCOCX", noise_generator_two_source, (70,30), "2"),
])
def test_simulated_peaklists(from_path, to_path, test_path, spectrum_name, noise_generator, plsplit, nmrstar_version):
    from_path = from_path.format(nmrstar_version)
    to_path = to_path.format(nmrstar_version, spectrum_name)
    test_path = test_path.format(nmrstar_version, spectrum_name)

    peaklist_file_translator = StarFileToPeakList(from_path=from_path,
                                                  to_path=to_path,
                                                  from_format="nmrstar",
                                                  to_format="sparky",
                                                  spectrum_name=spectrum_name,
                                                  noise_generator=noise_generator,
                                                  plsplit=plsplit,
                                                  nmrstar_version=nmrstar_version)

    nmrstar_to_peaklist_converter = Converter(file_generator=peaklist_file_translator)
    nmrstar_to_peaklist_converter.convert()

    with open(test_path) as infile:
        template_peaklist  = infile.read()
    with open(to_path.format(spectrum_name)) as infile:
        generated_peaklist = infile.read()

    assert template_peaklist == generated_peaklist