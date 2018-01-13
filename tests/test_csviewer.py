import os
import shutil
import pytest

from nmrstarlib.csviewer import CSViewer


def teardown_module(module, paths=("tests/example_data/NMRSTAR3/tmp",
                                   "tests/example_data/NMRSTAR2/tmp")):
    for path in paths:
        if os.path.exists(path):
            shutil.rmtree(path)


@pytest.mark.parametrize("amino_acids,atoms", [
    (None, None),
    (["SER", "MET"], None),
    (["SER", "MET"], ["CA", "CB"])
])
def test_csviewer(amino_acids, atoms):
    csviewer = CSViewer(from_path="tests/example_data/NMRSTAR3/bmr18569.str",
                        amino_acids=amino_acids,
                        atoms=atoms,
                        filename="tests/example_data/NMRSTAR3/tmp/18569",
                        csview_format="png",
                        nmrstar_version="3")
    csviewer.csview(view=False)

    csviewer = CSViewer(from_path="tests/example_data/NMRSTAR2/bmr18569.str",
                        amino_acids=amino_acids,
                        atoms=atoms,
                        filename="tests/example_data/NMRSTAR2/tmp/18569",
                        csview_format="png",
                        nmrstar_version="2")
    csviewer.csview(view=False)
