import os
import shutil
import pytest

from nmrstarlib.converter import Converter
from nmrstarlib.translator import StarFileToPeakList
from nmrstarlib.noise import NoiseGenerator


def teardown_module(module):
    if os.path.exists("tests/example_data/NMRSTAR3/tmp"):
        shutil.rmtree("tests/example_data/NMRSTAR3/tmp")
    if os.path.exists("tests/example_data/NMRSTAR2/tmp"):
        shutil.rmtree("tests/example_data/NMRSTAR2/tmp")


parameters_no_variance = {"H_loc": [0], "C_loc": [0], "N_loc": [0], "H_scale": [None], "C_scale": [None], "N_scale": [None]}
parameters_single_source_variance = {"H_loc": [0], "C_loc": [0], "N_loc": [0], "H_scale": [0.001], "C_scale": [0.01], "N_scale": [0.01]}
parameters_two_source_variance = {"H_loc": [0, 0], "C_loc": [0, 0], "N_loc": [0, 0],"H_scale": [0.001, 0.005], "C_scale": [0.01, 0.05], "N_scale": [0.01, 0.05]}


@pytest.mark.parametrize("from_path,to_path,test_path,spectrum_name,distribution_name,parameters,plsplit,seed,nmrstar_version", [
    # no variance
    ("tests/example_data/NMRSTAR{}/bmr18569.str", "tests/example_data/NMRSTAR{}/tmp/peaklists/no_variance/18569_{}.txt", "tests/example_data/NMRSTAR{}/peaklists/no_variance/18569_{}.txt", "CANCO", "normal", parameters_no_variance, None, None, "3"),
    ("tests/example_data/NMRSTAR{}/bmr18569.str", "tests/example_data/NMRSTAR{}/tmp/peaklists/no_variance/18569_{}.txt", "tests/example_data/NMRSTAR{}/peaklists/no_variance/18569_{}.txt", "CANCOCX", "normal", parameters_no_variance, None, None, "3"),
    ("tests/example_data/NMRSTAR{}/bmr18569.str", "tests/example_data/NMRSTAR{}/tmp/peaklists/no_variance/18569_{}.txt", "tests/example_data/NMRSTAR{}/peaklists/no_variance/18569_{}.txt", "CBCANH", "normal", parameters_no_variance, None, None, "3"),
    ("tests/example_data/NMRSTAR{}/bmr18569.str", "tests/example_data/NMRSTAR{}/tmp/peaklists/no_variance/18569_{}.txt", "tests/example_data/NMRSTAR{}/peaklists/no_variance/18569_{}.txt", "CBCAcoNH", "normal", parameters_no_variance, None, None, "3"),
    ("tests/example_data/NMRSTAR{}/bmr18569.str", "tests/example_data/NMRSTAR{}/tmp/peaklists/no_variance/18569_{}.txt", "tests/example_data/NMRSTAR{}/peaklists/no_variance/18569_{}.txt", "CCcoNH", "normal", parameters_no_variance, None, None, "3"),
    ("tests/example_data/NMRSTAR{}/bmr18569.str", "tests/example_data/NMRSTAR{}/tmp/peaklists/no_variance/18569_{}.txt", "tests/example_data/NMRSTAR{}/peaklists/no_variance/18569_{}.txt", "HBHAcoNH", "normal", parameters_no_variance, None, None, "3"),
    ("tests/example_data/NMRSTAR{}/bmr18569.str", "tests/example_data/NMRSTAR{}/tmp/peaklists/no_variance/18569_{}.txt", "tests/example_data/NMRSTAR{}/peaklists/no_variance/18569_{}.txt", "HNCA", "normal", parameters_no_variance, None, None, "3"),
    ("tests/example_data/NMRSTAR{}/bmr18569.str", "tests/example_data/NMRSTAR{}/tmp/peaklists/no_variance/18569_{}.txt", "tests/example_data/NMRSTAR{}/peaklists/no_variance/18569_{}.txt", "HNCACB", "normal", parameters_no_variance, None, None, "3"),
    ("tests/example_data/NMRSTAR{}/bmr18569.str", "tests/example_data/NMRSTAR{}/tmp/peaklists/no_variance/18569_{}.txt", "tests/example_data/NMRSTAR{}/peaklists/no_variance/18569_{}.txt", "HNCO", "normal", parameters_no_variance, None, None, "3"),
    ("tests/example_data/NMRSTAR{}/bmr18569.str", "tests/example_data/NMRSTAR{}/tmp/peaklists/no_variance/18569_{}.txt", "tests/example_data/NMRSTAR{}/peaklists/no_variance/18569_{}.txt", "HNcaCO", "normal", parameters_no_variance, None, None, "3"),
    ("tests/example_data/NMRSTAR{}/bmr18569.str", "tests/example_data/NMRSTAR{}/tmp/peaklists/no_variance/18569_{}.txt", "tests/example_data/NMRSTAR{}/peaklists/no_variance/18569_{}.txt", "HNcoCA", "normal", parameters_no_variance, None, None, "3"),
    ("tests/example_data/NMRSTAR{}/bmr18569.str", "tests/example_data/NMRSTAR{}/tmp/peaklists/no_variance/18569_{}.txt", "tests/example_data/NMRSTAR{}/peaklists/no_variance/18569_{}.txt", "HNcoCACB", "normal", parameters_no_variance, None, None, "3"),
    ("tests/example_data/NMRSTAR{}/bmr18569.str", "tests/example_data/NMRSTAR{}/tmp/peaklists/no_variance/18569_{}.txt", "tests/example_data/NMRSTAR{}/peaklists/no_variance/18569_{}.txt", "HSQC", "normal", parameters_no_variance, None, None, "3"),
    ("tests/example_data/NMRSTAR{}/bmr18569.str", "tests/example_data/NMRSTAR{}/tmp/peaklists/no_variance/18569_{}.txt", "tests/example_data/NMRSTAR{}/peaklists/no_variance/18569_{}.txt", "HccoNH", "normal", parameters_no_variance, None, None, "3"),
    ("tests/example_data/NMRSTAR{}/bmr18569.str", "tests/example_data/NMRSTAR{}/tmp/peaklists/no_variance/18569_{}.txt", "tests/example_data/NMRSTAR{}/peaklists/no_variance/18569_{}.txt", "NCA", "normal", parameters_no_variance, None, None, "3"),
    ("tests/example_data/NMRSTAR{}/bmr18569.str", "tests/example_data/NMRSTAR{}/tmp/peaklists/no_variance/18569_{}.txt", "tests/example_data/NMRSTAR{}/peaklists/no_variance/18569_{}.txt", "NCACX", "normal", parameters_no_variance, None, None, "3"),
    ("tests/example_data/NMRSTAR{}/bmr18569.str", "tests/example_data/NMRSTAR{}/tmp/peaklists/no_variance/18569_{}.txt", "tests/example_data/NMRSTAR{}/peaklists/no_variance/18569_{}.txt", "NCO", "normal", parameters_no_variance, None, None, "3"),
    ("tests/example_data/NMRSTAR{}/bmr18569.str", "tests/example_data/NMRSTAR{}/tmp/peaklists/no_variance/18569_{}.txt", "tests/example_data/NMRSTAR{}/peaklists/no_variance/18569_{}.txt", "NCOCX", "normal", parameters_no_variance, None, None, "3"),
    ("tests/example_data/NMRSTAR{}/bmr18569.str", "tests/example_data/NMRSTAR{}/tmp/peaklists/no_variance/18569_{}.txt", "tests/example_data/NMRSTAR{}/peaklists/no_variance/18569_{}.txt", "CANCO", "normal", parameters_no_variance, None, None, "2"),
    ("tests/example_data/NMRSTAR{}/bmr18569.str", "tests/example_data/NMRSTAR{}/tmp/peaklists/no_variance/18569_{}.txt", "tests/example_data/NMRSTAR{}/peaklists/no_variance/18569_{}.txt", "CANCOCX", "normal", parameters_no_variance, None, None, "2"),
    ("tests/example_data/NMRSTAR{}/bmr18569.str", "tests/example_data/NMRSTAR{}/tmp/peaklists/no_variance/18569_{}.txt", "tests/example_data/NMRSTAR{}/peaklists/no_variance/18569_{}.txt", "CBCANH", "normal", parameters_no_variance, None, None, "2"),
    ("tests/example_data/NMRSTAR{}/bmr18569.str", "tests/example_data/NMRSTAR{}/tmp/peaklists/no_variance/18569_{}.txt", "tests/example_data/NMRSTAR{}/peaklists/no_variance/18569_{}.txt", "CBCAcoNH", "normal", parameters_no_variance, None, None, "2"),
    ("tests/example_data/NMRSTAR{}/bmr18569.str", "tests/example_data/NMRSTAR{}/tmp/peaklists/no_variance/18569_{}.txt", "tests/example_data/NMRSTAR{}/peaklists/no_variance/18569_{}.txt", "CCcoNH", "normal", parameters_no_variance, None, None, "2"),
    ("tests/example_data/NMRSTAR{}/bmr18569.str", "tests/example_data/NMRSTAR{}/tmp/peaklists/no_variance/18569_{}.txt", "tests/example_data/NMRSTAR{}/peaklists/no_variance/18569_{}.txt", "HBHAcoNH", "normal", parameters_no_variance, None, None, "2"),
    ("tests/example_data/NMRSTAR{}/bmr18569.str", "tests/example_data/NMRSTAR{}/tmp/peaklists/no_variance/18569_{}.txt", "tests/example_data/NMRSTAR{}/peaklists/no_variance/18569_{}.txt", "HNCA", "normal", parameters_no_variance, None, None, "2"),
    ("tests/example_data/NMRSTAR{}/bmr18569.str", "tests/example_data/NMRSTAR{}/tmp/peaklists/no_variance/18569_{}.txt", "tests/example_data/NMRSTAR{}/peaklists/no_variance/18569_{}.txt", "HNCACB", "normal", parameters_no_variance, None, None, "2"),
    ("tests/example_data/NMRSTAR{}/bmr18569.str", "tests/example_data/NMRSTAR{}/tmp/peaklists/no_variance/18569_{}.txt", "tests/example_data/NMRSTAR{}/peaklists/no_variance/18569_{}.txt", "HNCO", "normal", parameters_no_variance, None, None, "2"),
    ("tests/example_data/NMRSTAR{}/bmr18569.str", "tests/example_data/NMRSTAR{}/tmp/peaklists/no_variance/18569_{}.txt", "tests/example_data/NMRSTAR{}/peaklists/no_variance/18569_{}.txt", "HNcaCO", "normal", parameters_no_variance, None, None, "2"),
    ("tests/example_data/NMRSTAR{}/bmr18569.str", "tests/example_data/NMRSTAR{}/tmp/peaklists/no_variance/18569_{}.txt", "tests/example_data/NMRSTAR{}/peaklists/no_variance/18569_{}.txt", "HNcoCA", "normal", parameters_no_variance, None, None, "2"),
    ("tests/example_data/NMRSTAR{}/bmr18569.str", "tests/example_data/NMRSTAR{}/tmp/peaklists/no_variance/18569_{}.txt", "tests/example_data/NMRSTAR{}/peaklists/no_variance/18569_{}.txt", "HNcoCACB", "normal", parameters_no_variance, None, None, "2"),
    ("tests/example_data/NMRSTAR{}/bmr18569.str", "tests/example_data/NMRSTAR{}/tmp/peaklists/no_variance/18569_{}.txt", "tests/example_data/NMRSTAR{}/peaklists/no_variance/18569_{}.txt", "HSQC", "normal", parameters_no_variance, None, None, "2"),
    ("tests/example_data/NMRSTAR{}/bmr18569.str", "tests/example_data/NMRSTAR{}/tmp/peaklists/no_variance/18569_{}.txt", "tests/example_data/NMRSTAR{}/peaklists/no_variance/18569_{}.txt", "HccoNH", "normal", parameters_no_variance, None, None, "2"),
    ("tests/example_data/NMRSTAR{}/bmr18569.str", "tests/example_data/NMRSTAR{}/tmp/peaklists/no_variance/18569_{}.txt", "tests/example_data/NMRSTAR{}/peaklists/no_variance/18569_{}.txt", "NCA", "normal", parameters_no_variance, None, None, "2"),
    ("tests/example_data/NMRSTAR{}/bmr18569.str", "tests/example_data/NMRSTAR{}/tmp/peaklists/no_variance/18569_{}.txt", "tests/example_data/NMRSTAR{}/peaklists/no_variance/18569_{}.txt", "NCACX", "normal", parameters_no_variance, None, None, "2"),
    ("tests/example_data/NMRSTAR{}/bmr18569.str", "tests/example_data/NMRSTAR{}/tmp/peaklists/no_variance/18569_{}.txt", "tests/example_data/NMRSTAR{}/peaklists/no_variance/18569_{}.txt", "NCO", "normal", parameters_no_variance, None, None, "2"),
    ("tests/example_data/NMRSTAR{}/bmr18569.str", "tests/example_data/NMRSTAR{}/tmp/peaklists/no_variance/18569_{}.txt", "tests/example_data/NMRSTAR{}/peaklists/no_variance/18569_{}.txt", "NCOCX", "normal", parameters_no_variance, None, None, "2"),
    # single source of variance
    ("tests/example_data/NMRSTAR{}/bmr18569.str", "tests/example_data/NMRSTAR{}/tmp/peaklists/single_source_variance/18569_{}.txt", "tests/example_data/NMRSTAR{}/peaklists/single_source_variance/18569_{}.txt", "CANCO", "normal", parameters_single_source_variance, None, 0, "3"),
    ("tests/example_data/NMRSTAR{}/bmr18569.str", "tests/example_data/NMRSTAR{}/tmp/peaklists/single_source_variance/18569_{}.txt", "tests/example_data/NMRSTAR{}/peaklists/single_source_variance/18569_{}.txt", "CANCOCX", "normal", parameters_single_source_variance, None, 0, "3"),
    ("tests/example_data/NMRSTAR{}/bmr18569.str", "tests/example_data/NMRSTAR{}/tmp/peaklists/single_source_variance/18569_{}.txt", "tests/example_data/NMRSTAR{}/peaklists/single_source_variance/18569_{}.txt", "CBCANH", "normal", parameters_single_source_variance, None, 0, "3"),
    ("tests/example_data/NMRSTAR{}/bmr18569.str", "tests/example_data/NMRSTAR{}/tmp/peaklists/single_source_variance/18569_{}.txt", "tests/example_data/NMRSTAR{}/peaklists/single_source_variance/18569_{}.txt", "CBCAcoNH", "normal", parameters_single_source_variance, None, 0, "3"),
    ("tests/example_data/NMRSTAR{}/bmr18569.str", "tests/example_data/NMRSTAR{}/tmp/peaklists/single_source_variance/18569_{}.txt", "tests/example_data/NMRSTAR{}/peaklists/single_source_variance/18569_{}.txt", "CCcoNH", "normal", parameters_single_source_variance, None, 0, "3"),
    ("tests/example_data/NMRSTAR{}/bmr18569.str", "tests/example_data/NMRSTAR{}/tmp/peaklists/single_source_variance/18569_{}.txt", "tests/example_data/NMRSTAR{}/peaklists/single_source_variance/18569_{}.txt", "HBHAcoNH", "normal", parameters_single_source_variance, None, 0, "3"),
    ("tests/example_data/NMRSTAR{}/bmr18569.str", "tests/example_data/NMRSTAR{}/tmp/peaklists/single_source_variance/18569_{}.txt", "tests/example_data/NMRSTAR{}/peaklists/single_source_variance/18569_{}.txt", "HNCA", "normal", parameters_single_source_variance, None, 0, "3"),
    ("tests/example_data/NMRSTAR{}/bmr18569.str", "tests/example_data/NMRSTAR{}/tmp/peaklists/single_source_variance/18569_{}.txt", "tests/example_data/NMRSTAR{}/peaklists/single_source_variance/18569_{}.txt", "HNCACB", "normal", parameters_single_source_variance, None, 0, "3"),
    ("tests/example_data/NMRSTAR{}/bmr18569.str", "tests/example_data/NMRSTAR{}/tmp/peaklists/single_source_variance/18569_{}.txt", "tests/example_data/NMRSTAR{}/peaklists/single_source_variance/18569_{}.txt", "HNCO", "normal", parameters_single_source_variance, None, 0, "3"),
    ("tests/example_data/NMRSTAR{}/bmr18569.str", "tests/example_data/NMRSTAR{}/tmp/peaklists/single_source_variance/18569_{}.txt", "tests/example_data/NMRSTAR{}/peaklists/single_source_variance/18569_{}.txt", "HNcaCO", "normal", parameters_single_source_variance, None, 0, "3"),
    ("tests/example_data/NMRSTAR{}/bmr18569.str", "tests/example_data/NMRSTAR{}/tmp/peaklists/single_source_variance/18569_{}.txt", "tests/example_data/NMRSTAR{}/peaklists/single_source_variance/18569_{}.txt", "HNcoCA", "normal", parameters_single_source_variance, None, 0, "3"),
    ("tests/example_data/NMRSTAR{}/bmr18569.str", "tests/example_data/NMRSTAR{}/tmp/peaklists/single_source_variance/18569_{}.txt", "tests/example_data/NMRSTAR{}/peaklists/single_source_variance/18569_{}.txt", "HNcoCACB", "normal", parameters_single_source_variance, None, 0, "3"),
    ("tests/example_data/NMRSTAR{}/bmr18569.str", "tests/example_data/NMRSTAR{}/tmp/peaklists/single_source_variance/18569_{}.txt", "tests/example_data/NMRSTAR{}/peaklists/single_source_variance/18569_{}.txt", "HSQC", "normal", parameters_single_source_variance, None, 0, "3"),
    ("tests/example_data/NMRSTAR{}/bmr18569.str", "tests/example_data/NMRSTAR{}/tmp/peaklists/single_source_variance/18569_{}.txt", "tests/example_data/NMRSTAR{}/peaklists/single_source_variance/18569_{}.txt", "HccoNH", "normal", parameters_single_source_variance, None, 0, "3"),
    ("tests/example_data/NMRSTAR{}/bmr18569.str", "tests/example_data/NMRSTAR{}/tmp/peaklists/single_source_variance/18569_{}.txt", "tests/example_data/NMRSTAR{}/peaklists/single_source_variance/18569_{}.txt", "NCA", "normal", parameters_single_source_variance, None, 0, "3"),
    ("tests/example_data/NMRSTAR{}/bmr18569.str", "tests/example_data/NMRSTAR{}/tmp/peaklists/single_source_variance/18569_{}.txt", "tests/example_data/NMRSTAR{}/peaklists/single_source_variance/18569_{}.txt", "NCACX", "normal", parameters_single_source_variance, None, 0, "3"),
    ("tests/example_data/NMRSTAR{}/bmr18569.str", "tests/example_data/NMRSTAR{}/tmp/peaklists/single_source_variance/18569_{}.txt", "tests/example_data/NMRSTAR{}/peaklists/single_source_variance/18569_{}.txt", "NCO", "normal", parameters_single_source_variance, None, 0, "3"),
    ("tests/example_data/NMRSTAR{}/bmr18569.str", "tests/example_data/NMRSTAR{}/tmp/peaklists/single_source_variance/18569_{}.txt", "tests/example_data/NMRSTAR{}/peaklists/single_source_variance/18569_{}.txt", "NCOCX", "normal", parameters_single_source_variance, None, 0, "3"),
    ("tests/example_data/NMRSTAR{}/bmr18569.str", "tests/example_data/NMRSTAR{}/tmp/peaklists/single_source_variance/18569_{}.txt", "tests/example_data/NMRSTAR{}/peaklists/single_source_variance/18569_{}.txt", "CANCO", "normal", parameters_single_source_variance, None, 0, "2"),
    ("tests/example_data/NMRSTAR{}/bmr18569.str", "tests/example_data/NMRSTAR{}/tmp/peaklists/single_source_variance/18569_{}.txt", "tests/example_data/NMRSTAR{}/peaklists/single_source_variance/18569_{}.txt", "CANCOCX", "normal", parameters_single_source_variance, None, 0, "2"),
    ("tests/example_data/NMRSTAR{}/bmr18569.str", "tests/example_data/NMRSTAR{}/tmp/peaklists/single_source_variance/18569_{}.txt", "tests/example_data/NMRSTAR{}/peaklists/single_source_variance/18569_{}.txt", "CBCANH", "normal", parameters_single_source_variance, None, 0, "2"),
    ("tests/example_data/NMRSTAR{}/bmr18569.str", "tests/example_data/NMRSTAR{}/tmp/peaklists/single_source_variance/18569_{}.txt", "tests/example_data/NMRSTAR{}/peaklists/single_source_variance/18569_{}.txt", "CBCAcoNH", "normal", parameters_single_source_variance, None, 0, "2"),
    ("tests/example_data/NMRSTAR{}/bmr18569.str", "tests/example_data/NMRSTAR{}/tmp/peaklists/single_source_variance/18569_{}.txt", "tests/example_data/NMRSTAR{}/peaklists/single_source_variance/18569_{}.txt", "CCcoNH", "normal", parameters_single_source_variance, None, 0, "2"),
    ("tests/example_data/NMRSTAR{}/bmr18569.str", "tests/example_data/NMRSTAR{}/tmp/peaklists/single_source_variance/18569_{}.txt", "tests/example_data/NMRSTAR{}/peaklists/single_source_variance/18569_{}.txt", "HBHAcoNH", "normal", parameters_single_source_variance, None, 0, "2"),
    ("tests/example_data/NMRSTAR{}/bmr18569.str", "tests/example_data/NMRSTAR{}/tmp/peaklists/single_source_variance/18569_{}.txt", "tests/example_data/NMRSTAR{}/peaklists/single_source_variance/18569_{}.txt", "HNCA", "normal", parameters_single_source_variance, None, 0, "2"),
    ("tests/example_data/NMRSTAR{}/bmr18569.str", "tests/example_data/NMRSTAR{}/tmp/peaklists/single_source_variance/18569_{}.txt", "tests/example_data/NMRSTAR{}/peaklists/single_source_variance/18569_{}.txt", "HNCACB", "normal", parameters_single_source_variance, None, 0, "2"),
    ("tests/example_data/NMRSTAR{}/bmr18569.str", "tests/example_data/NMRSTAR{}/tmp/peaklists/single_source_variance/18569_{}.txt", "tests/example_data/NMRSTAR{}/peaklists/single_source_variance/18569_{}.txt", "HNCO", "normal", parameters_single_source_variance, None, 0, "2"),
    ("tests/example_data/NMRSTAR{}/bmr18569.str", "tests/example_data/NMRSTAR{}/tmp/peaklists/single_source_variance/18569_{}.txt", "tests/example_data/NMRSTAR{}/peaklists/single_source_variance/18569_{}.txt", "HNcaCO", "normal", parameters_single_source_variance, None, 0, "2"),
    ("tests/example_data/NMRSTAR{}/bmr18569.str", "tests/example_data/NMRSTAR{}/tmp/peaklists/single_source_variance/18569_{}.txt", "tests/example_data/NMRSTAR{}/peaklists/single_source_variance/18569_{}.txt", "HNcoCA", "normal", parameters_single_source_variance, None, 0, "2"),
    ("tests/example_data/NMRSTAR{}/bmr18569.str", "tests/example_data/NMRSTAR{}/tmp/peaklists/single_source_variance/18569_{}.txt", "tests/example_data/NMRSTAR{}/peaklists/single_source_variance/18569_{}.txt", "HNcoCACB", "normal", parameters_single_source_variance, None, 0, "2"),
    ("tests/example_data/NMRSTAR{}/bmr18569.str", "tests/example_data/NMRSTAR{}/tmp/peaklists/single_source_variance/18569_{}.txt", "tests/example_data/NMRSTAR{}/peaklists/single_source_variance/18569_{}.txt", "HSQC", "normal", parameters_single_source_variance, None, 0, "2"),
    ("tests/example_data/NMRSTAR{}/bmr18569.str", "tests/example_data/NMRSTAR{}/tmp/peaklists/single_source_variance/18569_{}.txt", "tests/example_data/NMRSTAR{}/peaklists/single_source_variance/18569_{}.txt", "HccoNH", "normal", parameters_single_source_variance, None, 0, "2"),
    ("tests/example_data/NMRSTAR{}/bmr18569.str", "tests/example_data/NMRSTAR{}/tmp/peaklists/single_source_variance/18569_{}.txt", "tests/example_data/NMRSTAR{}/peaklists/single_source_variance/18569_{}.txt", "NCA", "normal", parameters_single_source_variance, None, 0, "2"),
    ("tests/example_data/NMRSTAR{}/bmr18569.str", "tests/example_data/NMRSTAR{}/tmp/peaklists/single_source_variance/18569_{}.txt", "tests/example_data/NMRSTAR{}/peaklists/single_source_variance/18569_{}.txt", "NCACX", "normal", parameters_single_source_variance, None, 0, "2"),
    ("tests/example_data/NMRSTAR{}/bmr18569.str", "tests/example_data/NMRSTAR{}/tmp/peaklists/single_source_variance/18569_{}.txt", "tests/example_data/NMRSTAR{}/peaklists/single_source_variance/18569_{}.txt", "NCO", "normal", parameters_single_source_variance, None, 0, "2"),
    ("tests/example_data/NMRSTAR{}/bmr18569.str", "tests/example_data/NMRSTAR{}/tmp/peaklists/single_source_variance/18569_{}.txt", "tests/example_data/NMRSTAR{}/peaklists/single_source_variance/18569_{}.txt", "NCOCX", "normal", parameters_single_source_variance, None, 0, "2"),
    # two sources of variance
    ("tests/example_data/NMRSTAR{}/bmr18569.str", "tests/example_data/NMRSTAR{}/tmp/peaklists/two_source_variance/18569_{}.txt", "tests/example_data/NMRSTAR{}/peaklists/two_source_variance/18569_{}.txt", "CANCO", "normal", parameters_two_source_variance, (70,30), 0, "3"),
    ("tests/example_data/NMRSTAR{}/bmr18569.str", "tests/example_data/NMRSTAR{}/tmp/peaklists/two_source_variance/18569_{}.txt", "tests/example_data/NMRSTAR{}/peaklists/two_source_variance/18569_{}.txt", "CANCOCX", "normal", parameters_two_source_variance, (70,30), 0, "3"),
    ("tests/example_data/NMRSTAR{}/bmr18569.str", "tests/example_data/NMRSTAR{}/tmp/peaklists/two_source_variance/18569_{}.txt", "tests/example_data/NMRSTAR{}/peaklists/two_source_variance/18569_{}.txt", "CBCANH", "normal", parameters_two_source_variance, (70,30), 0, "3"),
    ("tests/example_data/NMRSTAR{}/bmr18569.str", "tests/example_data/NMRSTAR{}/tmp/peaklists/two_source_variance/18569_{}.txt", "tests/example_data/NMRSTAR{}/peaklists/two_source_variance/18569_{}.txt", "CBCAcoNH", "normal", parameters_two_source_variance, (70,30), 0, "3"),
    ("tests/example_data/NMRSTAR{}/bmr18569.str", "tests/example_data/NMRSTAR{}/tmp/peaklists/two_source_variance/18569_{}.txt", "tests/example_data/NMRSTAR{}/peaklists/two_source_variance/18569_{}.txt", "CCcoNH", "normal", parameters_two_source_variance, (70,30), 0, "3"),
    ("tests/example_data/NMRSTAR{}/bmr18569.str", "tests/example_data/NMRSTAR{}/tmp/peaklists/two_source_variance/18569_{}.txt", "tests/example_data/NMRSTAR{}/peaklists/two_source_variance/18569_{}.txt", "HBHAcoNH", "normal", parameters_two_source_variance, (70,30), 0, "3"),
    ("tests/example_data/NMRSTAR{}/bmr18569.str", "tests/example_data/NMRSTAR{}/tmp/peaklists/two_source_variance/18569_{}.txt", "tests/example_data/NMRSTAR{}/peaklists/two_source_variance/18569_{}.txt", "HNCA", "normal", parameters_two_source_variance, (70,30), 0, "3"),
    ("tests/example_data/NMRSTAR{}/bmr18569.str", "tests/example_data/NMRSTAR{}/tmp/peaklists/two_source_variance/18569_{}.txt", "tests/example_data/NMRSTAR{}/peaklists/two_source_variance/18569_{}.txt", "HNCACB", "normal", parameters_two_source_variance, (70,30), 0, "3"),
    ("tests/example_data/NMRSTAR{}/bmr18569.str", "tests/example_data/NMRSTAR{}/tmp/peaklists/two_source_variance/18569_{}.txt", "tests/example_data/NMRSTAR{}/peaklists/two_source_variance/18569_{}.txt", "HNCO", "normal", parameters_two_source_variance, (70,30), 0, "3"),
    ("tests/example_data/NMRSTAR{}/bmr18569.str", "tests/example_data/NMRSTAR{}/tmp/peaklists/two_source_variance/18569_{}.txt", "tests/example_data/NMRSTAR{}/peaklists/two_source_variance/18569_{}.txt", "HNcaCO", "normal", parameters_two_source_variance, (70,30), 0, "3"),
    ("tests/example_data/NMRSTAR{}/bmr18569.str", "tests/example_data/NMRSTAR{}/tmp/peaklists/two_source_variance/18569_{}.txt", "tests/example_data/NMRSTAR{}/peaklists/two_source_variance/18569_{}.txt", "HNcoCA", "normal", parameters_two_source_variance, (70,30), 0, "3"),
    ("tests/example_data/NMRSTAR{}/bmr18569.str", "tests/example_data/NMRSTAR{}/tmp/peaklists/two_source_variance/18569_{}.txt", "tests/example_data/NMRSTAR{}/peaklists/two_source_variance/18569_{}.txt", "HNcoCACB", "normal", parameters_two_source_variance, (70,30), 0, "3"),
    ("tests/example_data/NMRSTAR{}/bmr18569.str", "tests/example_data/NMRSTAR{}/tmp/peaklists/two_source_variance/18569_{}.txt", "tests/example_data/NMRSTAR{}/peaklists/two_source_variance/18569_{}.txt", "HSQC", "normal", parameters_two_source_variance, (70,30), 0, "3"),
    ("tests/example_data/NMRSTAR{}/bmr18569.str", "tests/example_data/NMRSTAR{}/tmp/peaklists/two_source_variance/18569_{}.txt", "tests/example_data/NMRSTAR{}/peaklists/two_source_variance/18569_{}.txt", "HccoNH", "normal", parameters_two_source_variance, (70,30), 0, "3"),
    ("tests/example_data/NMRSTAR{}/bmr18569.str", "tests/example_data/NMRSTAR{}/tmp/peaklists/two_source_variance/18569_{}.txt", "tests/example_data/NMRSTAR{}/peaklists/two_source_variance/18569_{}.txt", "NCA", "normal", parameters_two_source_variance, (70,30), 0, "3"),
    ("tests/example_data/NMRSTAR{}/bmr18569.str", "tests/example_data/NMRSTAR{}/tmp/peaklists/two_source_variance/18569_{}.txt", "tests/example_data/NMRSTAR{}/peaklists/two_source_variance/18569_{}.txt", "NCACX", "normal", parameters_two_source_variance, (70,30), 0, "3"),
    ("tests/example_data/NMRSTAR{}/bmr18569.str", "tests/example_data/NMRSTAR{}/tmp/peaklists/two_source_variance/18569_{}.txt", "tests/example_data/NMRSTAR{}/peaklists/two_source_variance/18569_{}.txt", "NCO", "normal", parameters_two_source_variance, (70,30), 0, "3"),
    ("tests/example_data/NMRSTAR{}/bmr18569.str", "tests/example_data/NMRSTAR{}/tmp/peaklists/two_source_variance/18569_{}.txt", "tests/example_data/NMRSTAR{}/peaklists/two_source_variance/18569_{}.txt", "NCOCX", "normal", parameters_two_source_variance, (70,30), 0, "3"),
    ("tests/example_data/NMRSTAR{}/bmr18569.str", "tests/example_data/NMRSTAR{}/tmp/peaklists/two_source_variance/18569_{}.txt", "tests/example_data/NMRSTAR{}/peaklists/two_source_variance/18569_{}.txt", "CANCO", "normal", parameters_two_source_variance, (70,30), 0, "2"),
    ("tests/example_data/NMRSTAR{}/bmr18569.str", "tests/example_data/NMRSTAR{}/tmp/peaklists/two_source_variance/18569_{}.txt", "tests/example_data/NMRSTAR{}/peaklists/two_source_variance/18569_{}.txt", "CANCOCX", "normal", parameters_two_source_variance, (70,30), 0, "2"),
    ("tests/example_data/NMRSTAR{}/bmr18569.str", "tests/example_data/NMRSTAR{}/tmp/peaklists/two_source_variance/18569_{}.txt", "tests/example_data/NMRSTAR{}/peaklists/two_source_variance/18569_{}.txt", "CBCANH", "normal", parameters_two_source_variance, (70,30), 0, "2"),
    ("tests/example_data/NMRSTAR{}/bmr18569.str", "tests/example_data/NMRSTAR{}/tmp/peaklists/two_source_variance/18569_{}.txt", "tests/example_data/NMRSTAR{}/peaklists/two_source_variance/18569_{}.txt", "CBCAcoNH", "normal", parameters_two_source_variance, (70,30), 0, "2"),
    ("tests/example_data/NMRSTAR{}/bmr18569.str", "tests/example_data/NMRSTAR{}/tmp/peaklists/two_source_variance/18569_{}.txt", "tests/example_data/NMRSTAR{}/peaklists/two_source_variance/18569_{}.txt", "CCcoNH", "normal", parameters_two_source_variance, (70,30), 0, "2"),
    ("tests/example_data/NMRSTAR{}/bmr18569.str", "tests/example_data/NMRSTAR{}/tmp/peaklists/two_source_variance/18569_{}.txt", "tests/example_data/NMRSTAR{}/peaklists/two_source_variance/18569_{}.txt", "HBHAcoNH", "normal", parameters_two_source_variance, (70,30), 0, "2"),
    ("tests/example_data/NMRSTAR{}/bmr18569.str", "tests/example_data/NMRSTAR{}/tmp/peaklists/two_source_variance/18569_{}.txt", "tests/example_data/NMRSTAR{}/peaklists/two_source_variance/18569_{}.txt", "HNCA", "normal", parameters_two_source_variance, (70,30), 0, "2"),
    ("tests/example_data/NMRSTAR{}/bmr18569.str", "tests/example_data/NMRSTAR{}/tmp/peaklists/two_source_variance/18569_{}.txt", "tests/example_data/NMRSTAR{}/peaklists/two_source_variance/18569_{}.txt", "HNCACB", "normal", parameters_two_source_variance, (70,30), 0, "2"),
    ("tests/example_data/NMRSTAR{}/bmr18569.str", "tests/example_data/NMRSTAR{}/tmp/peaklists/two_source_variance/18569_{}.txt", "tests/example_data/NMRSTAR{}/peaklists/two_source_variance/18569_{}.txt", "HNCO", "normal", parameters_two_source_variance, (70,30), 0, "2"),
    ("tests/example_data/NMRSTAR{}/bmr18569.str", "tests/example_data/NMRSTAR{}/tmp/peaklists/two_source_variance/18569_{}.txt", "tests/example_data/NMRSTAR{}/peaklists/two_source_variance/18569_{}.txt", "HNcaCO", "normal", parameters_two_source_variance, (70,30), 0, "2"),
    ("tests/example_data/NMRSTAR{}/bmr18569.str", "tests/example_data/NMRSTAR{}/tmp/peaklists/two_source_variance/18569_{}.txt", "tests/example_data/NMRSTAR{}/peaklists/two_source_variance/18569_{}.txt", "HNcoCA", "normal", parameters_two_source_variance, (70,30), 0, "2"),
    ("tests/example_data/NMRSTAR{}/bmr18569.str", "tests/example_data/NMRSTAR{}/tmp/peaklists/two_source_variance/18569_{}.txt", "tests/example_data/NMRSTAR{}/peaklists/two_source_variance/18569_{}.txt", "HNcoCACB", "normal", parameters_two_source_variance, (70,30), 0, "2"),
    ("tests/example_data/NMRSTAR{}/bmr18569.str", "tests/example_data/NMRSTAR{}/tmp/peaklists/two_source_variance/18569_{}.txt", "tests/example_data/NMRSTAR{}/peaklists/two_source_variance/18569_{}.txt", "HSQC", "normal", parameters_two_source_variance, (70,30), 0, "2"),
    ("tests/example_data/NMRSTAR{}/bmr18569.str", "tests/example_data/NMRSTAR{}/tmp/peaklists/two_source_variance/18569_{}.txt", "tests/example_data/NMRSTAR{}/peaklists/two_source_variance/18569_{}.txt", "HccoNH", "normal", parameters_two_source_variance, (70,30), 0, "2"),
    ("tests/example_data/NMRSTAR{}/bmr18569.str", "tests/example_data/NMRSTAR{}/tmp/peaklists/two_source_variance/18569_{}.txt", "tests/example_data/NMRSTAR{}/peaklists/two_source_variance/18569_{}.txt", "NCA", "normal", parameters_two_source_variance, (70,30), 0, "2"),
    ("tests/example_data/NMRSTAR{}/bmr18569.str", "tests/example_data/NMRSTAR{}/tmp/peaklists/two_source_variance/18569_{}.txt", "tests/example_data/NMRSTAR{}/peaklists/two_source_variance/18569_{}.txt", "NCACX", "normal", parameters_two_source_variance, (70,30), 0, "2"),
    ("tests/example_data/NMRSTAR{}/bmr18569.str", "tests/example_data/NMRSTAR{}/tmp/peaklists/two_source_variance/18569_{}.txt", "tests/example_data/NMRSTAR{}/peaklists/two_source_variance/18569_{}.txt", "NCO", "normal", parameters_two_source_variance, (70,30), 0, "2"),
    ("tests/example_data/NMRSTAR{}/bmr18569.str", "tests/example_data/NMRSTAR{}/tmp/peaklists/two_source_variance/18569_{}.txt", "tests/example_data/NMRSTAR{}/peaklists/two_source_variance/18569_{}.txt", "NCOCX", "normal", parameters_two_source_variance, (70,30), 0, "2"),
])
def test_simulated_peaklists(from_path, to_path, test_path, spectrum_name, distribution_name, parameters, plsplit, seed, nmrstar_version):
    from_path = from_path.format(nmrstar_version)
    to_path = to_path.format(nmrstar_version, spectrum_name)
    test_path = test_path.format(nmrstar_version, spectrum_name)

    noise_generator = NoiseGenerator(parameters=parameters,
                                     distribution_name=distribution_name,
                                     seed=seed)

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
        template_peaklist = infile.read()

    with open(to_path.format(spectrum_name)) as infile:
        generated_peaklist = infile.read()

    assert template_peaklist == generated_peaklist