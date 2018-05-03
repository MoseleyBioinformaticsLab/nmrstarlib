import pytest
import nmrstarlib


@pytest.mark.parametrize("source", [
    ("tests/example_data/NMRSTAR3/bmr18569.str",
     "tests/example_data/NMRSTAR2/bmr18569.str",
     "tests/example_data/CIF/2rpv.cif")
])
def test_from_local_file(source):
    starfile_generator = nmrstarlib.read_files(*source)
    starfiles_list = list(starfile_generator)
    starfiles_ids_set = set(sf.id for sf in starfiles_list)
    assert starfiles_ids_set.issubset({"18569", "2RPV"})


@pytest.mark.parametrize("source", [
    ("15000",
     "18569")
])
def test_from_bmrbid(source):
    starfile_generator = nmrstarlib.read_files(*source)
    starfile1 = next(starfile_generator)
    starfile2 = next(starfile_generator)
    assert starfile1.id in ("15000", "18569") and starfile2.id in ("15000", "18569")


@pytest.mark.parametrize("source", [
    ("http://rest.bmrb.wisc.edu/bmrb/NMR-STAR3/15000",
     "http://rest.bmrb.wisc.edu/bmrb/NMR-STAR3/18569")
])
def test_from_url(source):
    starfile_generator = nmrstarlib.read_files(*source)
    starfile1 = next(starfile_generator)
    starfile2 = next(starfile_generator)
    assert starfile1.id in ("15000", "18569") and starfile2.id in ("15000", "18569")


@pytest.mark.parametrize("source", [
    "tests/example_data/NMRSTAR3/starfiles_directory",
    "tests/example_data/NMRSTAR2/starfiles_directory",
    "tests/example_data/CIF/ciffiles_directory",
    "tests/example_data/NMRSTAR3/starfiles_archive.zip",
    "tests/example_data/NMRSTAR2/starfiles_archive.zip",
    "tests/example_data/CIF/ciffiles_archive.zip",
    "tests/example_data/NMRSTAR3/starfiles_archive.tar.gz",
    "tests/example_data/NMRSTAR2/starfiles_archive.tar.gz",
    "tests/example_data/CIF/ciffiles_archive.tar.gz",
    "tests/example_data/NMRSTAR3/starfiles_archive.tar.bz2",
    "tests/example_data/NMRSTAR2/starfiles_archive.tar.bz2",
    "tests/example_data/CIF/ciffiles_archive.tar.bz2"
])
def test_reading(source):
    starfile_generator = nmrstarlib.read_files(source)
    starfiles_list = list(starfile_generator)
    starfiles_ids_set = set(sf.id for sf in starfiles_list)
    assert starfiles_ids_set.issubset({"15000", "18569", "2RPV", "2FRG"})
