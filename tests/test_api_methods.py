import json
import collections
import pytest

from nmrstarlib import nmrstarlib


@pytest.mark.parametrize("test_input,test_output,amino_acids,atoms,amino_acids_and_atoms", [
    (("tests/example_data/NMRSTAR3/bmr18569.str", "tests/example_data/NMRSTAR2/bmr18569.str"),
     ("tests/example_data/NMRSTAR3/chem_shifts_by_residue_all.json", "tests/example_data/NMRSTAR2/chem_shifts_by_residue_all.json"),
     None, None, None),

    (("tests/example_data/NMRSTAR3/bmr18569.str", "tests/example_data/NMRSTAR2/bmr18569.str"),
     ("tests/example_data/NMRSTAR3/chem_shifts_by_residue_SER.json", "tests/example_data/NMRSTAR2/chem_shifts_by_residue_SER.json"),
     ["SER"], None, None),

    (("tests/example_data/NMRSTAR3/bmr18569.str", "tests/example_data/NMRSTAR2/bmr18569.str"),
     ("tests/example_data/NMRSTAR3/chem_shifts_by_residue_CA_CB.json", "tests/example_data/NMRSTAR2/chem_shifts_by_residue_CA_CB.json"),
     None, ["CA", "CB"], None),

    (("tests/example_data/NMRSTAR3/bmr18569.str", "tests/example_data/NMRSTAR2/bmr18569.str"),
     ("tests/example_data/NMRSTAR3/chem_shifts_by_residue_SER_CA_CB.json", "tests/example_data/NMRSTAR2/chem_shifts_by_residue_SER_CA_CB.json"),
     ["SER"], ["CA", "CB"], None),

    (("tests/example_data/NMRSTAR3/bmr18569.str", "tests/example_data/NMRSTAR2/bmr18569.str"),
     ("tests/example_data/NMRSTAR3/chem_shifts_by_residue_SER_HA_CA_MET_CA_CB.json", "tests/example_data/NMRSTAR2/chem_shifts_by_residue_SER_HA_CA_MET_CA_CB.json"),
     None, None, {"SER":["HA", "CA"], "MET":["CA", "CB"]})
])
def test_chem_shifts_by_residue_all(test_input, test_output, amino_acids, atoms, amino_acids_and_atoms):
    input_file_path1, input_file_path2 = test_input
    output_file_path1, output_file_path2 = test_output

    starfile_generator = nmrstarlib.read_files(input_file_path1, input_file_path2)
    starfile1 = next(starfile_generator)
    starfile2 = next(starfile_generator)
    test_chem_shifts1 = starfile1.chem_shifts_by_residue(amino_acids=amino_acids,
                                                         atoms=atoms,
                                                         amino_acids_and_atoms=amino_acids_and_atoms,
                                                         nmrstar_version="3")

    test_chem_shifts2 = starfile2.chem_shifts_by_residue(amino_acids=amino_acids,
                                                         atoms=atoms,
                                                         amino_acids_and_atoms=amino_acids_and_atoms,
                                                         nmrstar_version="2")

    with open(output_file_path1, "r") as infile:
        model_chem_shifts1 = json.load(infile, object_pairs_hook=collections.OrderedDict)
    with open(output_file_path2, "r") as infile:
        model_chem_shifts2 = json.load(infile, object_pairs_hook=collections.OrderedDict)

    assert repr(test_chem_shifts1) == repr(model_chem_shifts1)
    assert repr(test_chem_shifts2) == repr(model_chem_shifts2)
