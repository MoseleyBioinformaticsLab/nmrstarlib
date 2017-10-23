import os
import shutil
import pytest

import nmrstarlib


def teardown_module(module):
    if os.path.exists("tests/example_data/NMRSTAR3/tmp"):
        shutil.rmtree("tests/example_data/NMRSTAR3/tmp")
    if os.path.exists("tests/example_data/NMRSTAR2/tmp"):
        shutil.rmtree("tests/example_data/NMRSTAR2/tmp")

@pytest.mark.parametrize("from_path,to_path,from_format,to_format", [
    # one-to-one file conversions
    ("tests/example_data/NMRSTAR3/bmr18569.str", "tests/example_data/NMRSTAR3/tmp/json/bmr18569.json", "nmrstar", "json"),
    ("tests/example_data/NMRSTAR2/bmr18569.str", "tests/example_data/NMRSTAR2/tmp/json/bmr18569.json", "nmrstar", "json"),
    ("tests/example_data/NMRSTAR3/bmr18569.str", "tests/example_data/NMRSTAR3/tmp/json/bmr18569.json.gz", "nmrstar", "json"),
    ("tests/example_data/NMRSTAR2/bmr18569.str", "tests/example_data/NMRSTAR2/tmp/json/bmr18569.json.gz", "nmrstar", "json"),
    ("tests/example_data/NMRSTAR3/bmr18569.str", "tests/example_data/NMRSTAR3/tmp/json/bmr18569.json.bz2", "nmrstar", "json"),
    ("tests/example_data/NMRSTAR2/bmr18569.str", "tests/example_data/NMRSTAR2/tmp/json/bmr18569.json.bz2", "nmrstar", "json"),
    ("tests/example_data/NMRSTAR3/tmp/json/bmr18569.json", "tests/example_data/NMRSTAR3/tmp/nmrstar/bmr18569.str", "json", "nmrstar"),
    ("tests/example_data/NMRSTAR2/tmp/json/bmr18569.json", "tests/example_data/NMRSTAR2/tmp/nmrstar/bmr18569.str", "json", "nmrstar"),
    ("tests/example_data/NMRSTAR3/tmp/json/bmr18569.json.gz", "tests/example_data/NMRSTAR3/tmp/nmrstar/gz/bmr18569.str", "json", "nmrstar"),
    ("tests/example_data/NMRSTAR2/tmp/json/bmr18569.json.gz", "tests/example_data/NMRSTAR2/tmp/nmrstar/gz/bmr18569.str", "json", "nmrstar"),
    ("tests/example_data/NMRSTAR3/tmp/json/bmr18569.json.gz", "tests/example_data/NMRSTAR3/tmp/nmrstar/gz/bmr18569.str.gz", "json", "nmrstar"),
    ("tests/example_data/NMRSTAR2/tmp/json/bmr18569.json.gz", "tests/example_data/NMRSTAR2/tmp/nmrstar/gz/bmr18569.str.gz", "json", "nmrstar"),
    ("tests/example_data/NMRSTAR3/tmp/json/bmr18569.json.gz", "tests/example_data/NMRSTAR3/tmp/nmrstar/gz/bmr18569.str.bz2", "json", "nmrstar"),
    ("tests/example_data/NMRSTAR2/tmp/json/bmr18569.json.gz", "tests/example_data/NMRSTAR2/tmp/nmrstar/gz/bmr18569.str.bz2", "json", "nmrstar"),
    ("tests/example_data/NMRSTAR3/tmp/json/bmr18569.json.bz2", "tests/example_data/NMRSTAR3/tmp/nmrstar/bz2/bmr18569.str", "json", "nmrstar"),
    ("tests/example_data/NMRSTAR2/tmp/json/bmr18569.json.bz2", "tests/example_data/NMRSTAR2/tmp/nmrstar/bz2/bmr18569.str", "json", "nmrstar"),
    ("tests/example_data/NMRSTAR3/tmp/json/bmr18569.json.bz2", "tests/example_data/NMRSTAR3/tmp/nmrstar/bz2/bmr18569.str.gz", "json", "nmrstar"),
    ("tests/example_data/NMRSTAR2/tmp/json/bmr18569.json.bz2", "tests/example_data/NMRSTAR2/tmp/nmrstar/bz2/bmr18569.str.gz", "json", "nmrstar"),
    ("tests/example_data/NMRSTAR3/tmp/json/bmr18569.json.bz2", "tests/example_data/NMRSTAR3/tmp/nmrstar/bz2/bmr18569.str.bz2", "json", "nmrstar"),
    ("tests/example_data/NMRSTAR2/tmp/json/bmr18569.json.bz2", "tests/example_data/NMRSTAR2/tmp/nmrstar/bz2/bmr18569.str.bz2", "json", "nmrstar"),
    # many-to-many file conversions
    ("tests/example_data/NMRSTAR3/starfiles_directory", "tests/example_data/NMRSTAR3/tmp/json/dir/starfiles_files_json", "nmrstar", "json"),
    ("tests/example_data/NMRSTAR2/starfiles_directory", "tests/example_data/NMRSTAR2/tmp/json/dir/starfiles_files_json", "nmrstar", "json"),
    ("tests/example_data/NMRSTAR3/starfiles_directory", "tests/example_data/NMRSTAR3/tmp/json/dir/starfiles_files_json.zip", "nmrstar", "json"),
    ("tests/example_data/NMRSTAR2/starfiles_directory", "tests/example_data/NMRSTAR2/tmp/json/dir/starfiles_files_json.zip", "nmrstar", "json"),
    ("tests/example_data/NMRSTAR3/starfiles_directory", "tests/example_data/NMRSTAR3/tmp/json/dir/starfiles_files_json.tar", "nmrstar", "json"),
    ("tests/example_data/NMRSTAR2/starfiles_directory", "tests/example_data/NMRSTAR2/tmp/json/dir/starfiles_files_json.tar", "nmrstar", "json"),
    ("tests/example_data/NMRSTAR3/starfiles_directory", "tests/example_data/NMRSTAR3/tmp/json/dir/starfiles_files_json.tar.gz", "nmrstar", "json"),
    ("tests/example_data/NMRSTAR2/starfiles_directory", "tests/example_data/NMRSTAR2/tmp/json/dir/starfiles_files_json.tar.gz", "nmrstar", "json"),
    ("tests/example_data/NMRSTAR3/starfiles_directory", "tests/example_data/NMRSTAR3/tmp/json/dir/starfiles_files_json.tar.bz2", "nmrstar", "json"),
    ("tests/example_data/NMRSTAR2/starfiles_directory", "tests/example_data/NMRSTAR2/tmp/json/dir/starfiles_files_json.tar.bz2", "nmrstar", "json"),
    ("tests/example_data/NMRSTAR3/tmp/json/dir/starfiles_files_json.zip", "tests/example_data/NMRSTAR3/tmp/nmrstar/zip/starfiles_nmrstar", "json", "nmrstar"),
    ("tests/example_data/NMRSTAR2/tmp/json/dir/starfiles_files_json.zip", "tests/example_data/NMRSTAR2/tmp/nmrstar/zip/starfiles_nmrstar", "json", "nmrstar"),
    ("tests/example_data/NMRSTAR3/tmp/json/dir/starfiles_files_json.zip", "tests/example_data/NMRSTAR3/tmp/nmrstar/zip/starfiles_nmrstar.zip", "json", "nmrstar"),
    ("tests/example_data/NMRSTAR2/tmp/json/dir/starfiles_files_json.zip", "tests/example_data/NMRSTAR2/tmp/nmrstar/zip/starfiles_nmrstar.zip", "json", "nmrstar"),
    ("tests/example_data/NMRSTAR3/tmp/json/dir/starfiles_files_json.zip", "tests/example_data/NMRSTAR3/tmp/nmrstar/zip/starfiles_nmrstar.tar", "json", "nmrstar"),
    ("tests/example_data/NMRSTAR2/tmp/json/dir/starfiles_files_json.zip", "tests/example_data/NMRSTAR2/tmp/nmrstar/zip/starfiles_nmrstar.tar", "json", "nmrstar"),
    ("tests/example_data/NMRSTAR3/tmp/json/dir/starfiles_files_json.zip", "tests/example_data/NMRSTAR3/tmp/nmrstar/zip/starfiles_nmrstar.tar.gz", "json", "nmrstar"),
    ("tests/example_data/NMRSTAR2/tmp/json/dir/starfiles_files_json.zip", "tests/example_data/NMRSTAR2/tmp/nmrstar/zip/starfiles_nmrstar.tar.gz", "json", "nmrstar"),
    ("tests/example_data/NMRSTAR3/tmp/json/dir/starfiles_files_json.zip", "tests/example_data/NMRSTAR3/tmp/nmrstar/zip/starfiles_nmrstar.tar.bz2", "json", "nmrstar"),
    ("tests/example_data/NMRSTAR2/tmp/json/dir/starfiles_files_json.zip", "tests/example_data/NMRSTAR2/tmp/nmrstar/zip/starfiles_nmrstar.tar.bz2", "json", "nmrstar"),
    ("tests/example_data/NMRSTAR3/tmp/json/dir/starfiles_files_json.tar", "tests/example_data/NMRSTAR3/tmp/nmrstar/tar/starfiles_nmrstar", "json", "nmrstar"),
    ("tests/example_data/NMRSTAR2/tmp/json/dir/starfiles_files_json.tar", "tests/example_data/NMRSTAR2/tmp/nmrstar/tar/starfiles_nmrstar", "json", "nmrstar"),
    ("tests/example_data/NMRSTAR3/tmp/json/dir/starfiles_files_json.tar", "tests/example_data/NMRSTAR3/tmp/nmrstar/tar/starfiles_nmrstar.zip", "json", "nmrstar"),
    ("tests/example_data/NMRSTAR2/tmp/json/dir/starfiles_files_json.tar", "tests/example_data/NMRSTAR2/tmp/nmrstar/tar/starfiles_nmrstar.zip", "json", "nmrstar"),
    ("tests/example_data/NMRSTAR3/tmp/json/dir/starfiles_files_json.tar", "tests/example_data/NMRSTAR3/tmp/nmrstar/tar/starfiles_nmrstar.tar", "json", "nmrstar"),
    ("tests/example_data/NMRSTAR2/tmp/json/dir/starfiles_files_json.tar", "tests/example_data/NMRSTAR2/tmp/nmrstar/tar/starfiles_nmrstar.tar", "json", "nmrstar"),
    ("tests/example_data/NMRSTAR3/tmp/json/dir/starfiles_files_json.tar", "tests/example_data/NMRSTAR3/tmp/nmrstar/tar/starfiles_nmrstar.tar.gz", "json", "nmrstar"),
    ("tests/example_data/NMRSTAR2/tmp/json/dir/starfiles_files_json.tar", "tests/example_data/NMRSTAR2/tmp/nmrstar/tar/starfiles_nmrstar.tar.gz", "json", "nmrstar"),
    ("tests/example_data/NMRSTAR3/tmp/json/dir/starfiles_files_json.tar", "tests/example_data/NMRSTAR3/tmp/nmrstar/tar/starfiles_nmrstar.tar.bz2", "json", "nmrstar"),
    ("tests/example_data/NMRSTAR2/tmp/json/dir/starfiles_files_json.tar", "tests/example_data/NMRSTAR2/tmp/nmrstar/tar/starfiles_nmrstar.tar.bz2", "json", "nmrstar"),
    ("tests/example_data/NMRSTAR3/tmp/json/dir/starfiles_files_json.tar.gz", "tests/example_data/NMRSTAR3/tmp/nmrstar/tar/starfiles_nmrstar", "json", "nmrstar"),
    ("tests/example_data/NMRSTAR2/tmp/json/dir/starfiles_files_json.tar.gz", "tests/example_data/NMRSTAR2/tmp/nmrstar/targz/starfiles_nmrstar", "json", "nmrstar"),
    ("tests/example_data/NMRSTAR3/tmp/json/dir/starfiles_files_json.tar.gz", "tests/example_data/NMRSTAR3/tmp/nmrstar/targz/starfiles_nmrstar.zip", "json", "nmrstar"),
    ("tests/example_data/NMRSTAR2/tmp/json/dir/starfiles_files_json.tar.gz", "tests/example_data/NMRSTAR2/tmp/nmrstar/targz/starfiles_nmrstar.zip", "json", "nmrstar"),
    ("tests/example_data/NMRSTAR3/tmp/json/dir/starfiles_files_json.tar.gz", "tests/example_data/NMRSTAR3/tmp/nmrstar/targz/starfiles_nmrstar.tar", "json", "nmrstar"),
    ("tests/example_data/NMRSTAR2/tmp/json/dir/starfiles_files_json.tar.gz", "tests/example_data/NMRSTAR2/tmp/nmrstar/targz/starfiles_nmrstar.tar", "json", "nmrstar"),
    ("tests/example_data/NMRSTAR3/tmp/json/dir/starfiles_files_json.tar.gz", "tests/example_data/NMRSTAR3/tmp/nmrstar/targz/starfiles_nmrstar.tar.gz", "json", "nmrstar"),
    ("tests/example_data/NMRSTAR2/tmp/json/dir/starfiles_files_json.tar.gz", "tests/example_data/NMRSTAR2/tmp/nmrstar/targz/starfiles_nmrstar.tar.gz", "json", "nmrstar"),
    ("tests/example_data/NMRSTAR3/tmp/json/dir/starfiles_files_json.tar.gz", "tests/example_data/NMRSTAR3/tmp/nmrstar/targz/starfiles_nmrstar.tar.bz2", "json", "nmrstar"),
    ("tests/example_data/NMRSTAR2/tmp/json/dir/starfiles_files_json.tar.gz", "tests/example_data/NMRSTAR2/tmp/nmrstar/targz/starfiles_nmrstar.tar.bz2", "json", "nmrstar"),
    ("tests/example_data/NMRSTAR3/tmp/json/dir/starfiles_files_json.tar.bz2", "tests/example_data/NMRSTAR3/tmp/nmrstar/tarbz2/starfiles_nmrstar", "json", "nmrstar"),
    ("tests/example_data/NMRSTAR2/tmp/json/dir/starfiles_files_json.tar.bz2", "tests/example_data/NMRSTAR2/tmp/nmrstar/tarbz2/starfiles_nmrstar", "json", "nmrstar"),
    ("tests/example_data/NMRSTAR3/tmp/json/dir/starfiles_files_json.tar.bz2", "tests/example_data/NMRSTAR3/tmp/nmrstar/tarbz2/starfiles_nmrstar.zip", "json", "nmrstar"),
    ("tests/example_data/NMRSTAR2/tmp/json/dir/starfiles_files_json.tar.bz2", "tests/example_data/NMRSTAR2/tmp/nmrstar/tarbz2/starfiles_nmrstar.zip", "json", "nmrstar"),
    ("tests/example_data/NMRSTAR3/tmp/json/dir/starfiles_files_json.tar.bz2", "tests/example_data/NMRSTAR3/tmp/nmrstar/tarbz2/starfiles_nmrstar.tar", "json", "nmrstar"),
    ("tests/example_data/NMRSTAR2/tmp/json/dir/starfiles_files_json.tar.bz2", "tests/example_data/NMRSTAR2/tmp/nmrstar/tarbz2/starfiles_nmrstar.tar", "json", "nmrstar"),
    ("tests/example_data/NMRSTAR3/tmp/json/dir/starfiles_files_json.tar.bz2", "tests/example_data/NMRSTAR3/tmp/nmrstar/tarbz2/starfiles_nmrstar.tar.gz", "json", "nmrstar"),
    ("tests/example_data/NMRSTAR2/tmp/json/dir/starfiles_files_json.tar.bz2", "tests/example_data/NMRSTAR2/tmp/nmrstar/tarbz2/starfiles_nmrstar.tar.gz", "json", "nmrstar"),
    ("tests/example_data/NMRSTAR3/tmp/json/dir/starfiles_files_json.tar.bz2", "tests/example_data/NMRSTAR3/tmp/nmrstar/tarbz2/starfiles_nmrstar.tar.bz2", "json", "nmrstar"),
    ("tests/example_data/NMRSTAR2/tmp/json/dir/starfiles_files_json.tar.bz2", "tests/example_data/NMRSTAR2/tmp/nmrstar/tarbz2/starfiles_nmrstar.tar.bz2", "json", "nmrstar")
])
def test_convert_command(from_path, to_path, from_format, to_format):
    command = "python -m nmrstarlib convert {} {} --from_format={} --to_format={}".format(from_path, to_path, from_format, to_format)
    assert os.system(command) == 0

    starfile_generator = nmrstarlib.read_files(to_path)
    starfiles_list = list(starfile_generator)
    starfiles_ids_set = set(sf.bmrbid for sf in starfiles_list)
    assert starfiles_ids_set.issubset({"15000", "18569"})


