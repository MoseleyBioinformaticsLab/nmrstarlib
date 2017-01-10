from nmrstarlib import nmrstarlib


def test_from_local_file():
    starfile_generator = nmrstarlib.read_files("tests/example_data/bmr18569.str")
    starfile = next(starfile_generator)
    assert starfile.bmrbid == "18569"


def test_from_local_files():
    starfile_generator = nmrstarlib.read_files("tests/example_data/bmr15000.str", "tests/example_data/bmr18569.str")
    starfile1 = next(starfile_generator)
    starfile2 = next(starfile_generator)
    assert starfile1.bmrbid == "15000" and starfile2.bmrbid == "18569"


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
    starfile_generator = nmrstarlib.read_files("tests/example_data/starfiles_directory")
    starfile1 = next(starfile_generator)
    starfile2 = next(starfile_generator)
    assert starfile1.bmrbid in ("15000", "18569") and starfile2.bmrbid in ("15000", "18569")


def test_from_zip_archive():
    starfile_generator = nmrstarlib.read_files("tests/example_data/starfiles_archive.zip")
    starfile1 = next(starfile_generator)
    starfile2 = next(starfile_generator)
    assert starfile1.bmrbid in ("15000", "18569") and starfile2.bmrbid in ("15000", "18569")


def test_from_tar_gz_archive():
    starfile_generator = nmrstarlib.read_files("tests/example_data/starfiles_archive.tar.gz")
    starfile1 = next(starfile_generator)
    starfile2 = next(starfile_generator)
    assert starfile1.bmrbid in ("15000", "18569") and starfile2.bmrbid in ("15000", "18569")


def test_from_tar_bz2_archive():
    starfile_generator = nmrstarlib.read_files("tests/example_data/starfiles_archive.tar.bz2")
    starfile1 = next(starfile_generator)
    starfile2 = next(starfile_generator)
    assert starfile1.bmrbid in ("15000", "18569") and starfile2.bmrbid in ("15000", "18569")
