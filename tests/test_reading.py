from nmrstarlib import nmrstarlib


def test_from_local_file():
    starfile_generator = nmrstarlib.read_files("tests/example_data/NMRSTAR3/bmr18569.str",
                                               "tests/example_data/NMRSTAR2/bmr18569.str")
    starfile1 = next(starfile_generator)
    starfile2 = next(starfile_generator)
    assert starfile1.bmrbid == "18569" and starfile2.bmrbid == "18569"


def test_from_bmrbid():
    starfile_generator = nmrstarlib.read_files("18569")
    starfile = next(starfile_generator)
    assert starfile.bmrbid == "18569"


def test_from_bmrbids():
    starfile_generator = nmrstarlib.read_files("15000", "18569")
    starfile1 = next(starfile_generator)
    starfile2 = next(starfile_generator)
    assert starfile1.bmrbid in ("15000", "18569") and starfile2.bmrbid in ("15000", "18569")


def test_from_directory():
    starfile_generator = nmrstarlib.read_files("tests/example_data/NMRSTAR3/starfiles_directory",
                                               "tests/example_data/NMRSTAR3/starfiles_directory")
    starfiles_list = list(starfile_generator)
    starfiles_ids_set = set(sf.bmrbid for sf in starfiles_list)
    assert starfiles_ids_set == {"15000", "18569"}


def test_from_zip_archive():
    starfile_generator = nmrstarlib.read_files("tests/example_data/NMRSTAR3/starfiles_archive.zip",
                                               "tests/example_data/NMRSTAR2/starfiles_archive.zip")
    starfiles_list = list(starfile_generator)
    starfiles_ids_set = set(sf.bmrbid for sf in starfiles_list)
    assert starfiles_ids_set == {"15000", "18569"}


def test_from_tar_gz_archive():
    starfile_generator = nmrstarlib.read_files("tests/example_data/NMRSTAR3/starfiles_archive.tar.gz",
                                               "tests/example_data/NMRSTAR2/starfiles_archive.tar.gz")
    starfiles_list = list(starfile_generator)
    starfiles_ids_set = set(sf.bmrbid for sf in starfiles_list)
    assert starfiles_ids_set == {"15000", "18569"}


def test_from_tar_bz2_archive():
    starfile_generator = nmrstarlib.read_files("tests/example_data/NMRSTAR3/starfiles_archive.tar.bz2",
                                               "tests/example_data/NMRSTAR2/starfiles_archive.tar.bz2")
    starfiles_list = list(starfile_generator)
    starfiles_ids_set = set(sf.bmrbid for sf in starfiles_list)
    assert starfiles_ids_set == {"15000", "18569"}
