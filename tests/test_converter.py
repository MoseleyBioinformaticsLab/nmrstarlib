import shutil
from nmrstarlib import nmrstarlib
from nmrstarlib.converter import Converter


def teardown_module(module):
    shutil.rmtree("tests/example_data/tmp")


def test_from_nmrstar_to_json_single_file():
    converter = Converter(from_path="tests/example_data/bmr18569.str",
                          to_path="tests/example_data/tmp/bmr18569.json",
                          from_format="nmrstar",
                          to_format="json")
    converter.convert()
    starfile_generator = nmrstarlib.read_files("tests/example_data/tmp/bmr18569.json")
    starfile = next(starfile_generator)
    assert starfile.bmrbid == "18569"


def test_from_json_to_nmrstar_single_file():
    converter = Converter(from_path="tests/example_data/tmp/bmr18569.json",
                          to_path="tests/example_data/tmp/bmr18569.str",
                          from_format="json",
                          to_format="nmrstar")
    converter.convert()
    starfile_generator = nmrstarlib.read_files("tests/example_data/tmp/bmr18569.str")
    starfile = next(starfile_generator)
    assert starfile.bmrbid == "18569"


def test_from_nmrstar_to_json_directory():
    converter = Converter(from_path="tests/example_data/starfiles_directory",
                          to_path="tests/example_data/tmp/starfiles_directory_json",
                          from_format="nmrstar",
                          to_format="json")
    converter.convert()
    starfile_generator = nmrstarlib.read_files("tests/example_data/tmp/starfiles_directory_json")
    starfile1 = next(starfile_generator)
    starfile2 = next(starfile_generator)
    assert starfile1.bmrbid == "15000" and starfile2.bmrbid == "18569"


def test_from_json_to_nmrstar_directory():
    converter = Converter(from_path="tests/example_data/tmp/starfiles_directory_json",
                          to_path="tests/example_data/tmp/starfiles_directory_nmrstar",
                          from_format="json",
                          to_format="nmrstar")
    converter.convert()
    starfile_generator = nmrstarlib.read_files("tests/example_data/tmp/starfiles_directory_nmrstar")
    starfile1 = next(starfile_generator)
    starfile2 = next(starfile_generator)
    assert starfile1.bmrbid == "15000" and starfile2.bmrbid == "18569"