@pytest.mark.parametrize("from_path,amino_acids,atoms,nmrstar_version", [
    ("tests/example_data/NMRSTAR3/bmr18569.str", None, None, "3"),
    ("tests/example_data/NMRSTAR3/bmr18569.str", "SER,MET", None, "3"),
    ("tests/example_data/NMRSTAR3/bmr18569.str", None, "CA,CB", "3"),
    ("tests/example_data/NMRSTAR3/bmr18569.str", "SER,MET", "CA,CB", "3"),
    ("tests/example_data/NMRSTAR2/bmr18569.str", None, None, "2"),
    ("tests/example_data/NMRSTAR2/bmr18569.str", "SER,MET", None, "2"),
    ("tests/example_data/NMRSTAR2/bmr18569.str", None, "CA,CB", "2"),
    ("tests/example_data/NMRSTAR2/bmr18569.str", "SER,MET", "CA,CB", "2")
])
def test_csview_command(from_path, amino_acids, atoms, nmrstar_version):

    if amino_acids == None and atoms == None:
        command = "python -m nmrstarlib csview {} --nmrstar_version={}".format(from_path, nmrstar_version)
    elif amino_acids == None and atoms != None:
        command = "python -m nmrstarlib csview {} --at={} --nmrstar_version={}".format(from_path, atoms, nmrstar_version)
    elif atoms == None and amino_acids != None:
        command = "python -m nmrstarlib csview {} --aa={} --nmrstar_version={}".format(from_path, amino_acids, nmrstar_version)
    else:
        command = "python -m nmrstarlib csview {} --aa={} --at={} --nmrstar_version={}".format(from_path, amino_acids, atoms, nmrstar_version)

    assert os.system(command) == 0
