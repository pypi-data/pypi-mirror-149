import unittest
from gbprocess.utils import fasta_to_dict
from data import barcodes, empty_barcode
from tempfile import TemporaryDirectory


class TestBarcodes(unittest.TestCase):
    def setUp(self):
        self.tempdir = TemporaryDirectory()

    def tearDown(self):
        self.tempdir.cleanup()

    def test_creates_valid_dict(self):
        barcodes_file = self.tempdir.name + "/barcodes.fasta"
        with open(self.tempdir.name + "/barcodes.fasta", "w+") as barcodes_fh:
            barcodes_fh.write(barcodes())
            barcodes_fh.flush()
        result = fasta_to_dict(barcodes_file)
        self.assertDictEqual(result, {"barcode1": "CCGAT", "barcode2": "AGAGC"})

    def test_empty_barcode_raises(self):
        barcodes_file = self.tempdir.name + "/barcodes.fasta"
        with open(self.tempdir.name + "/barcodes.fasta", "w+") as barcodes_fh:
            barcodes_fh.write(empty_barcode())
            barcodes_fh.flush()
        with self.assertRaises(ValueError):
            fasta_to_dict(barcodes_file)
