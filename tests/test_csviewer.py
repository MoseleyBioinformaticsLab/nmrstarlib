import shutil
from nmrstarlib.csviewer import CSViewer


def teardown_module(module):
    shutil.rmtree("tests/example_data/NMRSTAR3/tmp")
    shutil.rmtree("tests/example_data/NMRSTAR2/tmp")


def test_csviewer_all():
    csviewer = CSViewer(from_path="tests/example_data/NMRSTAR3/bmr18569.str",
                        amino_acids=(),
                        atoms=(),
                        filename="tests/example_data/NMRSTAR3/tmp/18569",
                        csview_format="png",
                        nmrstar_version="3")
    csviewer.csview(view=False)

    csviewer = CSViewer(from_path="tests/example_data/NMRSTAR2/bmr18569.str",
                        amino_acids=(),
                        atoms=(),
                        filename="tests/example_data/NMRSTAR2/tmp/18569",
                        csview_format="png",
                        nmrstar_version="2")
    csviewer.csview(view=False)


def test_csviewer_specific_amino_acid():
    csviewer = CSViewer(from_path="tests/example_data/NMRSTAR3/bmr18569.str",
                        amino_acids=("SER",),
                        atoms=(),
                        filename="tests/example_data/NMRSTAR3/tmp/18569_SER",
                        csview_format="png",
                        nmrstar_version="3")
    csviewer.csview(view=False)

    csviewer = CSViewer(from_path="tests/example_data/NMRSTAR2/bmr18569.str",
                        amino_acids=("SER",),
                        atoms=(),
                        filename="tests/example_data/NMRSTAR2/tmp/18569_SER",
                        csview_format="png",
                        nmrstar_version="2")
    csviewer.csview(view=False)


def test_csviewer_specific_amino_acid_specific_atom():
    csviewer = CSViewer(from_path="tests/example_data/NMRSTAR3/bmr18569.str",
                        amino_acids=("SER",),
                        atoms=("CA", "CB"),
                        filename="tests/example_data/NMRSTAR3/tmp/18569_SER_CA_CB",
                        csview_format="png",
                        nmrstar_version="3")
    csviewer.csview(view=False)

    csviewer = CSViewer(from_path="tests/example_data/NMRSTAR2/bmr18569.str",
                        amino_acids=("SER",),
                        atoms=("CA", "CB"),
                        filename="tests/example_data/NMRSTAR2/tmp/18569_SER_CA_CB",
                        csview_format="png",
                        nmrstar_version="2")
    csviewer.csview(view=False)