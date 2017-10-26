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
    command = "python -m nmrstarlib convert {} {} --from-format={} --to-format={}".format(from_path, to_path, from_format, to_format)
    assert os.system(command) == 0

    starfile_generator = nmrstarlib.read_files(to_path)
    starfiles_list = list(starfile_generator)
    starfiles_ids_set = set(sf.bmrbid for sf in starfiles_list)
    assert starfiles_ids_set.issubset({"15000", "18569"})


@pytest.mark.parametrize("from_path,amino_acids,atoms,amino_acids_and_atoms,nmrstar_version", [
    ("tests/example_data/NMRSTAR3/bmr18569.str", "", "", "", "3"),
    ("tests/example_data/NMRSTAR3/bmr18569.str", "SER,MET", "", "", "3"),
    ("tests/example_data/NMRSTAR3/bmr18569.str", "", "CA,CB", "", "3"),
    ("tests/example_data/NMRSTAR3/bmr18569.str", "SER,MET", "CA,CB", "", "3"),
    ("tests/example_data/NMRSTAR3/bmr18569.str", "", "", "ALA-CA,CB:LYS-CB,CG,CD", "3"),
    ("tests/example_data/NMRSTAR2/bmr18569.str", "", "", "", "2"),
    ("tests/example_data/NMRSTAR2/bmr18569.str", "SER,MET", "", "", "2"),
    ("tests/example_data/NMRSTAR2/bmr18569.str", "", "CA,CB", "", "2"),
    ("tests/example_data/NMRSTAR2/bmr18569.str", "SER,MET", "CA,CB", "", "2"),
    ("tests/example_data/NMRSTAR3/bmr18569.str", "", "", "ALA-CA,CB:LYS-CB,CG,CD", "2")
])
def test_csview_command(from_path, amino_acids, atoms, amino_acids_and_atoms, nmrstar_version):

    command = "python -m nmrstarlib csview {} --aa={} --at={} --aa-at={} --nmrstar-version={}".format(from_path,
                                                                                                      amino_acids,
                                                                                                      atoms,
                                                                                                      amino_acids_and_atoms,
                                                                                                      nmrstar_version)
    assert os.system(command) == 0


