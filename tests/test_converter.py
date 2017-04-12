import os
import shutil
import pytest

from nmrstarlib import nmrstarlib
from nmrstarlib.converter import Converter
from nmrstarlib.translator import StarFileToStarFile


def teardown_module(module):
    if os.path.exists("tests/example_data/NMRSTAR3/tmp"):
        shutil.rmtree("tests/example_data/NMRSTAR3/tmp")
    if os.path.exists("tests/example_data/NMRSTAR2/tmp"):
        shutil.rmtree("tests/example_data/NMRSTAR2/tmp")


@pytest.mark.parametrize("from_path,to_path,from_format,to_format", [
    ("tests/example_data/NMRSTAR3/bmr18569.str", "tests/example_data/NMRSTAR3/tmp/bmr18569.json", "nmrstar", "json"),
    ("tests/example_data/NMRSTAR2/bmr18569.str", "tests/example_data/NMRSTAR2/tmp/bmr18569.json", "nmrstar", "json"),
    ("tests/example_data/NMRSTAR3/tmp/bmr18569.json", "tests/example_data/NMRSTAR3/tmp/bmr18569.str", "json", "nmrstar"),
    ("tests/example_data/NMRSTAR2/tmp/bmr18569.json", "tests/example_data/NMRSTAR2/tmp/bmr18569.str", "json", "nmrstar")
])
def test_one_to_one_conversion(from_path, to_path, from_format, to_format):
    nmrstar_file_translator = StarFileToStarFile(from_path=from_path,
                                                 to_path=to_path,
                                                 from_format=from_format,
                                                 to_format=to_format)
    converter = Converter(file_generator=nmrstar_file_translator)
    converter.convert()

    starfile_generator = nmrstarlib.read_files(to_path)
    starfile = next(starfile_generator)
    assert starfile.bmrbid == "18569"


@pytest.mark.parametrize("from_path,to_path,from_format,to_format", [
    ("tests/example_data/NMRSTAR3/starfiles_directory", "tests/example_data/NMRSTAR3/tmp/starfiles_directory_json", "nmrstar", "json"),
    ("tests/example_data/NMRSTAR2/starfiles_directory", "tests/example_data/NMRSTAR2/tmp/starfiles_directory_json", "nmrstar", "json"),
    ("tests/example_data/NMRSTAR3/tmp/starfiles_directory_json", "tests/example_data/NMRSTAR3/tmp/starfiles_directory_nmrstar", "json", "nmrstar"),
    ("tests/example_data/NMRSTAR2/tmp/starfiles_directory_json", "tests/example_data/NMRSTAR2/tmp/starfiles_directory_nmrstar", "json", "nmrstar")

])
def test_many_to_many_conversion(from_path, to_path, from_format, to_format):
    nmrstar_file_translator = StarFileToStarFile(from_path=from_path,
                                                 to_path=to_path,
                                                 from_format=from_format,
                                                 to_format=to_format)
    converter = Converter(file_generator=nmrstar_file_translator)
    converter.convert()

    starfile_generator = nmrstarlib.read_files(to_path)
    starfiles_list = list(starfile_generator)
    starfiles_ids_set = set(sf.bmrbid for sf in starfiles_list)
    assert starfiles_ids_set == {"15000", "18569"}
