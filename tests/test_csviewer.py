import shutil
from nmrstarlib.csviewer import CSViewer


def teardown_module(module):
    shutil.rmtree("tests/example_data/tmp")


def test_csviewer_all():
    csviewer = CSViewer(from_path="tests/example_data/bmr18569.str",
                        aminoacids=(),
                        atoms=(),
                        filename="tests/example_data/tmp/18569",
                        csview_format="png")
    csviewer.csview(view=False)


def test_csviewer_specific_amino_acid():
    csviewer = CSViewer(from_path="tests/example_data/bmr18569.str",
                        aminoacids=("SER",),
                        atoms=(),
                        filename="tests/example_data/tmp/18569_SER",
                        csview_format="png")
    csviewer.csview(view=False)


def test_csviewer_specific_amino_acid_specific_atom():
    csviewer = CSViewer(from_path="tests/example_data/bmr18569.str",
                        aminoacids=("SER",),
                        atoms=("CA", "CB"),
                        filename="tests/example_data/tmp/18569_SER_CA_CB",
                        csview_format="png")
    csviewer.csview(view=False)