@pytest.mark.parametrize("from_path,to_path,test_path,spectrum_name,from_format,to_format,plsplit,distribution,H_dim,C_dim,N_dim,seed,nmrstar_version", [
    # no variance
    ("tests/example_data/NMRSTAR{}/bmr18569.str", "tests/example_data/NMRSTAR{}/tmp/peaklists/no_variance/18569_{}.txt", "tests/example_data/NMRSTAR{}/peaklists/no_variance/18569_{}.txt", "CANCO", "nmrstar", "sparky", "100", "normal", "", "", "", "0", "3"),
    ("tests/example_data/NMRSTAR{}/bmr18569.str", "tests/example_data/NMRSTAR{}/tmp/peaklists/no_variance/18569_{}.txt", "tests/example_data/NMRSTAR{}/peaklists/no_variance/18569_{}.txt", "CANCOCX", "nmrstar", "sparky", "100", "normal", "", "", "", "0", "3"),
    ("tests/example_data/NMRSTAR{}/bmr18569.str", "tests/example_data/NMRSTAR{}/tmp/peaklists/no_variance/18569_{}.txt", "tests/example_data/NMRSTAR{}/peaklists/no_variance/18569_{}.txt", "CBCANH", "nmrstar", "sparky", "100", "normal", "", "", "", "0", "3"),
    ("tests/example_data/NMRSTAR{}/bmr18569.str", "tests/example_data/NMRSTAR{}/tmp/peaklists/no_variance/18569_{}.txt", "tests/example_data/NMRSTAR{}/peaklists/no_variance/18569_{}.txt", "CBCAcoNH", "nmrstar", "sparky", "100", "normal", "", "", "", "0", "3"),
    ("tests/example_data/NMRSTAR{}/bmr18569.str", "tests/example_data/NMRSTAR{}/tmp/peaklists/no_variance/18569_{}.txt", "tests/example_data/NMRSTAR{}/peaklists/no_variance/18569_{}.txt", "CCcoNH", "nmrstar", "sparky", "100", "normal", "", "", "", "0", "3"),
    ("tests/example_data/NMRSTAR{}/bmr18569.str", "tests/example_data/NMRSTAR{}/tmp/peaklists/no_variance/18569_{}.txt", "tests/example_data/NMRSTAR{}/peaklists/no_variance/18569_{}.txt", "HBHAcoNH", "nmrstar", "sparky", "100", "normal", "", "", "", "0", "3"),
    ("tests/example_data/NMRSTAR{}/bmr18569.str", "tests/example_data/NMRSTAR{}/tmp/peaklists/no_variance/18569_{}.txt", "tests/example_data/NMRSTAR{}/peaklists/no_variance/18569_{}.txt", "HNCA", "nmrstar", "sparky", "100", "normal", "", "", "", "0", "3"),
    ("tests/example_data/NMRSTAR{}/bmr18569.str", "tests/example_data/NMRSTAR{}/tmp/peaklists/no_variance/18569_{}.txt", "tests/example_data/NMRSTAR{}/peaklists/no_variance/18569_{}.txt", "HNCACB", "nmrstar", "sparky", "100", "normal", "", "", "", "0", "3"),
    ("tests/example_data/NMRSTAR{}/bmr18569.str", "tests/example_data/NMRSTAR{}/tmp/peaklists/no_variance/18569_{}.txt", "tests/example_data/NMRSTAR{}/peaklists/no_variance/18569_{}.txt", "HNCO", "nmrstar", "sparky", "100", "normal", "", "", "", "0", "3"),
    ("tests/example_data/NMRSTAR{}/bmr18569.str", "tests/example_data/NMRSTAR{}/tmp/peaklists/no_variance/18569_{}.txt", "tests/example_data/NMRSTAR{}/peaklists/no_variance/18569_{}.txt", "HNcaCO", "nmrstar", "sparky", "100", "normal", "", "", "", "0", "3"),
    ("tests/example_data/NMRSTAR{}/bmr18569.str", "tests/example_data/NMRSTAR{}/tmp/peaklists/no_variance/18569_{}.txt", "tests/example_data/NMRSTAR{}/peaklists/no_variance/18569_{}.txt", "HNcoCA", "nmrstar", "sparky", "100", "normal", "", "", "", "0", "3"),
    ("tests/example_data/NMRSTAR{}/bmr18569.str", "tests/example_data/NMRSTAR{}/tmp/peaklists/no_variance/18569_{}.txt", "tests/example_data/NMRSTAR{}/peaklists/no_variance/18569_{}.txt", "HNcoCACB", "nmrstar", "sparky", "100", "normal", "", "", "", "0", "3"),
    ("tests/example_data/NMRSTAR{}/bmr18569.str", "tests/example_data/NMRSTAR{}/tmp/peaklists/no_variance/18569_{}.txt", "tests/example_data/NMRSTAR{}/peaklists/no_variance/18569_{}.txt", "HSQC", "nmrstar", "sparky", "100", "normal", "", "", "", "0", "3"),
    ("tests/example_data/NMRSTAR{}/bmr18569.str", "tests/example_data/NMRSTAR{}/tmp/peaklists/no_variance/18569_{}.txt", "tests/example_data/NMRSTAR{}/peaklists/no_variance/18569_{}.txt", "HccoNH", "nmrstar", "sparky", "100", "normal", "", "", "", "0", "3"),
    ("tests/example_data/NMRSTAR{}/bmr18569.str", "tests/example_data/NMRSTAR{}/tmp/peaklists/no_variance/18569_{}.txt", "tests/example_data/NMRSTAR{}/peaklists/no_variance/18569_{}.txt", "NCA", "nmrstar", "sparky", "100", "normal", "", "", "", "0", "3"),
    ("tests/example_data/NMRSTAR{}/bmr18569.str", "tests/example_data/NMRSTAR{}/tmp/peaklists/no_variance/18569_{}.txt", "tests/example_data/NMRSTAR{}/peaklists/no_variance/18569_{}.txt", "NCACX", "nmrstar", "sparky", "100", "normal", "", "", "", "0", "3"),
    ("tests/example_data/NMRSTAR{}/bmr18569.str", "tests/example_data/NMRSTAR{}/tmp/peaklists/no_variance/18569_{}.txt", "tests/example_data/NMRSTAR{}/peaklists/no_variance/18569_{}.txt", "NCO", "nmrstar", "sparky", "100", "normal", "", "", "", "0", "3"),
    ("tests/example_data/NMRSTAR{}/bmr18569.str", "tests/example_data/NMRSTAR{}/tmp/peaklists/no_variance/18569_{}.txt", "tests/example_data/NMRSTAR{}/peaklists/no_variance/18569_{}.txt", "NCOCX", "nmrstar", "sparky", "100", "normal", "", "", "", "0", "3"),
    ("tests/example_data/NMRSTAR{}/bmr18569.str", "tests/example_data/NMRSTAR{}/tmp/peaklists/no_variance/18569_{}.txt", "tests/example_data/NMRSTAR{}/peaklists/no_variance/18569_{}.txt", "CANCO", "nmrstar", "sparky", "100", "normal", "", "", "", "0", "2"),
    ("tests/example_data/NMRSTAR{}/bmr18569.str", "tests/example_data/NMRSTAR{}/tmp/peaklists/no_variance/18569_{}.txt", "tests/example_data/NMRSTAR{}/peaklists/no_variance/18569_{}.txt", "CANCOCX", "nmrstar", "sparky", "100", "normal", "", "", "", "0", "2"),
    ("tests/example_data/NMRSTAR{}/bmr18569.str", "tests/example_data/NMRSTAR{}/tmp/peaklists/no_variance/18569_{}.txt", "tests/example_data/NMRSTAR{}/peaklists/no_variance/18569_{}.txt", "CBCANH", "nmrstar", "sparky", "100", "normal", "", "", "", "0", "2"),
    ("tests/example_data/NMRSTAR{}/bmr18569.str", "tests/example_data/NMRSTAR{}/tmp/peaklists/no_variance/18569_{}.txt", "tests/example_data/NMRSTAR{}/peaklists/no_variance/18569_{}.txt", "CBCAcoNH", "nmrstar", "sparky", "100", "normal", "", "", "", "0", "2"),
    ("tests/example_data/NMRSTAR{}/bmr18569.str", "tests/example_data/NMRSTAR{}/tmp/peaklists/no_variance/18569_{}.txt", "tests/example_data/NMRSTAR{}/peaklists/no_variance/18569_{}.txt", "CCcoNH", "nmrstar", "sparky", "100", "normal", "", "", "", "0", "2"),
    ("tests/example_data/NMRSTAR{}/bmr18569.str", "tests/example_data/NMRSTAR{}/tmp/peaklists/no_variance/18569_{}.txt", "tests/example_data/NMRSTAR{}/peaklists/no_variance/18569_{}.txt", "HBHAcoNH", "nmrstar", "sparky", "100", "normal", "", "", "", "0", "2"),
    ("tests/example_data/NMRSTAR{}/bmr18569.str", "tests/example_data/NMRSTAR{}/tmp/peaklists/no_variance/18569_{}.txt", "tests/example_data/NMRSTAR{}/peaklists/no_variance/18569_{}.txt", "HNCA", "nmrstar", "sparky", "100", "normal", "", "", "", "0", "2"),
    ("tests/example_data/NMRSTAR{}/bmr18569.str", "tests/example_data/NMRSTAR{}/tmp/peaklists/no_variance/18569_{}.txt", "tests/example_data/NMRSTAR{}/peaklists/no_variance/18569_{}.txt", "HNCACB", "nmrstar", "sparky", "100", "normal", "", "", "", "0", "2"),
    ("tests/example_data/NMRSTAR{}/bmr18569.str", "tests/example_data/NMRSTAR{}/tmp/peaklists/no_variance/18569_{}.txt", "tests/example_data/NMRSTAR{}/peaklists/no_variance/18569_{}.txt", "HNCO", "nmrstar", "sparky", "100", "normal", "", "", "", "0", "2"),
    ("tests/example_data/NMRSTAR{}/bmr18569.str", "tests/example_data/NMRSTAR{}/tmp/peaklists/no_variance/18569_{}.txt", "tests/example_data/NMRSTAR{}/peaklists/no_variance/18569_{}.txt", "HNcaCO", "nmrstar", "sparky", "100", "normal", "", "", "", "0", "2"),
    ("tests/example_data/NMRSTAR{}/bmr18569.str", "tests/example_data/NMRSTAR{}/tmp/peaklists/no_variance/18569_{}.txt", "tests/example_data/NMRSTAR{}/peaklists/no_variance/18569_{}.txt", "HNcoCA", "nmrstar", "sparky", "100", "normal", "", "", "", "0", "2"),
    ("tests/example_data/NMRSTAR{}/bmr18569.str", "tests/example_data/NMRSTAR{}/tmp/peaklists/no_variance/18569_{}.txt", "tests/example_data/NMRSTAR{}/peaklists/no_variance/18569_{}.txt", "HNcoCACB", "nmrstar", "sparky", "100", "normal", "", "", "", "0", "2"),
    ("tests/example_data/NMRSTAR{}/bmr18569.str", "tests/example_data/NMRSTAR{}/tmp/peaklists/no_variance/18569_{}.txt", "tests/example_data/NMRSTAR{}/peaklists/no_variance/18569_{}.txt", "HSQC", "nmrstar", "sparky", "100", "normal", "", "", "", "0", "2"),
    ("tests/example_data/NMRSTAR{}/bmr18569.str", "tests/example_data/NMRSTAR{}/tmp/peaklists/no_variance/18569_{}.txt", "tests/example_data/NMRSTAR{}/peaklists/no_variance/18569_{}.txt", "HccoNH", "nmrstar", "sparky", "100", "normal", "", "", "", "0", "2"),
    ("tests/example_data/NMRSTAR{}/bmr18569.str", "tests/example_data/NMRSTAR{}/tmp/peaklists/no_variance/18569_{}.txt", "tests/example_data/NMRSTAR{}/peaklists/no_variance/18569_{}.txt", "NCA", "nmrstar", "sparky", "100", "normal", "", "", "", "0", "2"),
    ("tests/example_data/NMRSTAR{}/bmr18569.str", "tests/example_data/NMRSTAR{}/tmp/peaklists/no_variance/18569_{}.txt", "tests/example_data/NMRSTAR{}/peaklists/no_variance/18569_{}.txt", "NCACX", "nmrstar", "sparky", "100", "normal", "", "", "", "0", "2"),
    ("tests/example_data/NMRSTAR{}/bmr18569.str", "tests/example_data/NMRSTAR{}/tmp/peaklists/no_variance/18569_{}.txt", "tests/example_data/NMRSTAR{}/peaklists/no_variance/18569_{}.txt", "NCO", "nmrstar", "sparky", "100", "normal", "", "", "", "0", "2"),
    ("tests/example_data/NMRSTAR{}/bmr18569.str", "tests/example_data/NMRSTAR{}/tmp/peaklists/no_variance/18569_{}.txt", "tests/example_data/NMRSTAR{}/peaklists/no_variance/18569_{}.txt", "NCOCX", "nmrstar", "sparky", "100", "normal", "", "", "", "0", "2"),
    # single source of variance
    ("tests/example_data/NMRSTAR{}/bmr18569.str", "tests/example_data/NMRSTAR{}/tmp/peaklists/single_source_variance/18569_{}.txt", "tests/example_data/NMRSTAR{}/peaklists/single_source_variance/18569_{}.txt", "CANCO", "nmrstar", "sparky", "100", "normal", "0,0.001", "0,0.01", "0,0.01", "0", "3"),
    ("tests/example_data/NMRSTAR{}/bmr18569.str", "tests/example_data/NMRSTAR{}/tmp/peaklists/single_source_variance/18569_{}.txt", "tests/example_data/NMRSTAR{}/peaklists/single_source_variance/18569_{}.txt", "CANCOCX", "nmrstar", "sparky", "100", "normal", "0,0.001", "0,0.01", "0,0.01", "0", "3"),
    ("tests/example_data/NMRSTAR{}/bmr18569.str", "tests/example_data/NMRSTAR{}/tmp/peaklists/single_source_variance/18569_{}.txt", "tests/example_data/NMRSTAR{}/peaklists/single_source_variance/18569_{}.txt", "CBCANH", "nmrstar", "sparky", "100", "normal", "0,0.001", "0,0.01", "0,0.01", "0", "3"),
    ("tests/example_data/NMRSTAR{}/bmr18569.str", "tests/example_data/NMRSTAR{}/tmp/peaklists/single_source_variance/18569_{}.txt", "tests/example_data/NMRSTAR{}/peaklists/single_source_variance/18569_{}.txt", "CBCAcoNH", "nmrstar", "sparky", "100", "normal", "0,0.001", "0,0.01", "0,0.01", "0", "3"),
    ("tests/example_data/NMRSTAR{}/bmr18569.str", "tests/example_data/NMRSTAR{}/tmp/peaklists/single_source_variance/18569_{}.txt", "tests/example_data/NMRSTAR{}/peaklists/single_source_variance/18569_{}.txt", "CCcoNH", "nmrstar", "sparky", "100", "normal", "0,0.001", "0,0.01", "0,0.01", "0", "3"),
    ("tests/example_data/NMRSTAR{}/bmr18569.str", "tests/example_data/NMRSTAR{}/tmp/peaklists/single_source_variance/18569_{}.txt", "tests/example_data/NMRSTAR{}/peaklists/single_source_variance/18569_{}.txt", "HBHAcoNH", "nmrstar", "sparky", "100", "normal", "0,0.001", "0,0.01", "0,0.01", "0", "3"),
    ("tests/example_data/NMRSTAR{}/bmr18569.str", "tests/example_data/NMRSTAR{}/tmp/peaklists/single_source_variance/18569_{}.txt", "tests/example_data/NMRSTAR{}/peaklists/single_source_variance/18569_{}.txt", "HNCA", "nmrstar", "sparky", "100", "normal", "0,0.001", "0,0.01", "0,0.01", "0", "3"),
    ("tests/example_data/NMRSTAR{}/bmr18569.str", "tests/example_data/NMRSTAR{}/tmp/peaklists/single_source_variance/18569_{}.txt", "tests/example_data/NMRSTAR{}/peaklists/single_source_variance/18569_{}.txt", "HNCACB", "nmrstar", "sparky", "100", "normal", "0,0.001", "0,0.01", "0,0.01", "0", "3"),
    ("tests/example_data/NMRSTAR{}/bmr18569.str", "tests/example_data/NMRSTAR{}/tmp/peaklists/single_source_variance/18569_{}.txt", "tests/example_data/NMRSTAR{}/peaklists/single_source_variance/18569_{}.txt", "HNCO", "nmrstar", "sparky", "100", "normal", "0,0.001", "0,0.01", "0,0.01", "0", "3"),
    ("tests/example_data/NMRSTAR{}/bmr18569.str", "tests/example_data/NMRSTAR{}/tmp/peaklists/single_source_variance/18569_{}.txt", "tests/example_data/NMRSTAR{}/peaklists/single_source_variance/18569_{}.txt", "HNcaCO", "nmrstar", "sparky", "100", "normal", "0,0.001", "0,0.01", "0,0.01", "0", "3"),
    ("tests/example_data/NMRSTAR{}/bmr18569.str", "tests/example_data/NMRSTAR{}/tmp/peaklists/single_source_variance/18569_{}.txt", "tests/example_data/NMRSTAR{}/peaklists/single_source_variance/18569_{}.txt", "HNcoCA", "nmrstar", "sparky", "100", "normal", "0,0.001", "0,0.01", "0,0.01", "0", "3"),
    ("tests/example_data/NMRSTAR{}/bmr18569.str", "tests/example_data/NMRSTAR{}/tmp/peaklists/single_source_variance/18569_{}.txt", "tests/example_data/NMRSTAR{}/peaklists/single_source_variance/18569_{}.txt", "HNcoCACB", "nmrstar", "sparky", "100", "normal", "0,0.001", "0,0.01", "0,0.01", "0", "3"),
    ("tests/example_data/NMRSTAR{}/bmr18569.str", "tests/example_data/NMRSTAR{}/tmp/peaklists/single_source_variance/18569_{}.txt", "tests/example_data/NMRSTAR{}/peaklists/single_source_variance/18569_{}.txt", "HSQC", "nmrstar", "sparky", "100", "normal", "0,0.001", "0,0.01", "0,0.01", "0", "3"),
    ("tests/example_data/NMRSTAR{}/bmr18569.str", "tests/example_data/NMRSTAR{}/tmp/peaklists/single_source_variance/18569_{}.txt", "tests/example_data/NMRSTAR{}/peaklists/single_source_variance/18569_{}.txt", "HccoNH", "nmrstar", "sparky", "100", "normal", "0,0.001", "0,0.01", "0,0.01", "0", "3"),
    ("tests/example_data/NMRSTAR{}/bmr18569.str", "tests/example_data/NMRSTAR{}/tmp/peaklists/single_source_variance/18569_{}.txt", "tests/example_data/NMRSTAR{}/peaklists/single_source_variance/18569_{}.txt", "NCA", "nmrstar", "sparky", "100", "normal", "0,0.001", "0,0.01", "0,0.01", "0", "3"),
    ("tests/example_data/NMRSTAR{}/bmr18569.str", "tests/example_data/NMRSTAR{}/tmp/peaklists/single_source_variance/18569_{}.txt", "tests/example_data/NMRSTAR{}/peaklists/single_source_variance/18569_{}.txt", "NCACX", "nmrstar", "sparky", "100", "normal", "0,0.001", "0,0.01", "0,0.01", "0", "3"),
    ("tests/example_data/NMRSTAR{}/bmr18569.str", "tests/example_data/NMRSTAR{}/tmp/peaklists/single_source_variance/18569_{}.txt", "tests/example_data/NMRSTAR{}/peaklists/single_source_variance/18569_{}.txt", "NCO", "nmrstar", "sparky", "100", "normal", "0,0.001", "0,0.01", "0,0.01", "0", "3"),
    ("tests/example_data/NMRSTAR{}/bmr18569.str", "tests/example_data/NMRSTAR{}/tmp/peaklists/single_source_variance/18569_{}.txt", "tests/example_data/NMRSTAR{}/peaklists/single_source_variance/18569_{}.txt", "NCOCX", "nmrstar", "sparky", "100", "normal", "0,0.001", "0,0.01", "0,0.01", "0", "3"),
    ("tests/example_data/NMRSTAR{}/bmr18569.str", "tests/example_data/NMRSTAR{}/tmp/peaklists/single_source_variance/18569_{}.txt", "tests/example_data/NMRSTAR{}/peaklists/single_source_variance/18569_{}.txt", "CANCO", "nmrstar", "sparky", "100", "normal", "0,0.001", "0,0.01", "0,0.01", "0", "2"),
    ("tests/example_data/NMRSTAR{}/bmr18569.str", "tests/example_data/NMRSTAR{}/tmp/peaklists/single_source_variance/18569_{}.txt", "tests/example_data/NMRSTAR{}/peaklists/single_source_variance/18569_{}.txt", "CANCOCX", "nmrstar", "sparky", "100", "normal", "0,0.001", "0,0.01", "0,0.01", "0", "2"),
    ("tests/example_data/NMRSTAR{}/bmr18569.str", "tests/example_data/NMRSTAR{}/tmp/peaklists/single_source_variance/18569_{}.txt", "tests/example_data/NMRSTAR{}/peaklists/single_source_variance/18569_{}.txt", "CBCANH", "nmrstar", "sparky", "100", "normal", "0,0.001", "0,0.01", "0,0.01", "0", "2"),
    ("tests/example_data/NMRSTAR{}/bmr18569.str", "tests/example_data/NMRSTAR{}/tmp/peaklists/single_source_variance/18569_{}.txt", "tests/example_data/NMRSTAR{}/peaklists/single_source_variance/18569_{}.txt", "CBCAcoNH", "nmrstar", "sparky", "100", "normal", "0,0.001", "0,0.01", "0,0.01", "0", "2"),
    ("tests/example_data/NMRSTAR{}/bmr18569.str", "tests/example_data/NMRSTAR{}/tmp/peaklists/single_source_variance/18569_{}.txt", "tests/example_data/NMRSTAR{}/peaklists/single_source_variance/18569_{}.txt", "CCcoNH", "nmrstar", "sparky", "100", "normal", "0,0.001", "0,0.01", "0,0.01", "0", "2"),
    ("tests/example_data/NMRSTAR{}/bmr18569.str", "tests/example_data/NMRSTAR{}/tmp/peaklists/single_source_variance/18569_{}.txt", "tests/example_data/NMRSTAR{}/peaklists/single_source_variance/18569_{}.txt", "HBHAcoNH", "nmrstar", "sparky", "100", "normal", "0,0.001", "0,0.01", "0,0.01", "0", "2"),
    ("tests/example_data/NMRSTAR{}/bmr18569.str", "tests/example_data/NMRSTAR{}/tmp/peaklists/single_source_variance/18569_{}.txt", "tests/example_data/NMRSTAR{}/peaklists/single_source_variance/18569_{}.txt", "HNCA", "nmrstar", "sparky", "100", "normal", "0,0.001", "0,0.01", "0,0.01", "0", "2"),
    ("tests/example_data/NMRSTAR{}/bmr18569.str", "tests/example_data/NMRSTAR{}/tmp/peaklists/single_source_variance/18569_{}.txt", "tests/example_data/NMRSTAR{}/peaklists/single_source_variance/18569_{}.txt", "HNCACB", "nmrstar", "sparky", "100", "normal", "0,0.001", "0,0.01", "0,0.01", "0", "2"),
    ("tests/example_data/NMRSTAR{}/bmr18569.str", "tests/example_data/NMRSTAR{}/tmp/peaklists/single_source_variance/18569_{}.txt", "tests/example_data/NMRSTAR{}/peaklists/single_source_variance/18569_{}.txt", "HNCO", "nmrstar", "sparky", "100", "normal", "0,0.001", "0,0.01", "0,0.01", "0", "2"),
    ("tests/example_data/NMRSTAR{}/bmr18569.str", "tests/example_data/NMRSTAR{}/tmp/peaklists/single_source_variance/18569_{}.txt", "tests/example_data/NMRSTAR{}/peaklists/single_source_variance/18569_{}.txt", "HNcaCO", "nmrstar", "sparky", "100", "normal", "0,0.001", "0,0.01", "0,0.01", "0", "2"),
    ("tests/example_data/NMRSTAR{}/bmr18569.str", "tests/example_data/NMRSTAR{}/tmp/peaklists/single_source_variance/18569_{}.txt", "tests/example_data/NMRSTAR{}/peaklists/single_source_variance/18569_{}.txt", "HNcoCA", "nmrstar", "sparky", "100", "normal", "0,0.001", "0,0.01", "0,0.01", "0", "2"),
    ("tests/example_data/NMRSTAR{}/bmr18569.str", "tests/example_data/NMRSTAR{}/tmp/peaklists/single_source_variance/18569_{}.txt", "tests/example_data/NMRSTAR{}/peaklists/single_source_variance/18569_{}.txt", "HNcoCACB", "nmrstar", "sparky", "100", "normal", "0,0.001", "0,0.01", "0,0.01", "0", "2"),
    ("tests/example_data/NMRSTAR{}/bmr18569.str", "tests/example_data/NMRSTAR{}/tmp/peaklists/single_source_variance/18569_{}.txt", "tests/example_data/NMRSTAR{}/peaklists/single_source_variance/18569_{}.txt", "HSQC", "nmrstar", "sparky", "100", "normal", "0,0.001", "0,0.01", "0,0.01", "0", "2"),
    ("tests/example_data/NMRSTAR{}/bmr18569.str", "tests/example_data/NMRSTAR{}/tmp/peaklists/single_source_variance/18569_{}.txt", "tests/example_data/NMRSTAR{}/peaklists/single_source_variance/18569_{}.txt", "HccoNH", "nmrstar", "sparky", "100", "normal", "0,0.001", "0,0.01", "0,0.01", "0", "2"),
    ("tests/example_data/NMRSTAR{}/bmr18569.str", "tests/example_data/NMRSTAR{}/tmp/peaklists/single_source_variance/18569_{}.txt", "tests/example_data/NMRSTAR{}/peaklists/single_source_variance/18569_{}.txt", "NCA", "nmrstar", "sparky", "100", "normal", "0,0.001", "0,0.01", "0,0.01", "0", "2"),
    ("tests/example_data/NMRSTAR{}/bmr18569.str", "tests/example_data/NMRSTAR{}/tmp/peaklists/single_source_variance/18569_{}.txt", "tests/example_data/NMRSTAR{}/peaklists/single_source_variance/18569_{}.txt", "NCACX", "nmrstar", "sparky", "100", "normal", "0,0.001", "0,0.01", "0,0.01", "0", "2"),
    ("tests/example_data/NMRSTAR{}/bmr18569.str", "tests/example_data/NMRSTAR{}/tmp/peaklists/single_source_variance/18569_{}.txt", "tests/example_data/NMRSTAR{}/peaklists/single_source_variance/18569_{}.txt", "NCO", "nmrstar", "sparky", "100", "normal", "0,0.001", "0,0.01", "0,0.01", "0", "2"),
    ("tests/example_data/NMRSTAR{}/bmr18569.str", "tests/example_data/NMRSTAR{}/tmp/peaklists/single_source_variance/18569_{}.txt", "tests/example_data/NMRSTAR{}/peaklists/single_source_variance/18569_{}.txt", "NCOCX", "nmrstar", "sparky", "100", "normal", "0,0.001", "0,0.01", "0,0.01", "0", "2"),
    # two sources of variance
    ("tests/example_data/NMRSTAR{}/bmr18569.str", "tests/example_data/NMRSTAR{}/tmp/peaklists/two_source_variance/18569_{}.txt", "tests/example_data/NMRSTAR{}/peaklists/two_source_variance/18569_{}.txt", "CANCO", "nmrstar", "sparky", "70,30", "normal", "0:0,0.001:0.005", "0:0,0.01:0.05", "0:0,0.01:0.05", "0", "3"),
    ("tests/example_data/NMRSTAR{}/bmr18569.str", "tests/example_data/NMRSTAR{}/tmp/peaklists/two_source_variance/18569_{}.txt", "tests/example_data/NMRSTAR{}/peaklists/two_source_variance/18569_{}.txt", "CANCOCX", "nmrstar", "sparky", "70,30", "normal", "0:0,0.001:0.005", "0:0,0.01:0.05", "0:0,0.01:0.05", "0", "3"),
    ("tests/example_data/NMRSTAR{}/bmr18569.str", "tests/example_data/NMRSTAR{}/tmp/peaklists/two_source_variance/18569_{}.txt", "tests/example_data/NMRSTAR{}/peaklists/two_source_variance/18569_{}.txt", "CBCANH", "nmrstar", "sparky", "70,30", "normal", "0:0,0.001:0.005", "0:0,0.01:0.05", "0:0,0.01:0.05", "0", "3"),
    ("tests/example_data/NMRSTAR{}/bmr18569.str", "tests/example_data/NMRSTAR{}/tmp/peaklists/two_source_variance/18569_{}.txt", "tests/example_data/NMRSTAR{}/peaklists/two_source_variance/18569_{}.txt", "CBCAcoNH", "nmrstar", "sparky", "70,30", "normal", "0:0,0.001:0.005", "0:0,0.01:0.05", "0:0,0.01:0.05", "0", "3"),
    ("tests/example_data/NMRSTAR{}/bmr18569.str", "tests/example_data/NMRSTAR{}/tmp/peaklists/two_source_variance/18569_{}.txt", "tests/example_data/NMRSTAR{}/peaklists/two_source_variance/18569_{}.txt", "CCcoNH", "nmrstar", "sparky", "70,30", "normal", "0:0,0.001:0.005", "0:0,0.01:0.05", "0:0,0.01:0.05", "0", "3"),
    ("tests/example_data/NMRSTAR{}/bmr18569.str", "tests/example_data/NMRSTAR{}/tmp/peaklists/two_source_variance/18569_{}.txt", "tests/example_data/NMRSTAR{}/peaklists/two_source_variance/18569_{}.txt", "HBHAcoNH", "nmrstar", "sparky", "70,30", "normal", "0:0,0.001:0.005", "0:0,0.01:0.05", "0:0,0.01:0.05", "0", "3"),
    ("tests/example_data/NMRSTAR{}/bmr18569.str", "tests/example_data/NMRSTAR{}/tmp/peaklists/two_source_variance/18569_{}.txt", "tests/example_data/NMRSTAR{}/peaklists/two_source_variance/18569_{}.txt", "HNCA", "nmrstar", "sparky", "70,30", "normal", "0:0,0.001:0.005", "0:0,0.01:0.05", "0:0,0.01:0.05", "0", "3"),
    ("tests/example_data/NMRSTAR{}/bmr18569.str", "tests/example_data/NMRSTAR{}/tmp/peaklists/two_source_variance/18569_{}.txt", "tests/example_data/NMRSTAR{}/peaklists/two_source_variance/18569_{}.txt", "HNCACB", "nmrstar", "sparky", "70,30", "normal", "0:0,0.001:0.005", "0:0,0.01:0.05", "0:0,0.01:0.05", "0", "3"),
    ("tests/example_data/NMRSTAR{}/bmr18569.str", "tests/example_data/NMRSTAR{}/tmp/peaklists/two_source_variance/18569_{}.txt", "tests/example_data/NMRSTAR{}/peaklists/two_source_variance/18569_{}.txt", "HNCO", "nmrstar", "sparky", "70,30", "normal", "0:0,0.001:0.005", "0:0,0.01:0.05", "0:0,0.01:0.05", "0", "3"),
    ("tests/example_data/NMRSTAR{}/bmr18569.str", "tests/example_data/NMRSTAR{}/tmp/peaklists/two_source_variance/18569_{}.txt", "tests/example_data/NMRSTAR{}/peaklists/two_source_variance/18569_{}.txt", "HNcaCO", "nmrstar", "sparky", "70,30", "normal", "0:0,0.001:0.005", "0:0,0.01:0.05", "0:0,0.01:0.05", "0", "3"),
    ("tests/example_data/NMRSTAR{}/bmr18569.str", "tests/example_data/NMRSTAR{}/tmp/peaklists/two_source_variance/18569_{}.txt", "tests/example_data/NMRSTAR{}/peaklists/two_source_variance/18569_{}.txt", "HNcoCA", "nmrstar", "sparky", "70,30", "normal", "0:0,0.001:0.005", "0:0,0.01:0.05", "0:0,0.01:0.05", "0", "3"),
    ("tests/example_data/NMRSTAR{}/bmr18569.str", "tests/example_data/NMRSTAR{}/tmp/peaklists/two_source_variance/18569_{}.txt", "tests/example_data/NMRSTAR{}/peaklists/two_source_variance/18569_{}.txt", "HNcoCACB", "nmrstar", "sparky", "70,30", "normal", "0:0,0.001:0.005", "0:0,0.01:0.05", "0:0,0.01:0.05", "0", "3"),
    ("tests/example_data/NMRSTAR{}/bmr18569.str", "tests/example_data/NMRSTAR{}/tmp/peaklists/two_source_variance/18569_{}.txt", "tests/example_data/NMRSTAR{}/peaklists/two_source_variance/18569_{}.txt", "HSQC", "nmrstar", "sparky", "70,30", "normal", "0:0,0.001:0.005", "0:0,0.01:0.05", "0:0,0.01:0.05", "0", "3"),
    ("tests/example_data/NMRSTAR{}/bmr18569.str", "tests/example_data/NMRSTAR{}/tmp/peaklists/two_source_variance/18569_{}.txt", "tests/example_data/NMRSTAR{}/peaklists/two_source_variance/18569_{}.txt", "HccoNH", "nmrstar", "sparky", "70,30", "normal", "0:0,0.001:0.005", "0:0,0.01:0.05", "0:0,0.01:0.05", "0", "3"),
    ("tests/example_data/NMRSTAR{}/bmr18569.str", "tests/example_data/NMRSTAR{}/tmp/peaklists/two_source_variance/18569_{}.txt", "tests/example_data/NMRSTAR{}/peaklists/two_source_variance/18569_{}.txt", "NCA", "nmrstar", "sparky", "70,30", "normal", "0:0,0.001:0.005", "0:0,0.01:0.05", "0:0,0.01:0.05", "0", "3"),
    ("tests/example_data/NMRSTAR{}/bmr18569.str", "tests/example_data/NMRSTAR{}/tmp/peaklists/two_source_variance/18569_{}.txt", "tests/example_data/NMRSTAR{}/peaklists/two_source_variance/18569_{}.txt", "NCACX", "nmrstar", "sparky", "70,30", "normal", "0:0,0.001:0.005", "0:0,0.01:0.05", "0:0,0.01:0.05", "0", "3"),
    ("tests/example_data/NMRSTAR{}/bmr18569.str", "tests/example_data/NMRSTAR{}/tmp/peaklists/two_source_variance/18569_{}.txt", "tests/example_data/NMRSTAR{}/peaklists/two_source_variance/18569_{}.txt", "NCO", "nmrstar", "sparky", "70,30", "normal", "0:0,0.001:0.005", "0:0,0.01:0.05", "0:0,0.01:0.05", "0", "3"),
    ("tests/example_data/NMRSTAR{}/bmr18569.str", "tests/example_data/NMRSTAR{}/tmp/peaklists/two_source_variance/18569_{}.txt", "tests/example_data/NMRSTAR{}/peaklists/two_source_variance/18569_{}.txt", "NCOCX", "nmrstar", "sparky", "70,30", "normal", "0:0,0.001:0.005", "0:0,0.01:0.05", "0:0,0.01:0.05", "0", "3"),
    ("tests/example_data/NMRSTAR{}/bmr18569.str", "tests/example_data/NMRSTAR{}/tmp/peaklists/two_source_variance/18569_{}.txt", "tests/example_data/NMRSTAR{}/peaklists/two_source_variance/18569_{}.txt", "CANCO", "nmrstar", "sparky", "70,30", "normal", "0:0,0.001:0.005", "0:0,0.01:0.05", "0:0,0.01:0.05", "0", "2"),
    ("tests/example_data/NMRSTAR{}/bmr18569.str", "tests/example_data/NMRSTAR{}/tmp/peaklists/two_source_variance/18569_{}.txt", "tests/example_data/NMRSTAR{}/peaklists/two_source_variance/18569_{}.txt", "CANCOCX", "nmrstar", "sparky", "70,30", "normal", "0:0,0.001:0.005", "0:0,0.01:0.05", "0:0,0.01:0.05", "0", "2"),
    ("tests/example_data/NMRSTAR{}/bmr18569.str", "tests/example_data/NMRSTAR{}/tmp/peaklists/two_source_variance/18569_{}.txt", "tests/example_data/NMRSTAR{}/peaklists/two_source_variance/18569_{}.txt", "CBCANH", "nmrstar", "sparky", "70,30", "normal", "0:0,0.001:0.005", "0:0,0.01:0.05", "0:0,0.01:0.05", "0", "2"),
    ("tests/example_data/NMRSTAR{}/bmr18569.str", "tests/example_data/NMRSTAR{}/tmp/peaklists/two_source_variance/18569_{}.txt", "tests/example_data/NMRSTAR{}/peaklists/two_source_variance/18569_{}.txt", "CBCAcoNH", "nmrstar", "sparky", "70,30", "normal", "0:0,0.001:0.005", "0:0,0.01:0.05", "0:0,0.01:0.05", "0", "2"),
    ("tests/example_data/NMRSTAR{}/bmr18569.str", "tests/example_data/NMRSTAR{}/tmp/peaklists/two_source_variance/18569_{}.txt", "tests/example_data/NMRSTAR{}/peaklists/two_source_variance/18569_{}.txt", "CCcoNH", "nmrstar", "sparky", "70,30", "normal", "0:0,0.001:0.005", "0:0,0.01:0.05", "0:0,0.01:0.05", "0", "2"),
    ("tests/example_data/NMRSTAR{}/bmr18569.str", "tests/example_data/NMRSTAR{}/tmp/peaklists/two_source_variance/18569_{}.txt", "tests/example_data/NMRSTAR{}/peaklists/two_source_variance/18569_{}.txt", "HBHAcoNH", "nmrstar", "sparky", "70,30", "normal", "0:0,0.001:0.005", "0:0,0.01:0.05", "0:0,0.01:0.05", "0", "2"),
    ("tests/example_data/NMRSTAR{}/bmr18569.str", "tests/example_data/NMRSTAR{}/tmp/peaklists/two_source_variance/18569_{}.txt", "tests/example_data/NMRSTAR{}/peaklists/two_source_variance/18569_{}.txt", "HNCA", "nmrstar", "sparky", "70,30", "normal", "0:0,0.001:0.005", "0:0,0.01:0.05", "0:0,0.01:0.05", "0", "2"),
    ("tests/example_data/NMRSTAR{}/bmr18569.str", "tests/example_data/NMRSTAR{}/tmp/peaklists/two_source_variance/18569_{}.txt", "tests/example_data/NMRSTAR{}/peaklists/two_source_variance/18569_{}.txt", "HNCACB", "nmrstar", "sparky", "70,30", "normal", "0:0,0.001:0.005", "0:0,0.01:0.05", "0:0,0.01:0.05", "0", "2"),
    ("tests/example_data/NMRSTAR{}/bmr18569.str", "tests/example_data/NMRSTAR{}/tmp/peaklists/two_source_variance/18569_{}.txt", "tests/example_data/NMRSTAR{}/peaklists/two_source_variance/18569_{}.txt", "HNCO", "nmrstar", "sparky", "70,30", "normal", "0:0,0.001:0.005", "0:0,0.01:0.05", "0:0,0.01:0.05", "0", "2"),
    ("tests/example_data/NMRSTAR{}/bmr18569.str", "tests/example_data/NMRSTAR{}/tmp/peaklists/two_source_variance/18569_{}.txt", "tests/example_data/NMRSTAR{}/peaklists/two_source_variance/18569_{}.txt", "HNcaCO", "nmrstar", "sparky", "70,30", "normal", "0:0,0.001:0.005", "0:0,0.01:0.05", "0:0,0.01:0.05", "0", "2"),
    ("tests/example_data/NMRSTAR{}/bmr18569.str", "tests/example_data/NMRSTAR{}/tmp/peaklists/two_source_variance/18569_{}.txt", "tests/example_data/NMRSTAR{}/peaklists/two_source_variance/18569_{}.txt", "HNcoCA", "nmrstar", "sparky", "70,30", "normal", "0:0,0.001:0.005", "0:0,0.01:0.05", "0:0,0.01:0.05", "0", "2"),
    ("tests/example_data/NMRSTAR{}/bmr18569.str", "tests/example_data/NMRSTAR{}/tmp/peaklists/two_source_variance/18569_{}.txt", "tests/example_data/NMRSTAR{}/peaklists/two_source_variance/18569_{}.txt", "HNcoCACB", "nmrstar", "sparky", "70,30", "normal", "0:0,0.001:0.005", "0:0,0.01:0.05", "0:0,0.01:0.05", "0", "2"),
    ("tests/example_data/NMRSTAR{}/bmr18569.str", "tests/example_data/NMRSTAR{}/tmp/peaklists/two_source_variance/18569_{}.txt", "tests/example_data/NMRSTAR{}/peaklists/two_source_variance/18569_{}.txt", "HSQC", "nmrstar", "sparky", "70,30", "normal", "0:0,0.001:0.005", "0:0,0.01:0.05", "0:0,0.01:0.05", "0", "2"),
    ("tests/example_data/NMRSTAR{}/bmr18569.str", "tests/example_data/NMRSTAR{}/tmp/peaklists/two_source_variance/18569_{}.txt", "tests/example_data/NMRSTAR{}/peaklists/two_source_variance/18569_{}.txt", "HccoNH", "nmrstar", "sparky", "70,30", "normal", "0:0,0.001:0.005", "0:0,0.01:0.05", "0:0,0.01:0.05", "0", "2"),
    ("tests/example_data/NMRSTAR{}/bmr18569.str", "tests/example_data/NMRSTAR{}/tmp/peaklists/two_source_variance/18569_{}.txt", "tests/example_data/NMRSTAR{}/peaklists/two_source_variance/18569_{}.txt", "NCA", "nmrstar", "sparky", "70,30", "normal", "0:0,0.001:0.005", "0:0,0.01:0.05", "0:0,0.01:0.05", "0", "2"),
    ("tests/example_data/NMRSTAR{}/bmr18569.str", "tests/example_data/NMRSTAR{}/tmp/peaklists/two_source_variance/18569_{}.txt", "tests/example_data/NMRSTAR{}/peaklists/two_source_variance/18569_{}.txt", "NCACX", "nmrstar", "sparky", "70,30", "normal", "0:0,0.001:0.005", "0:0,0.01:0.05", "0:0,0.01:0.05", "0", "2"),
    ("tests/example_data/NMRSTAR{}/bmr18569.str", "tests/example_data/NMRSTAR{}/tmp/peaklists/two_source_variance/18569_{}.txt", "tests/example_data/NMRSTAR{}/peaklists/two_source_variance/18569_{}.txt", "NCO", "nmrstar", "sparky", "70,30", "normal", "0:0,0.001:0.005", "0:0,0.01:0.05", "0:0,0.01:0.05", "0", "2"),
    ("tests/example_data/NMRSTAR{}/bmr18569.str", "tests/example_data/NMRSTAR{}/tmp/peaklists/two_source_variance/18569_{}.txt", "tests/example_data/NMRSTAR{}/peaklists/two_source_variance/18569_{}.txt", "NCOCX", "nmrstar", "sparky", "70,30", "normal", "0:0,0.001:0.005", "0:0,0.01:0.05", "0:0,0.01:0.05", "0", "2"),
])
def test_plsimulate_command(from_path, to_path, test_path, spectrum_name, from_format, to_format, plsplit, distribution, H_dim, C_dim, N_dim, seed, nmrstar_version):

    from_path = from_path.format(nmrstar_version)
    to_path = to_path.format(nmrstar_version, spectrum_name)
    test_path = test_path.format(nmrstar_version, spectrum_name)

    command = "python -m nmrstarlib plsimulate {} {} {} --from-format={} --to-format={} --plsplit={} " \
              "--distribution={} --H={} --C={} --N={} --seed={} --nmrstar-version={}".\
        format(from_path, to_path, spectrum_name, from_format, to_format, plsplit, distribution, H_dim, C_dim, N_dim, seed, nmrstar_version)

    assert os.system(command) == 0

    with open(test_path) as infile:
        template_peaklist = infile.read()
    with open(to_path) as infile:
        generated_peaklist = infile.read()

    assert template_peaklist == generated_peaklist
