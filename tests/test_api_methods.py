import json
from collections import OrderedDict
from nmrstarlib import nmrstarlib


def test_chem_shift_by_residue_all():
    starfile_generator = nmrstarlib.read_files("tests/example_data/bmr18569.str")
    starfile = next(starfile_generator)
    test_chem_shifts = starfile.chem_shifts_by_residue()

    with open("tests/example_data/chem_shifts_by_residue_all.json", "r") as infile:
        model_chem_shifts = json.load(infile, object_pairs_hook=OrderedDict)

    assert repr(test_chem_shifts) == repr(model_chem_shifts)


def test_chem_shift_by_residue_specific_amino_acid():
    starfile_generator = nmrstarlib.read_files("tests/example_data/bmr18569.str")
    starfile = next(starfile_generator)
    test_chem_shifts = starfile.chem_shifts_by_residue(aminoacids=("SER"))

    with open("tests/example_data/chem_shifts_by_residue_SER.json", "r") as infile:
        model_chem_shifts = json.load(infile, object_pairs_hook=OrderedDict)

    assert repr(test_chem_shifts) == repr(model_chem_shifts)


def test_chem_shift_by_residue_specific_amino_acid_specific_atoms():
    starfile_generator = nmrstarlib.read_files("tests/example_data/bmr18569.str")
    starfile = next(starfile_generator)
    test_chem_shifts = starfile.chem_shifts_by_residue(aminoacids=("SER"), atoms=("CA", "CB"))

    with open("tests/example_data/chem_shifts_by_residue_SER_CA_CB.json", "r") as infile:
        model_chem_shifts = json.load(infile, object_pairs_hook=OrderedDict)

    assert repr(test_chem_shifts) == repr(model_chem_shifts)