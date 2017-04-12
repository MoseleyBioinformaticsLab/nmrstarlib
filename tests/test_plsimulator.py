import os
import shutil
import pytest

from nmrstarlib.converter import Converter
from nmrstarlib.translator import StarFileToPeakList
from nmrstarlib.noise import RandomNormalNoiseGenerator


def teardown_module(module):
    if os.path.exists("tests/example_data/NMRSTAR3/tmp"):
        shutil.rmtree("tests/example_data/NMRSTAR3/tmp")
    if os.path.exists("tests/example_data/NMRSTAR2/tmp"):
        shutil.rmtree("tests/example_data/NMRSTAR2/tmp")


spectrum_names = ("CANCO", "CANCOCX", "CBCANH", "CBCAcoNH", "CCcoNH", "HBHAcoNH", "HNCA", "HNCACB", "HNCO", "HNcaCO",
                  "HNcoCA", "HNcoCACB", "HSQC", "HccoNH", "NCA", "NCACX", "NCO", "NCOCX")

noise_generator = RandomNormalNoiseGenerator({"H_mean": [0], "C_mean": [0], "N_mean": [0],
                                              "H_std": [0], "C_std": [0], "N_std": [0]})

noise_generator_with_split = RandomNormalNoiseGenerator({"H_mean": [0, 0], "C_mean": [0, 0], "N_mean": [0, 0],
                                                         "H_std": [0, 0], "C_std": [0, 0], "N_std": [0, 0]})


@pytest.mark.parametrize("spectrum_names_tuple,noise_generator,plsplit", [
    (spectrum_names, None, None),
    (spectrum_names, noise_generator, None),
    (spectrum_names, noise_generator_with_split, (70, 30))
])
def test_simulated_peaklists(spectrum_names_tuple, noise_generator, plsplit):

    if spectrum_names_tuple is not None:
        for spectrum_name in spectrum_names_tuple:

            peaklist_file_translator = StarFileToPeakList(from_path="tests/example_data/NMRSTAR3/bmr18569.str",
                                                          to_path="tests/example_data/NMRSTAR3/tmp/18569_{}.txt".format(spectrum_name),
                                                          from_format="nmrstar",
                                                          to_format="sparky",
                                                          spectrum_name=spectrum_name,
                                                          noise_generator=noise_generator,
                                                          plsplit=plsplit,
                                                          nmrstar_version="3")
            nmrstar_to_peaklist_converter = Converter(file_generator=peaklist_file_translator)
            nmrstar_to_peaklist_converter.convert()

            peaklist_file_translator = StarFileToPeakList(from_path="tests/example_data/NMRSTAR2/bmr18569.str",
                                                          to_path="tests/example_data/NMRSTAR2/tmp/18569_{}.txt".format(spectrum_name),
                                                          from_format="nmrstar",
                                                          to_format="sparky",
                                                          spectrum_name=spectrum_name,
                                                          noise_generator=noise_generator,
                                                          plsplit=plsplit,
                                                          nmrstar_version="2")
            nmrstar_to_peaklist_converter = Converter(file_generator=peaklist_file_translator)
            nmrstar_to_peaklist_converter.convert()

            with open("tests/example_data/NMRSTAR3/peaklists/18569_{}.txt".format(spectrum_name)) as infile:
                template_peaklist1  = infile.read()
            with open("tests/example_data/NMRSTAR3/tmp/18569_{}.txt".format(spectrum_name)) as infile:
                generated_peaklist1 = infile.read()

            with open("tests/example_data/NMRSTAR2/peaklists/18569_{}.txt".format(spectrum_name)) as infile:
                template_peaklist2  = infile.read()
            with open("tests/example_data/NMRSTAR2/tmp/18569_{}.txt".format(spectrum_name)) as infile:
                generated_peaklist2 = infile.read()

            assert template_peaklist1 == generated_peaklist1
            assert template_peaklist2 == generated_peaklist2