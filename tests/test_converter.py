import shutil
from nmrstarlib import nmrstarlib
from nmrstarlib.converter import Converter


def teardown_module(module):
    shutil.rmtree("tests/example_data/NMRSTAR3/tmp")
    shutil.rmtree("tests/example_data/NMRSTAR2/tmp")


def test_from_nmrstar_to_json_single_file():
    converter = Converter(from_path="tests/example_data/NMRSTAR3/bmr18569.str",
                          to_path="tests/example_data/NMRSTAR3/tmp/bmr18569.json",
                          from_format="nmrstar",
                          to_format="json")
    converter.convert()
    converter = Converter(from_path="tests/example_data/NMRSTAR2/bmr18569.str",
                          to_path="tests/example_data/NMRSTAR2/tmp/bmr18569.json",
                          from_format="nmrstar",
                          to_format="json")
    converter.convert()
    starfile_generator = nmrstarlib.read_files("tests/example_data/NMRSTAR3/tmp/bmr18569.json",
                                               "tests/example_data/NMRSTAR2/tmp/bmr18569.json")
    starfile1 = next(starfile_generator)
    starfile2 = next(starfile_generator)
    assert starfile1.bmrbid == "18569" and starfile2.bmrbid == "18569"


def test_from_json_to_nmrstar_single_file():
    converter = Converter(from_path="tests/example_data/NMRSTAR3/tmp/bmr18569.json",
                          to_path="tests/example_data/NMRSTAR3/tmp/bmr18569.str",
                          from_format="json",
                          to_format="nmrstar")
    converter.convert()
    converter = Converter(from_path="tests/example_data/NMRSTAR2/tmp/bmr18569.json",
                          to_path="tests/example_data/NMRSTAR2/tmp/bmr18569.str",
                          from_format="json",
                          to_format="nmrstar")
    converter.convert()
    starfile_generator = nmrstarlib.read_files("tests/example_data/NMRSTAR3/tmp/bmr18569.str",
                                               "tests/example_data/NMRSTAR2/tmp/bmr18569.str")
    starfile1 = next(starfile_generator)
    starfile2 = next(starfile_generator)
    assert starfile1.bmrbid == "18569" and starfile2.bmrbid == "18569"


def test_from_nmrstar_to_json_directory():
    converter = Converter(from_path="tests/example_data/NMRSTAR3/starfiles_directory",
                          to_path="tests/example_data/NMRSTAR3/tmp/starfiles_directory_json",
                          from_format="nmrstar",
                          to_format="json")
    converter.convert()
    converter = Converter(from_path="tests/example_data/NMRSTAR2/starfiles_directory",
                          to_path="tests/example_data/NMRSTAR2/tmp/starfiles_directory_json",
                          from_format="nmrstar",
                          to_format="json")
    converter.convert()
    starfile_generator = nmrstarlib.read_files("tests/example_data/NMRSTAR3/tmp/starfiles_directory_json",
                                               "tests/example_data/NMRSTAR2/tmp/starfiles_directory_json")
    starfiles_list = list(starfile_generator)
    starfiles_ids_set = set(sf.bmrbid for sf in starfiles_list)
    assert starfiles_ids_set == {"15000", "18569"}


def test_from_json_to_nmrstar_directory():
    converter = Converter(from_path="tests/example_data/NMRSTAR3/tmp/starfiles_directory_json",
                          to_path="tests/example_data/NMRSTAR3/tmp/starfiles_directory_nmrstar",
                          from_format="json",
                          to_format="nmrstar")
    converter.convert()
    converter = Converter(from_path="tests/example_data/NMRSTAR2/tmp/starfiles_directory_json",
                          to_path="tests/example_data/NMRSTAR2/tmp/starfiles_directory_nmrstar",
                          from_format="json",
                          to_format="nmrstar")
    converter.convert()
    starfile_generator = nmrstarlib.read_files("tests/example_data/NMRSTAR3/tmp/starfiles_directory_nmrstar",
                                               "tests/example_data/NMRSTAR2/tmp/starfiles_directory_nmrstar")
    starfiles_list = list(starfile_generator)
    starfiles_ids_set = set(sf.bmrbid for sf in starfiles_list)
    assert starfiles_ids_set == {"15000", "18569"}
