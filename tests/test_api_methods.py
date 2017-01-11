import json
from collections import OrderedDict
from nmrstarlib import nmrstarlib


def test_chem_shift_by_residue_all():
    starfile_generator = nmrstarlib.read_files("tests/example_data/NMRSTAR3/bmr18569.str",
                                               "tests/example_data/NMRSTAR2/bmr18569.str")
    starfile1 = next(starfile_generator)
    starfile2 = next(starfile_generator)
    test_chem_shifts1 = starfile1.chem_shifts_by_residue(nmrstar_version="3")
    test_chem_shifts2 = starfile2.chem_shifts_by_residue(nmrstar_version="2")

    with open("tests/example_data/NMRSTAR3/chem_shifts_by_residue_all.json", "r") as infile:
        model_chem_shifts1 = json.load(infile, object_pairs_hook=OrderedDict)
    with open("tests/example_data/NMRSTAR2/chem_shifts_by_residue_all.json", "r") as infile:
        model_chem_shifts2 = json.load(infile, object_pairs_hook=OrderedDict)

    assert repr(test_chem_shifts1) == repr(model_chem_shifts1)
    assert repr(test_chem_shifts2) == repr(model_chem_shifts2)


def test_chem_shift_by_residue_specific_amino_acid():
    starfile_generator = nmrstarlib.read_files("tests/example_data/NMRSTAR3/bmr18569.str",
                                               "tests/example_data/NMRSTAR2/bmr18569.str")
    starfile1 = next(starfile_generator)
    starfile2 = next(starfile_generator)
    test_chem_shifts1 = starfile1.chem_shifts_by_residue(amino_acids=("SER",), nmrstar_version="3")
    test_chem_shifts2 = starfile2.chem_shifts_by_residue(amino_acids=("SER",), nmrstar_version="2")

    with open("tests/example_data/NMRSTAR3/chem_shifts_by_residue_SER.json", "r") as infile:
        model_chem_shifts1 = json.load(infile, object_pairs_hook=OrderedDict)
    with open("tests/example_data/NMRSTAR2/chem_shifts_by_residue_SER.json", "r") as infile:
        model_chem_shifts2 = json.load(infile, object_pairs_hook=OrderedDict)

    assert repr(test_chem_shifts1) == repr(model_chem_shifts1)
    assert repr(test_chem_shifts2) == repr(model_chem_shifts2)


def test_chem_shift_by_residue_specific_amino_acid_specific_atoms():
    starfile_generator = nmrstarlib.read_files("tests/example_data/NMRSTAR3/bmr18569.str",
                                               "tests/example_data/NMRSTAR2/bmr18569.str")
    starfile1 = next(starfile_generator)
    starfile2 = next(starfile_generator)
    test_chem_shifts1 = starfile1.chem_shifts_by_residue(amino_acids=("SER",), atoms=("CA", "CB"), nmrstar_version="3")
    test_chem_shifts2 = starfile2.chem_shifts_by_residue(amino_acids=("SER",), atoms=("CA", "CB"), nmrstar_version="2")

    with open("tests/example_data/NMRSTAR3/chem_shifts_by_residue_SER_CA_CB.json", "r") as infile:
        model_chem_shifts1 = json.load(infile, object_pairs_hook=OrderedDict)
    with open("tests/example_data/NMRSTAR2/chem_shifts_by_residue_SER_CA_CB.json", "r") as infile:
        model_chem_shifts2 = json.load(infile, object_pairs_hook=OrderedDict)

    assert repr(test_chem_shifts1) == repr(model_chem_shifts1)
    assert repr(test_chem_shifts2) == repr(model_chem_shifts2)