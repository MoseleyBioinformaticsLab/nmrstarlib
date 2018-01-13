import os
import shutil
import pytest

import nmrstarlib
from nmrstarlib.converter import Converter
from nmrstarlib.translator import StarFileToStarFile


def teardown_module(module, paths=(
        "tests/example_data/NMRSTAR3/tmp",
        "tests/example_data/NMRSTAR2/tmp",
        "tests/example_data/CIF/tmp")):
    for path in paths:
        if os.path.exists(path):
            shutil.rmtree(path)

@pytest.mark.parametrize("from_path,to_path,from_format,to_format", [
    # one-to-one file conversions
    ("tests/example_data/NMRSTAR3/bmr18569.str", "tests/example_data/NMRSTAR3/tmp/json/bmr18569.json", "nmrstar", "json"),
    ("tests/example_data/NMRSTAR2/bmr18569.str", "tests/example_data/NMRSTAR2/tmp/json/bmr18569.json", "nmrstar", "json"),
    ("tests/example_data/CIF/2rpv.cif",          "tests/example_data/CIF/tmp/json/2rpv.json",          "cif",     "json"),

    ("tests/example_data/NMRSTAR3/bmr18569.str", "tests/example_data/NMRSTAR3/tmp/json/bmr18569.json.gz", "nmrstar", "json"),
    ("tests/example_data/NMRSTAR2/bmr18569.str", "tests/example_data/NMRSTAR2/tmp/json/bmr18569.json.gz", "nmrstar", "json"),
    ("tests/example_data/CIF/2rpv.cif",          "tests/example_data/CIF/tmp/json/2rpv.json.gz",          "cif",     "json"),

    ("tests/example_data/NMRSTAR3/bmr18569.str", "tests/example_data/NMRSTAR3/tmp/json/bmr18569.json.bz2", "nmrstar", "json"),
    ("tests/example_data/NMRSTAR2/bmr18569.str", "tests/example_data/NMRSTAR2/tmp/json/bmr18569.json.bz2", "nmrstar", "json"),
    ("tests/example_data/CIF/2rpv.cif",          "tests/example_data/CIF/tmp/json/2rpv.json.bz2",           "cif", "json"),

    ("tests/example_data/NMRSTAR3/tmp/json/bmr18569.json", "tests/example_data/NMRSTAR3/tmp/nmrstar/bmr18569.str", "json", "nmrstar"),
    ("tests/example_data/NMRSTAR2/tmp/json/bmr18569.json", "tests/example_data/NMRSTAR2/tmp/nmrstar/bmr18569.str", "json", "nmrstar"),
    ("tests/example_data/CIF/tmp/json/2rpv.json",          "tests/example_data/CIF/tmp/cif/2rpv.cif",              "json", "cif"),

    ("tests/example_data/NMRSTAR3/tmp/json/bmr18569.json.gz", "tests/example_data/NMRSTAR3/tmp/nmrstar/gz/bmr18569.str", "json", "nmrstar"),
    ("tests/example_data/NMRSTAR2/tmp/json/bmr18569.json.gz", "tests/example_data/NMRSTAR2/tmp/nmrstar/gz/bmr18569.str", "json", "nmrstar"),
    ("tests/example_data/CIF/tmp/json/2rpv.json.gz",          "tests/example_data/CIF/tmp/cif/gz/2rpv.cif",              "json", "cif"),

    ("tests/example_data/NMRSTAR3/tmp/json/bmr18569.json.gz", "tests/example_data/NMRSTAR3/tmp/nmrstar/gz/bmr18569.str.gz", "json", "nmrstar"),
    ("tests/example_data/NMRSTAR2/tmp/json/bmr18569.json.gz", "tests/example_data/NMRSTAR2/tmp/nmrstar/gz/bmr18569.str.gz", "json", "nmrstar"),
    ("tests/example_data/CIF/tmp/json/2rpv.json.gz",          "tests/example_data/CIF/tmp/cif/gz/2rpv.cif.gz",              "json", "cif"),

    ("tests/example_data/NMRSTAR3/tmp/json/bmr18569.json.gz", "tests/example_data/NMRSTAR3/tmp/nmrstar/gz/bmr18569.str.bz2", "json", "nmrstar"),
    ("tests/example_data/NMRSTAR2/tmp/json/bmr18569.json.gz", "tests/example_data/NMRSTAR2/tmp/nmrstar/gz/bmr18569.str.bz2", "json", "nmrstar"),
    ("tests/example_data/CIF/tmp/json/2rpv.json.gz",          "tests/example_data/CIF/tmp/cif/gz/2rpv.cif.bz2",              "json", "cif"),

    ("tests/example_data/NMRSTAR3/tmp/json/bmr18569.json.bz2", "tests/example_data/NMRSTAR3/tmp/nmrstar/bz2/bmr18569.str", "json", "nmrstar"),
    ("tests/example_data/NMRSTAR2/tmp/json/bmr18569.json.bz2", "tests/example_data/NMRSTAR2/tmp/nmrstar/bz2/bmr18569.str", "json", "nmrstar"),
    ("tests/example_data/CIF/tmp/json/2rpv.json.bz2",          "tests/example_data/CIF/tmp/cif/bz2/2rpv.cif",              "json", "cif"),

    ("tests/example_data/NMRSTAR3/tmp/json/bmr18569.json.bz2", "tests/example_data/NMRSTAR3/tmp/nmrstar/bz2/bmr18569.str.gz", "json", "nmrstar"),
    ("tests/example_data/NMRSTAR2/tmp/json/bmr18569.json.bz2", "tests/example_data/NMRSTAR2/tmp/nmrstar/bz2/bmr18569.str.gz", "json", "nmrstar"),
    ("tests/example_data/CIF/tmp/json/2rpv.json.bz2",          "tests/example_data/CIF/tmp/cif/bz2/2rpv.cif.gz",              "json", "cif"),

    ("tests/example_data/NMRSTAR3/tmp/json/bmr18569.json.bz2", "tests/example_data/NMRSTAR3/tmp/nmrstar/bz2/bmr18569.str.bz2", "json", "nmrstar"),
    ("tests/example_data/NMRSTAR2/tmp/json/bmr18569.json.bz2", "tests/example_data/NMRSTAR2/tmp/nmrstar/bz2/bmr18569.str.bz2", "json", "nmrstar"),
    ("tests/example_data/CIF/tmp/json/2rpv.json.bz2",          "tests/example_data/CIF/tmp/cif/bz2/2rpv.cif.bz2",              "json", "cif"),

    # many-to-many file conversions
    ("tests/example_data/NMRSTAR3/starfiles_directory", "tests/example_data/NMRSTAR3/tmp/json/dir/starfiles_files_json", "nmrstar", "json"),
    ("tests/example_data/NMRSTAR2/starfiles_directory", "tests/example_data/NMRSTAR2/tmp/json/dir/starfiles_files_json", "nmrstar", "json"),
    ("tests/example_data/CIF/ciffiles_directory",       "tests/example_data/CIF/tmp/json/dir/ciffiles_files_json",       "cif",     "json"),

    ("tests/example_data/NMRSTAR3/starfiles_directory", "tests/example_data/NMRSTAR3/tmp/json/dir/starfiles_files_json.zip", "nmrstar", "json"),
    ("tests/example_data/NMRSTAR2/starfiles_directory", "tests/example_data/NMRSTAR2/tmp/json/dir/starfiles_files_json.zip", "nmrstar", "json"),
    ("tests/example_data/CIF/ciffiles_directory",       "tests/example_data/CIF/tmp/json/dir/ciffiles_files_json.zip",       "cif",     "json"),

    ("tests/example_data/NMRSTAR3/starfiles_directory", "tests/example_data/NMRSTAR3/tmp/json/dir/starfiles_files_json.tar", "nmrstar", "json"),
    ("tests/example_data/NMRSTAR2/starfiles_directory", "tests/example_data/NMRSTAR2/tmp/json/dir/starfiles_files_json.tar", "nmrstar", "json"),
    ("tests/example_data/CIF/ciffiles_directory",       "tests/example_data/CIF/tmp/json/dir/ciffiles_files_json.tar",       "cif",     "json"),

    ("tests/example_data/NMRSTAR3/starfiles_directory", "tests/example_data/NMRSTAR3/tmp/json/dir/starfiles_files_json.tar.gz", "nmrstar", "json"),
    ("tests/example_data/NMRSTAR2/starfiles_directory", "tests/example_data/NMRSTAR2/tmp/json/dir/starfiles_files_json.tar.gz", "nmrstar", "json"),
    ("tests/example_data/CIF/ciffiles_directory",       "tests/example_data/CIF/tmp/json/dir/ciffiles_files_json.tar.gz",       "cif",     "json"),

    ("tests/example_data/NMRSTAR3/starfiles_directory", "tests/example_data/NMRSTAR3/tmp/json/dir/starfiles_files_json.tar.bz2", "nmrstar", "json"),
    ("tests/example_data/NMRSTAR2/starfiles_directory", "tests/example_data/NMRSTAR2/tmp/json/dir/starfiles_files_json.tar.bz2", "nmrstar", "json"),
    ("tests/example_data/CIF/ciffiles_directory",       "tests/example_data/CIF/tmp/json/dir/ciffiles_files_json.tar.bz2",       "cif",     "json"),

    ("tests/example_data/NMRSTAR3/tmp/json/dir/starfiles_files_json.zip", "tests/example_data/NMRSTAR3/tmp/nmrstar/zip/starfiles_nmrstar", "json", "nmrstar"),
    ("tests/example_data/NMRSTAR2/tmp/json/dir/starfiles_files_json.zip", "tests/example_data/NMRSTAR2/tmp/nmrstar/zip/starfiles_nmrstar", "json", "nmrstar"),
    ("tests/example_data/CIF/tmp/json/dir/ciffiles_files_json.zip",       "tests/example_data/CIF/tmp/cif/zip/ciffiles_cif",               "json", "cif"),

    ("tests/example_data/NMRSTAR3/tmp/json/dir/starfiles_files_json.zip", "tests/example_data/NMRSTAR3/tmp/nmrstar/zip/starfiles_nmrstar.zip", "json", "nmrstar"),
    ("tests/example_data/NMRSTAR2/tmp/json/dir/starfiles_files_json.zip", "tests/example_data/NMRSTAR2/tmp/nmrstar/zip/starfiles_nmrstar.zip", "json", "nmrstar"),
    ("tests/example_data/CIF/tmp/json/dir/ciffiles_files_json.zip",       "tests/example_data/CIF/tmp/cif/zip/starfiles_cif.zip",              "json", "cif"),

    ("tests/example_data/NMRSTAR3/tmp/json/dir/starfiles_files_json.zip", "tests/example_data/NMRSTAR3/tmp/nmrstar/zip/starfiles_nmrstar.tar", "json", "nmrstar"),
    ("tests/example_data/NMRSTAR2/tmp/json/dir/starfiles_files_json.zip", "tests/example_data/NMRSTAR2/tmp/nmrstar/zip/starfiles_nmrstar.tar", "json", "nmrstar"),
    ("tests/example_data/CIF/tmp/json/dir/ciffiles_files_json.zip",       "tests/example_data/CIF/tmp/cif/zip/ciffiles_cif.tar",               "json", "cif"),

    ("tests/example_data/NMRSTAR3/tmp/json/dir/starfiles_files_json.zip", "tests/example_data/NMRSTAR3/tmp/nmrstar/zip/starfiles_nmrstar.tar.gz", "json", "nmrstar"),
    ("tests/example_data/NMRSTAR2/tmp/json/dir/starfiles_files_json.zip", "tests/example_data/NMRSTAR2/tmp/nmrstar/zip/starfiles_nmrstar.tar.gz", "json", "nmrstar"),
    ("tests/example_data/CIF/tmp/json/dir/ciffiles_files_json.zip",       "tests/example_data/CIF/tmp/cif/zip/ciffiles_cif.tar.gz",               "json", "cif"),

    ("tests/example_data/NMRSTAR3/tmp/json/dir/starfiles_files_json.zip", "tests/example_data/NMRSTAR3/tmp/nmrstar/zip/starfiles_nmrstar.tar.bz2", "json", "nmrstar"),
    ("tests/example_data/NMRSTAR2/tmp/json/dir/starfiles_files_json.zip", "tests/example_data/NMRSTAR2/tmp/nmrstar/zip/starfiles_nmrstar.tar.bz2", "json", "nmrstar"),
    ("tests/example_data/CIF/tmp/json/dir/ciffiles_files_json.zip",       "tests/example_data/CIF/tmp/cif/zip/ciffiles_cif.tar.bz2",               "json", "cif"),

    ("tests/example_data/NMRSTAR3/tmp/json/dir/starfiles_files_json.tar", "tests/example_data/NMRSTAR3/tmp/nmrstar/tar/starfiles_nmrstar", "json", "nmrstar"),
    ("tests/example_data/NMRSTAR2/tmp/json/dir/starfiles_files_json.tar", "tests/example_data/NMRSTAR2/tmp/nmrstar/tar/starfiles_nmrstar", "json", "nmrstar"),
    ("tests/example_data/CIF/tmp/json/dir/ciffiles_files_json.tar",       "tests/example_data/CIF/tmp/cif/tar/ciffiles_cif",               "json", "cif"),

    ("tests/example_data/NMRSTAR3/tmp/json/dir/starfiles_files_json.tar", "tests/example_data/NMRSTAR3/tmp/nmrstar/tar/starfiles_nmrstar.zip", "json", "nmrstar"),
    ("tests/example_data/NMRSTAR2/tmp/json/dir/starfiles_files_json.tar", "tests/example_data/NMRSTAR2/tmp/nmrstar/tar/starfiles_nmrstar.zip", "json", "nmrstar"),
    ("tests/example_data/CIF/tmp/json/dir/ciffiles_files_json.tar",       "tests/example_data/CIF/tmp/cif/tar/ciffiles_cif.zip",               "json", "cif"),

    ("tests/example_data/NMRSTAR3/tmp/json/dir/starfiles_files_json.tar", "tests/example_data/NMRSTAR3/tmp/nmrstar/tar/starfiles_nmrstar.tar", "json", "nmrstar"),
    ("tests/example_data/NMRSTAR2/tmp/json/dir/starfiles_files_json.tar", "tests/example_data/NMRSTAR2/tmp/nmrstar/tar/starfiles_nmrstar.tar", "json", "nmrstar"),
    ("tests/example_data/CIF/tmp/json/dir/ciffiles_files_json.tar",       "tests/example_data/CIF/tmp/cif/tar/ciffiles_cif.tar",               "json", "cif"),

    ("tests/example_data/NMRSTAR3/tmp/json/dir/starfiles_files_json.tar", "tests/example_data/NMRSTAR3/tmp/nmrstar/tar/starfiles_nmrstar.tar.gz", "json", "nmrstar"),
    ("tests/example_data/NMRSTAR2/tmp/json/dir/starfiles_files_json.tar", "tests/example_data/NMRSTAR2/tmp/nmrstar/tar/starfiles_nmrstar.tar.gz", "json", "nmrstar"),
    ("tests/example_data/CIF/tmp/json/dir/ciffiles_files_json.tar",       "tests/example_data/CIF/tmp/cif/tar/ciffiles_cif.tar.gz",               "json", "cif"),

    ("tests/example_data/NMRSTAR3/tmp/json/dir/starfiles_files_json.tar", "tests/example_data/NMRSTAR3/tmp/nmrstar/tar/starfiles_nmrstar.tar.bz2", "json", "nmrstar"),
    ("tests/example_data/NMRSTAR2/tmp/json/dir/starfiles_files_json.tar", "tests/example_data/NMRSTAR2/tmp/nmrstar/tar/starfiles_nmrstar.tar.bz2", "json", "nmrstar"),
    ("tests/example_data/CIF/tmp/json/dir/ciffiles_files_json.tar",       "tests/example_data/CIF/tmp/cif/tar/ciffiles_cif.tar.bz2",               "json", "cif"),

    ("tests/example_data/NMRSTAR3/tmp/json/dir/starfiles_files_json.tar.gz", "tests/example_data/NMRSTAR3/tmp/nmrstar/targz/starfiles_nmrstar", "json", "nmrstar"),
    ("tests/example_data/NMRSTAR2/tmp/json/dir/starfiles_files_json.tar.gz", "tests/example_data/NMRSTAR2/tmp/nmrstar/targz/starfiles_nmrstar", "json", "nmrstar"),
    ("tests/example_data/CIF/tmp/json/dir/ciffiles_files_json.tar.gz",       "tests/example_data/CIF/tmp/cif/targz/ciffiles_cif",               "json", "cif"),

    ("tests/example_data/NMRSTAR3/tmp/json/dir/starfiles_files_json.tar.gz", "tests/example_data/NMRSTAR3/tmp/nmrstar/targz/starfiles_nmrstar.zip", "json", "nmrstar"),
    ("tests/example_data/NMRSTAR2/tmp/json/dir/starfiles_files_json.tar.gz", "tests/example_data/NMRSTAR2/tmp/nmrstar/targz/starfiles_nmrstar.zip", "json", "nmrstar"),
    ("tests/example_data/CIF/tmp/json/dir/ciffiles_files_json.tar.gz",       "tests/example_data/CIF/tmp/cif/targz/ciffiles_cif.zip",               "json", "cif"),

    ("tests/example_data/NMRSTAR3/tmp/json/dir/starfiles_files_json.tar.gz", "tests/example_data/NMRSTAR3/tmp/nmrstar/targz/starfiles_nmrstar.tar", "json", "nmrstar"),
    ("tests/example_data/NMRSTAR2/tmp/json/dir/starfiles_files_json.tar.gz", "tests/example_data/NMRSTAR2/tmp/nmrstar/targz/starfiles_nmrstar.tar", "json", "nmrstar"),
    ("tests/example_data/CIF/tmp/json/dir/ciffiles_files_json.tar.gz",       "tests/example_data/CIF/tmp/cif/targz/ciffiles_cif.tar",               "json", "cif"),

    ("tests/example_data/NMRSTAR3/tmp/json/dir/starfiles_files_json.tar.gz", "tests/example_data/NMRSTAR3/tmp/nmrstar/targz/starfiles_nmrstar.tar.gz", "json", "nmrstar"),
    ("tests/example_data/NMRSTAR2/tmp/json/dir/starfiles_files_json.tar.gz", "tests/example_data/NMRSTAR2/tmp/nmrstar/targz/starfiles_nmrstar.tar.gz", "json", "nmrstar"),
    ("tests/example_data/CIF/tmp/json/dir/ciffiles_files_json.tar.gz",       "tests/example_data/CIF/tmp/cif/targz/ciffiles_cif.tar.gz",               "json", "cif"),

    ("tests/example_data/NMRSTAR3/tmp/json/dir/starfiles_files_json.tar.gz", "tests/example_data/NMRSTAR3/tmp/nmrstar/targz/starfiles_nmrstar.tar.bz2", "json", "nmrstar"),
    ("tests/example_data/NMRSTAR2/tmp/json/dir/starfiles_files_json.tar.gz", "tests/example_data/NMRSTAR2/tmp/nmrstar/targz/starfiles_nmrstar.tar.bz2", "json", "nmrstar"),
    ("tests/example_data/CIF/tmp/json/dir/ciffiles_files_json.tar.gz",       "tests/example_data/CIF/tmp/cif/targz/ciffiles_cif.tar.bz2",               "json", "cif"),

    ("tests/example_data/NMRSTAR3/tmp/json/dir/starfiles_files_json.tar.bz2", "tests/example_data/NMRSTAR3/tmp/nmrstar/tarbz2/starfiles_nmrstar", "json", "nmrstar"),
    ("tests/example_data/NMRSTAR2/tmp/json/dir/starfiles_files_json.tar.bz2", "tests/example_data/NMRSTAR2/tmp/nmrstar/tarbz2/starfiles_nmrstar", "json", "nmrstar"),
    ("tests/example_data/CIF/tmp/json/dir/ciffiles_files_json.tar.bz2",       "tests/example_data/CIF/tmp/cif/tarbz2/ciffiles_cif",               "json", "cif"),

    ("tests/example_data/NMRSTAR3/tmp/json/dir/starfiles_files_json.tar.bz2", "tests/example_data/NMRSTAR3/tmp/nmrstar/tarbz2/starfiles_nmrstar.zip", "json", "nmrstar"),
    ("tests/example_data/NMRSTAR2/tmp/json/dir/starfiles_files_json.tar.bz2", "tests/example_data/NMRSTAR2/tmp/nmrstar/tarbz2/starfiles_nmrstar.zip", "json", "nmrstar"),
    ("tests/example_data/CIF/tmp/json/dir/ciffiles_files_json.tar.bz2",       "tests/example_data/CIF/tmp/cif/tarbz2/ciffiles_cif.zip",               "json", "cif"),

    ("tests/example_data/NMRSTAR3/tmp/json/dir/starfiles_files_json.tar.bz2", "tests/example_data/NMRSTAR3/tmp/nmrstar/tarbz2/starfiles_nmrstar.tar", "json", "nmrstar"),
    ("tests/example_data/NMRSTAR2/tmp/json/dir/starfiles_files_json.tar.bz2", "tests/example_data/NMRSTAR2/tmp/nmrstar/tarbz2/starfiles_nmrstar.tar", "json", "nmrstar"),
    ("tests/example_data/CIF/tmp/json/dir/ciffiles_files_json.tar.bz2",       "tests/example_data/CIF/tmp/cif/tarbz2/ciffiles_cif.tar",               "json", "cif"),

    ("tests/example_data/NMRSTAR3/tmp/json/dir/starfiles_files_json.tar.bz2", "tests/example_data/NMRSTAR3/tmp/nmrstar/tarbz2/starfiles_nmrstar.tar.gz", "json", "nmrstar"),
    ("tests/example_data/NMRSTAR2/tmp/json/dir/starfiles_files_json.tar.bz2", "tests/example_data/NMRSTAR2/tmp/nmrstar/tarbz2/starfiles_nmrstar.tar.gz", "json", "nmrstar"),
    ("tests/example_data/CIF/tmp/json/dir/ciffiles_files_json.tar.bz2",       "tests/example_data/CIF/tmp/cif/tarbz2/ciffiles_cif.tar.gz",               "json", "cif"),

    ("tests/example_data/NMRSTAR3/tmp/json/dir/starfiles_files_json.tar.bz2", "tests/example_data/NMRSTAR3/tmp/nmrstar/tarbz2/starfiles_nmrstar.tar.bz2", "json", "nmrstar"),
    ("tests/example_data/NMRSTAR2/tmp/json/dir/starfiles_files_json.tar.bz2", "tests/example_data/NMRSTAR2/tmp/nmrstar/tarbz2/starfiles_nmrstar.tar.bz2", "json", "nmrstar"),
    ("tests/example_data/CIF/tmp/json/dir/ciffiles_files_json.tar.bz2",       "tests/example_data/CIF/tmp/cif/tarbz2/ciffiles_cif.tar.bz2",               "json", "cif")
])
def test_converter_module(from_path, to_path, from_format, to_format):
    nmrstar_file_translator = StarFileToStarFile(from_path=from_path,
                                                 to_path=to_path,
                                                 from_format=from_format,
                                                 to_format=to_format)
    converter = Converter(file_generator=nmrstar_file_translator)
    converter.convert()

    starfile_generator = nmrstarlib.read_files(to_path)
    starfiles_list = list(starfile_generator)
    starfiles_ids_set = set(sf.id for sf in starfiles_list)
    assert starfiles_ids_set.issubset({"15000", "18569", "2RPV", "2FRG"})
