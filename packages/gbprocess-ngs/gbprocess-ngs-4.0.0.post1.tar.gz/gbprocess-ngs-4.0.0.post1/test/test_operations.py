import unittest
import shutil
from pathlib import Path
from tempfile import TemporaryDirectory
from textwrap import dedent

from gbprocess.data import SequencingData, PairedEndFastq, SingleEndFastq
from gbprocess.operations.demultiplexing import CutadaptDemultiplex
from gbprocess.operations.merging import Pear
from gbprocess.operations.filtering import (
    AverageQualityFilter,
    LengthFilter,
    MaxNFilter,
    RemovePatternFilter,
    SlidingWindowQualityFilter,
)
from gbprocess.operations.trimming import (
    CutadaptTrimmer,
    SingleEndTrimmer,
    PairedEndTrimmer,
)
from utils import CustomTestCase

from data import (
    barcodes,
    fastq_forward,
    fastq_reverse,
    invalid_fastq_content,
    fastq_forward_spacer,
    fastq_reverse_spacer,
    fastq_single_end_spacer,
)


class CustomOperationTestCase(CustomTestCase):
    def setUp(self):
        self.tempdir = TemporaryDirectory()
        self.barcodes = self.tempdir.name + "/barcodes.fasta"
        forward_fastq = self.tempdir.name + "/17146FL-13-01-01_S97_L002_R1_001.fastq"
        reverse_fastq = self.tempdir.name + "/17146FL-13-01-01_S97_L002_R2_001.fastq"
        invalid_fastq_file = self.tempdir.name + "/invalid.fastq"
        with open(forward_fastq, "w+") as temp_file_forward, open(
            reverse_fastq, "w+"
        ) as temp_file_reverse, open(self.barcodes, "w+") as barcodes_file, open(
            invalid_fastq_file, "w+"
        ) as invalid_file:
            temp_file_forward.write(fastq_forward())
            temp_file_reverse.write(fastq_reverse())
            barcodes_file.write(barcodes())
            invalid_file.write(invalid_fastq_content())
        self.barcodes = self.tempdir.name + "/barcodes.fasta"
        self.paired_fastq = PairedEndFastq(
            forward_fastq,
            reverse_fastq,
            run="17146FL-13-01-01_S97",
            extension=".fastq",
            orientation=[1, 2],
            exists_ok=True,
        )
        self.single_end_fastq = SingleEndFastq(
            forward_fastq,
            run="17146FL-13-01-01_S97",
            extension=".fastq",
            exists_ok=True,
        )
        self.invalid_fastq = SingleEndFastq(
            invalid_fastq_file, run="invalid", extension=".fastq", exists_ok=True
        )

    def tearDown(self):
        self.tempdir.cleanup()

    def assertFileContentEquals(self, file_to_check, contents):
        with file_to_check.open("r") as fh:
            file_contents = fh.read().strip()
            self.assertMultiLineEqual(file_contents, contents)


class TestPear(CustomOperationTestCase):
    def setUp(self):
        self.merged_read = dedent(
            """\
                                     @EU861894-140/1
                                     CCGATCTCTCGGGCTGTCCGGGGATTTCAAACCCTGGTAAGGTTCTTCGGTTAGTGACGAATTAATGCACATGCTCCACCGCTTGTGCGGGCCCCCGTCAATTCACT
                                     +
                                     ??CFFF?AIIAHEIII?IIIHIIII#IIIII?#IIIIIIFI=IIIIII9IIIIIIIIIIIIIEIIIIIIIBI@DBHIIIIIIIICIIII?IIIIADCIIIFF1F@1@
                                  """
        ).strip()
        super().setUp()

    @unittest.skipIf(not shutil.which("pear"), "PEAR not available")
    def test_merge_single_raises(self):
        merger = Pear(
            minimum_overlap=1,
            minimum_length=1,
            output_directory=self.tempdir.name,
            output_file_name_template="{run}{extension}",
        )
        with self.assertRaises(ValueError):
            merger.perform(self.single_end_fastq)

    @unittest.skipIf(not shutil.which("pear"), "PEAR not available")
    def test_merge_paired(self):
        merger = Pear(
            minimum_overlap=1,
            minimum_length=1,
            output_directory=self.tempdir.name,
            output_file_name_template="{run}{extension}",
        )
        output_seq_data, _ = merger.perform(self.paired_fastq)
        (fastq,) = output_seq_data
        (forward,) = fastq.files

        # Check file contents
        self.assertFileContentEquals(forward, self.merged_read)

        # Check output directory
        self.assertTrue(self.tempdir.name == str(forward.parent))

        # Check file names
        run = self.paired_fastq.run
        extension = self.paired_fastq.extension
        self.assertTrue(forward.name == f"{run}{extension}")

    @unittest.skipIf(not shutil.which("pear"), "PEAR not available")
    def test_prevent_rename_extension(self):
        forward_fastq = self.tempdir.name + "/17146FL-13-01-01_S97_L002_R1_001.fq"
        reverse_fastq = self.tempdir.name + "/17146FL-13-01-01_S97_L002_R2_001.fq"

        with open(forward_fastq, "w+") as temp_file_forward, open(
            reverse_fastq, "w+"
        ) as temp_file_reverse:
            temp_file_reverse.write(fastq_reverse())
            temp_file_forward.write(fastq_forward())
        self.paired_fastq = PairedEndFastq(
            forward_fastq,
            reverse_fastq,
            run="17146FL-13-01-01_S97",
            extension=".fq",
            orientation=[1, 2],
            exists_ok=True,
        )
        merger = Pear(
            minimum_overlap=1,
            minimum_length=1,
            output_directory=self.tempdir.name,
            output_file_name_template="{run}{extension}",
        )
        _ = merger.perform(self.paired_fastq)
        self.assertEqual(self.paired_fastq.extension, ".fq")


class TestDemultiplexing(CustomOperationTestCase):
    def setUp(self):
        self.barcode1_forward_read = dedent(
            """\
                                            @EU861894-140/1
                                            CCGATCTCTCGGCCTGCCCGGGGATCTCAAACNCTGGTAAGCTTCTCCGGTTAGTGACGAATCACTGTACCTGCTCCACCGCTTGTGCGGGCCCTCGTCA
                                            +
                                            ??CFFF?;HHAH#III#I:IHJIJG#JIJJI?3IIJ0JJ#G3JGHG#I90?HIJG9JEIIBD#C#G@#C=)I@#BHBBCDCD;ACDCB;??CD>#D#:DA

                                            """
        ).strip()
        self.barcode2_forward_read = dedent(
            """\
                                                @EU861894-138/1
                                                AGAGCGCATCCACATGTGGTCCCCCGCTTCGGGGCAGGTTGCCCACGTGTTACGCGACCGTTCGCCATTAACCAC
                                                +
                                                @CCF:#@DHHG?BAJJG0BII#GI8;FJIBFBHGJI>+EC=BECBDCHDEAAD#=E6DDFF=9CD#A#8H@@>#D

                                            """
        ).strip()
        self.barcode1_reverse_read = dedent(
            """\
                                                @EU861894-140/2
                                                AGTGAATTGACAGGGGCACGCATAAGCGGTGCGGTATGTGCATTAATTCGTCACTAACTGAAGAACCTCACCAGGCTTTGAAACCCACGGAGAGCGGGAG
                                                +
                                                @1@F1FFEFFA#AGGJB!EHDI434:J?GJI##B#)BJIICJJGEBFIBJ>GGDJIGI#)II<H6=ID#E?CD4##CDEFB#C#CA#-<#?#FCE#!DC'

                                            """
        ).strip()
        self.barcode2_reverse_read = dedent(
            """\
                                                @EU861894-138/2
                                                CTTCGGGGGTGGTTAGGCAACCCCCCCCGAAGCGGGGGACAACAGCCTTAAACGGTTCCTAATACCGCATGGTGA
                                                +
                                                BB@FB2@FHB2HFJGFFHJ?8=##JDGHDEIBH?H#HI)EFFEF#C#B#HE?#D?#;#DDCA#:DD>BCB###D'

                                            """
        ).strip()

        super().setUp()

    def test_demultiplexing_paired(self):
        demultiplexer = CutadaptDemultiplex(
            error_rate=0.0,
            barcodes=self.barcodes,
            output_file_name_template="{sample_name}_{run}_{orientation}{extension}",
            output_directory=self.tempdir.name,
        )
        output_seq_data, _ = demultiplexer.perform(self.paired_fastq)
        output_fastq1, output_fastq2 = output_seq_data
        forward_1, reverse_1 = output_fastq1.files
        forward_2, reverse_2 = output_fastq2.files

        # Check file contents
        self.assertFileContentEquals(forward_1, self.barcode1_forward_read)
        self.assertFileContentEquals(forward_2, self.barcode2_forward_read)
        self.assertFileContentEquals(reverse_1, self.barcode1_reverse_read)
        self.assertFileContentEquals(reverse_2, self.barcode2_reverse_read)

        # Check output directory
        parents = set([forward_1.parent, reverse_1.parent, forward_2.parent, reverse_2.parent])
        self.assertTrue(len(parents) == 1)
        self.assertTrue(self.tempdir.name == str(parents.pop()))

        # Check file names
        run = self.single_end_fastq.run
        extension = self.single_end_fastq.extension
        self.assertTrue(forward_1.name == f"barcode1_{run}_1{extension}")
        self.assertTrue(reverse_1.name == f"barcode1_{run}_2{extension}")
        self.assertTrue(forward_2.name == f"barcode2_{run}_1{extension}")
        self.assertTrue(reverse_2.name == f"barcode2_{run}_2{extension}")

    def test_demultiplexing_single(self):
        demultiplexer = CutadaptDemultiplex(
            error_rate=0.0,
            barcodes=self.barcodes,
            output_file_name_template="{sample_name}_{run}{extension}",
            output_directory=self.tempdir.name,
        )
        output_seq_data, _ = demultiplexer.perform(self.single_end_fastq)
        output_fastq1, output_fastq2 = output_seq_data
        (fastq1,) = output_fastq1.files
        (fastq2,) = output_fastq2.files
        # Check file contents
        self.assertFileContentEquals(fastq1, self.barcode1_forward_read)
        self.assertFileContentEquals(fastq2, self.barcode2_forward_read)

        # Checkout output file directories
        self.assertTrue(fastq1.parent == fastq2.parent)
        self.assertTrue(self.tempdir.name == str(fastq1.parent))

        # Check file names
        run = self.single_end_fastq.run
        extension = self.single_end_fastq.extension
        self.assertTrue(fastq1.name == f"barcode1_{run}{extension}")
        self.assertTrue(fastq2.name == f"barcode2_{run}{extension}")

    def test_demultiplexing_paired_with_remnant(self):
        demultiplexer = CutadaptDemultiplex(
            error_rate=0.0,
            barcodes=self.barcodes,
            output_file_name_template="{sample_name}_{run}_{orientation}{extension}",
            output_directory=self.tempdir.name,
            barcode_side_cutsite_remnant="AGAG",
        )
        output_seq_data, _ = demultiplexer.perform(self.paired_fastq)
        output_fastq1, output_fastq2 = output_seq_data
        forward_1, reverse_1 = output_fastq1.files
        forward_2, reverse_2 = output_fastq2.files

        # Check file contents
        self.assertFileContentEquals(forward_1, self.barcode1_forward_read)
        self.assertFileContentEquals(forward_2, "")
        self.assertFileContentEquals(reverse_1, self.barcode1_reverse_read)
        self.assertFileContentEquals(reverse_2, "")

        # Check output directory
        parents = set([forward_1.parent, reverse_1.parent, forward_2.parent, reverse_2.parent])
        self.assertTrue(len(parents) == 1)
        self.assertTrue(self.tempdir.name == str(parents.pop()))

        # Check file names
        run = self.single_end_fastq.run
        extension = self.single_end_fastq.extension
        self.assertTrue(forward_1.name == f"barcode1_{run}_1{extension}")
        self.assertTrue(reverse_1.name == f"barcode1_{run}_2{extension}")
        self.assertTrue(forward_2.name == f"barcode2_{run}_1{extension}")
        self.assertTrue(reverse_2.name == f"barcode2_{run}_2{extension}")

    def test_demultiplexing_single_with_remnant(self):
        demultiplexer = CutadaptDemultiplex(
            error_rate=0.0,
            barcodes=self.barcodes,
            output_file_name_template="{sample_name}_{run}{extension}",
            output_directory=self.tempdir.name,
            barcode_side_cutsite_remnant="AGAG",
        )
        output_seq_data, _ = demultiplexer.perform(self.single_end_fastq)
        output_fastq1, output_fastq2 = output_seq_data
        (fastq1,) = output_fastq1.files
        (fastq2,) = output_fastq2.files
        # Check file contents
        self.assertFileContentEquals(fastq1, self.barcode1_forward_read)
        self.assertFileContentEquals(fastq2, "")

        # Checkout output file directories
        self.assertTrue(fastq1.parent == fastq2.parent)
        self.assertTrue(self.tempdir.name == str(fastq1.parent))

        # Check file names
        run = self.single_end_fastq.run
        extension = self.single_end_fastq.extension
        self.assertTrue(fastq1.name == f"barcode1_{run}{extension}")
        self.assertTrue(fastq2.name == f"barcode2_{run}{extension}")

    def test_barcodes_file_does_not_exist(self):
        with self.assertRaises(ValueError):
            CutadaptDemultiplex(
                error_rate=0.5,
                barcodes="foo",
                output_file_name_template="{sample_name}_{run}_{orientation}{extension}",
                output_directory=self.tempdir.name,
            )

    def test_demultiplexing_error_rate_boundry_raises(self):
        with self.assertRaises(AssertionError):
            CutadaptDemultiplex(
                error_rate=2,
                barcodes=self.barcodes,
                output_file_name_template="{sample_name}_{run}_{orientation}{extension}",
                output_directory=self.tempdir.name,
            )

    def test_demultiplexing_error_rate_not_float_raises(self):
        with self.assertRaises(ValueError):
            CutadaptDemultiplex(
                error_rate="a",
                barcodes=self.barcodes,
                output_file_name_template="{sample_name}_{run}_{orientation}{extension}",
                output_directory=self.tempdir.name,
            )

    def test_barcode_side_cutsite_remnant_not_dna(self):
        with self.assertRaises(ValueError):
            CutadaptDemultiplex(
                error_rate=0.5,
                barcodes=self.barcodes,
                output_file_name_template="{sample_name}_{run}_{orientation}{extension}",
                output_directory=self.tempdir.name,
                barcode_side_cutsite_remnant="EEEE",
            )

    def test_empty_barcodes_file(self):
        open(self.barcodes, "w").close()
        with self.assertRaises(ValueError):
            CutadaptDemultiplex(
                error_rate=0.5,
                barcodes=self.barcodes,
                output_file_name_template="{sample_name}_{run}_{orientation}{extension}",
                output_directory=self.tempdir.name,
            )

    def test_pass_no_fastq(self):
        demultiplexer = CutadaptDemultiplex(
            error_rate=0.0,
            barcodes=self.barcodes,
            output_file_name_template="{sample_name}_{run}_{orientation}{extension}",
            output_directory=self.tempdir.name,
        )
        with self.assertRaises(ValueError):
            demultiplexer.perform(None)


class TestDiscardMaxN(CustomOperationTestCase):
    def setUp(self):
        self.forward_out = dedent(
            """
                                @EU861894-138/1
                                AGAGCGCATCCACATGTGGTCCCCCGCTTCGGGGCAGGTTGCCCACGTGTTACGCGACCGTTCGCCATTAACCAC
                                +
                                @CCF:#@DHHG?BAJJG0BII#GI8;FJIBFBHGJI>+EC=BECBDCHDEAAD#=E6DDFF=9CD#A#8H@@>#D
                                """
        ).strip()
        self.reverse_out = dedent(
            """
                                @EU861894-138/2
                                CTTCGGGGGTGGTTAGGCAACCCCCCCCGAAGCGGGGGACAACAGCCTTAAACGGTTCCTAATACCGCATGGTGA
                                +
                                BB@FB2@FHB2HFJGFFHJ?8=##JDGHDEIBH?H#HI)EFFEF#C#B#HE?#D?#;#DDCA#:DD>BCB###D'
                                """
        ).strip()

        super().setUp()

    def test_filter_max_paired(self):
        filter_operation = MaxNFilter(
            max_n=0,
            output_directory=self.tempdir.name,
            output_file_name_template="{run}_{orientation}{extension}",
        )
        output_seq_data, _ = filter_operation.perform(self.paired_fastq)
        (fastq,) = output_seq_data
        forward, reverse = fastq.files

        # Check file contents
        self.assertFileContentEquals(forward, self.forward_out)
        self.assertFileContentEquals(reverse, self.reverse_out)

        # Check output directory
        self.assertTrue(forward.parent == reverse.parent)
        self.assertTrue(self.tempdir.name == str(forward.parent))

        # Check file names
        run = self.paired_fastq.run
        extension = self.paired_fastq.extension
        self.assertTrue(forward.name == f"{run}_1{extension}")
        self.assertTrue(reverse.name == f"{run}_2{extension}")

    def test_filter_max_single(self):
        filter_operation = MaxNFilter(
            max_n=0,
            output_directory=self.tempdir.name,
            output_file_name_template="{run}{extension}",
        )
        output_seq_data, _ = filter_operation.perform(self.single_end_fastq)
        (fastq,) = output_seq_data
        (forward,) = fastq.files
        # Check file contents
        self.assertFileContentEquals(forward, self.forward_out)

        # Check output directory
        self.assertTrue(str(forward.parent) == self.tempdir.name)

        # Check output name
        run = self.single_end_fastq.run
        extension = self.single_end_fastq.extension
        self.assertTrue(str(forward.name) == f"{run}{extension}")

    def test_max_n_bounds(self):
        with self.assertRaises(ValueError):
            MaxNFilter(
                max_n=-1,
                output_directory=self.tempdir.name,
                output_file_name_template="{run}{extension}",
            )

    def test_empty_fastq_input(self):
        empty_file = Path(self.tempdir.name + "/empty.fastq")
        empty_file.touch()
        empty_fastq = SingleEndFastq(
            empty_file, run="empty_output", extension=".fastq", exists_ok=True
        )
        filter_operation = MaxNFilter(
            max_n=0,
            output_directory=self.tempdir.name,
            output_file_name_template="{run}{extension}",
        )
        output_seq, _ = filter_operation.perform(empty_fastq)
        (fastq,) = output_seq
        self.assertTrue(fastq.empty)

    def test_pass_no_fastq(self):
        filter_operation = MaxNFilter(
            max_n=0,
            output_directory=self.tempdir.name,
            output_file_name_template="{run}{extension}",
        )
        with self.assertRaises(ValueError):
            filter_operation.perform(None)


class TestLengthFilter(CustomOperationTestCase):
    def setUp(self):
        self.forward_out = dedent(
            """
                                @EU861894-140/1
                                CCGATCTCTCGGCCTGCCCGGGGATCTCAAACNCTGGTAAGCTTCTCCGGTTAGTGACGAATCACTGTACCTGCTCCACCGCTTGTGCGGGCCCTCGTCA
                                +
                                ??CFFF?;HHAH#III#I:IHJIJG#JIJJI?3IIJ0JJ#G3JGHG#I90?HIJG9JEIIBD#C#G@#C=)I@#BHBBCDCD;ACDCB;??CD>#D#:DA
                                """
        ).strip()
        self.reverse_out = dedent(
            """
                                @EU861894-140/2
                                AGTGAATTGACAGGGGCACGCATAAGCGGTGCGGTATGTGCATTAATTCGTCACTAACTGAAGAACCTCACCAGGCTTTGAAACCCACGGAGAGCGGGAG
                                +
                                @1@F1FFEFFA#AGGJB!EHDI434:J?GJI##B#)BJIICJJGEBFIBJ>GGDJIGI#)II<H6=ID#E?CD4##CDEFB#C#CA#-<#?#FCE#!DC'
                                """
        ).strip()
        super().setUp()

    def test_filter_length_paired(self):
        filter_operation = LengthFilter(
            minimum_length=100,
            output_directory=self.tempdir.name,
            output_file_name_template="{run}_{orientation}{extension}",
        )
        output_seq_data, _ = filter_operation.perform(self.paired_fastq)
        (fastq,) = output_seq_data
        forward, reverse = fastq.files

        # Check output file contents
        self.assertFileContentEquals(forward, self.forward_out)
        self.assertFileContentEquals(reverse, self.reverse_out)

        # Check output directory
        self.assertEqual(forward.parent, reverse.parent)
        self.assertEqual(self.tempdir.name, str(forward.parent))

        # Check output name
        run = self.single_end_fastq.run
        extension = self.single_end_fastq.extension
        self.assertEqual(forward.name, f"{run}_1{extension}")
        self.assertEqual(reverse.name, f"{run}_2{extension}")

    def test_filter_length_single(self):
        filter_operation = LengthFilter(
            minimum_length=100,
            output_directory=self.tempdir.name,
            output_file_name_template="{run}{extension}",
        )
        output_seq_data, _ = filter_operation.perform(self.single_end_fastq)
        (fastq,) = output_seq_data
        (forward,) = fastq.files

        # Check file contents
        self.assertFileContentEquals(forward, self.forward_out)

        # Check output directory
        self.assertEqual(str(forward.parent), self.tempdir.name)

        # Check output name
        run = self.single_end_fastq.run
        extension = self.single_end_fastq.extension
        self.assertEqual(str(forward.name), f"{run}{extension}")

    def test_filter_single_end_until_empty(self):
        filter_operation = LengthFilter(
            minimum_length=1000,
            output_directory=self.tempdir.name,
            output_file_name_template="{run}{extension}",
        )
        output_seq_data, _ = filter_operation.perform(self.single_end_fastq)
        (fastq,) = output_seq_data
        self.assertTrue(fastq.empty)

    def test_filter_paired_end_until_empty(self):
        filter_operation = LengthFilter(
            minimum_length=1000,
            output_directory=self.tempdir.name,
            output_file_name_template="{run}_{orientation}{extension}",
        )
        output_seq_data, _ = filter_operation.perform(self.paired_fastq)
        (fastq,) = output_seq_data
        self.assertTrue(fastq.empty)

    def test_filter_length_out_of_bounds(self):
        with self.assertRaises(ValueError):
            LengthFilter(
                minimum_length=-1,
                output_directory=self.tempdir.name,
                output_file_name_template="{run}{extension}",
            )

    def test_filter_length_to_be_zero(self):
        # No filtering
        filter_operation = LengthFilter(
            minimum_length=0,
            output_directory=self.tempdir.name,
            output_file_name_template="{run}{extension}",
        )

        output_seq_data, _ = filter_operation.perform(self.single_end_fastq)
        (fastq,) = output_seq_data
        (forward,) = fastq.files
        # Check if contents is still the same
        self.assertFileContentEquals(forward, fastq_forward())

    def test_empty_input_fastq(self):
        empty_file = Path(self.tempdir.name + "/empty.fastq")
        empty_file.touch()
        empty_fastq = SingleEndFastq(
            empty_file, run="empty_output", extension=".fastq", exists_ok=True
        )
        filter_operation = LengthFilter(
            minimum_length=100,
            output_directory=self.tempdir.name,
            output_file_name_template="{run}{extension}",
        )
        output_seq, _ = filter_operation.perform(empty_fastq)
        (fastq,) = output_seq
        self.assertTrue(fastq.empty)


class TestAverageQualityFilter(CustomOperationTestCase):
    def setUp(self):
        self.forward_out = dedent(
            """
                                @EU861894-140/1
                                CCGATCTCTCGGCCTGCCCGGGGATCTCAAACNCTGGTAAGCTTCTCCGGTTAGTGACGAATCACTGTACCTGCTCCACCGCTTGTGCGGGCCCTCGTCA
                                +
                                ??CFFF?;HHAH#III#I:IHJIJG#JIJJI?3IIJ0JJ#G3JGHG#I90?HIJG9JEIIBD#C#G@#C=)I@#BHBBCDCD;ACDCB;??CD>#D#:DA
                                """
        ).strip()
        self.reverse_out = dedent(
            """
                                @EU861894-140/2
                                AGTGAATTGACAGGGGCACGCATAAGCGGTGCGGTATGTGCATTAATTCGTCACTAACTGAAGAACCTCACCAGGCTTTGAAACCCACGGAGAGCGGGAG
                                +
                                @1@F1FFEFFA#AGGJB!EHDI434:J?GJI##B#)BJIICJJGEBFIBJ>GGDJIGI#)II<H6=ID#E?CD4##CDEFB#C#CA#-<#?#FCE#!DC'
                                """
        ).strip()
        self.single_out = dedent(
            """
                                @EU861894-138/1
                                AGAGCGCATCCACATGTGGTCCCCCGCTTCGGGGCAGGTTGCCCACGTGTTACGCGACCGTTCGCCATTAACCAC
                                +
                                @CCF:#@DHHG?BAJJG0BII#GI8;FJIBFBHGJI>+EC=BECBDCHDEAAD#=E6DDFF=9CD#A#8H@@>#D
                                """
        ).strip()
        super().setUp()

    def test_average_quality_filter_paired(self):
        filter_operation = AverageQualityFilter(
            average_quality=28,
            output_directory=self.tempdir.name,
            output_file_name_template="{run}_{orientation}{extension}",
        )
        output_seq_data, _ = filter_operation.perform(self.paired_fastq)
        (fastq,) = output_seq_data
        forward, reverse = fastq.files
        # Check output file contents
        self.assertFileContentEquals(forward, self.forward_out)
        self.assertFileContentEquals(reverse, self.reverse_out)

        # Check output directory
        self.assertEqual(forward.parent, reverse.parent)
        self.assertEqual(self.tempdir.name, str(forward.parent))

        # Check output name
        run = self.single_end_fastq.run
        extension = self.single_end_fastq.extension
        self.assertEqual(forward.name, f"{run}_1{extension}")
        self.assertEqual(reverse.name, f"{run}_2{extension}")

    def test_average_quality_filter_single(self):
        filter_operation = AverageQualityFilter(
            average_quality=31,
            output_directory=self.tempdir.name,
            output_file_name_template="{run}{extension}",
        )
        output_seq_data, _ = filter_operation.perform(self.single_end_fastq)
        (fastq,) = output_seq_data
        (forward,) = fastq.files

        # Check file contents
        self.assertFileContentEquals(forward, self.single_out)

        # Check output directory
        self.assertEqual(str(forward.parent), self.tempdir.name)

        # Check output name
        run = self.single_end_fastq.run
        extension = self.single_end_fastq.extension
        self.assertEqual(str(forward.name), f"{run}{extension}")

    def test_pass_none(self):
        filter_operation = AverageQualityFilter(
            average_quality=31,
            output_directory=self.tempdir.name,
            output_file_name_template="{run}{extension}",
        )
        with self.assertRaises(ValueError):
            filter_operation.perform(None)

    def test_average_quality_not_int(self):
        with self.assertRaises(ValueError):
            AverageQualityFilter(
                average_quality="a",
                output_directory=self.tempdir.name,
                output_file_name_template="{run}{extension}",
            )

    def test_quality_value_out_of_bounds(self):
        with self.assertRaises(ValueError):
            AverageQualityFilter(
                average_quality=-1,
                output_directory=self.tempdir.name,
                output_file_name_template="{run}{extension}",
            )

    def test_filter_nothing(self):
        filter_operation = AverageQualityFilter(
            average_quality=0,
            output_directory=self.tempdir.name,
            output_file_name_template="{run}{extension}",
        )

        output_seq_data, _ = filter_operation.perform(self.single_end_fastq)
        (fastq,) = output_seq_data
        (forward,) = fastq.files

        # Check file contents
        self.assertFileContentEquals(forward, fastq_forward())

        # Check output directory
        self.assertEqual(str(forward.parent), self.tempdir.name)

        # Check output name
        run = self.single_end_fastq.run
        extension = self.single_end_fastq.extension
        self.assertEqual(str(forward.name), f"{run}{extension}")

    def test_filter_everything(self):
        filter_operation = AverageQualityFilter(
            average_quality=100,
            output_directory=self.tempdir.name,
            output_file_name_template="{run}{extension}",
        )

        output_seq_data, _ = filter_operation.perform(self.single_end_fastq)
        (fastq,) = output_seq_data
        (forward,) = fastq.files

        # Check file contents
        self.assertFileContentEquals(forward, "")

        # Check output directory
        self.assertEqual(str(forward.parent), self.tempdir.name)

        # Check output name
        run = self.single_end_fastq.run
        extension = self.single_end_fastq.extension
        self.assertEqual(str(forward.name), f"{run}{extension}")

    def test_filter_paired_only_one_orientation_passed(self):
        # Forward read passes, but reverse read is below quality threshold
        # Both reads need to be removed
        filter_operation = AverageQualityFilter(
            average_quality=30,
            output_directory=self.tempdir.name,
            output_file_name_template="{run}_{orientation}{extension}",
        )
        output_seq_data, _ = filter_operation.perform(self.paired_fastq)
        (fastq,) = output_seq_data
        forward, reverse = fastq.files
        self.assertFileContentEquals(forward, "")
        self.assertFileContentEquals(reverse, "")

    def test_bad_fastq_format(self):
        filter_operation = AverageQualityFilter(
            average_quality=30,
            output_directory=self.tempdir.name,
            output_file_name_template="output_{run}{extension}",
        )
        with self.assertRaises(ValueError):
            filter_operation.perform(self.invalid_fastq)


class TestSlidingWindowQualityFilter(CustomOperationTestCase):
    def setUp(self):
        self.forward_out = dedent(
            """
                                @EU861894-140/1
                                CCGATCTCTCGGCCTGCCCGGGGATCTCAAACNCTGGTAAGCTTCTCCGGTTAGTGACGAATCACTGTACCTGCTCCACCGCTTGTGCGGGCCCTCGTCA
                                +
                                ??CFFF?;HHAH#III#I:IHJIJG#JIJJI?3IIJ0JJ#G3JGHG#I90?HIJG9JEIIBD#C#G@#C=)I@#BHBBCDCD;ACDCB;??CD>#D#:DA
                                """
        ).strip()
        self.reverse_out = dedent(
            """
                                @EU861894-140/2
                                AGTGAATTGACAGGGGCACGCATAAGCGGTGCGGTATGTGCATTAATTCGTCACTAACTGAAGAACCTCACCAGGCTTTGAAACCCACGGAGAGCGGGAG
                                +
                                @1@F1FFEFFA#AGGJB!EHDI434:J?GJI##B#)BJIICJJGEBFIBJ>GGDJIGI#)II<H6=ID#E?CD4##CDEFB#C#CA#-<#?#FCE#!DC'
                                """
        ).strip()
        super().setUp()

    def test_sliding_window_filter_paired(self):
        filter_operation = SlidingWindowQualityFilter(
            window_size=5,
            average_quality=28,
            count=2,
            output_directory=self.tempdir.name,
            output_file_name_template="{run}_{orientation}{extension}",
        )
        output_seq_data, _ = filter_operation.perform(self.paired_fastq)
        (fastq,) = output_seq_data
        forward, reverse = fastq.files
        # Check output file contents
        self.assertFileContentEquals(forward, self.forward_out)
        self.assertFileContentEquals(reverse, self.reverse_out)

        # Check output directory
        self.assertEqual(forward.parent, reverse.parent)
        self.assertEqual(self.tempdir.name, str(forward.parent))

        # Check output name
        run = self.single_end_fastq.run
        extension = self.single_end_fastq.extension
        self.assertEqual(forward.name, f"{run}_1{extension}")
        self.assertEqual(reverse.name, f"{run}_2{extension}")

    def test_sliding_window_filter_single(self):
        filter_operation = SlidingWindowQualityFilter(
            window_size=5,
            average_quality=28,
            count=1,
            output_directory=self.tempdir.name,
            output_file_name_template="{run}{extension}",
        )
        output_seq_data, _ = filter_operation.perform(self.single_end_fastq)
        (fastq,) = output_seq_data
        (forward,) = fastq.files

        # Check file contents
        self.assertFileContentEquals(forward, self.forward_out)

        # Check output directory
        self.assertEqual(str(forward.parent), self.tempdir.name)

        # Check output name
        run = self.single_end_fastq.run
        extension = self.single_end_fastq.extension
        self.assertEqual(str(forward.name), f"{run}{extension}")


class TestCutadaptTrimmer(CustomOperationTestCase):
    def setUp(self):
        super().setUp()
        barcode_content = dedent(
            """
            >sample1
            CCGCTT
            """
        ).strip()

        self.paired_fastq.sample_name = "sample1"
        self.single_end_fastq.sample_name = "sample1"
        self.barcodes = self.tempdir.name + "/barcodes.fasta"
        forward = self.tempdir.name + "/spacer_sample1_barcode1_1.fastq"
        reverse = self.tempdir.name + "/spacer_sample1_barcode1_2.fastq"
        single_end = self.tempdir.name + "/spacersingle_sample1_barcode1_1.fastq"
        with open(self.barcodes, "w") as barcodes_file:
            barcodes_file.write(barcode_content)
        with open(forward, "w+") as forward_fastq:
            forward_fastq.write(fastq_forward_spacer())
        with open(reverse, "w+") as reverse_fastq:
            reverse_fastq.write(fastq_reverse_spacer())
        with open(single_end, "w+") as single_fastq:
            single_fastq.write(fastq_single_end_spacer())

        self.single_end_fastq_with_spacer = SingleEndFastq(
            single_end,
            run="spacersingle",
            sample_name="sample1",
            extension=".fastq",
            orientation="1",
            exists_ok=True,
        )
        self.paired_end_fastq_with_spacer = PairedEndFastq(
            forward,
            reverse,
            run="spacer",
            sample_name="sample1",
            extension=".fastq",
            orientation=("1", "2"),
            exists_ok=True,
        )

    def test_trim_paired_with_spacer(self):
        result_forward_reads = dedent(
            """
                                       @1-5/1
                                       GGGGGGGGGGGGGGGGGGGGGG
                                       +
                                       FFFFFFFFFFFFFFFFFFFFFF
                                       @1-4/1
                                       GGGGGGGGGGGGGGGGGGGGGG
                                       +
                                       FFFFFFFFFFFFFFFFFFFFFF
                                       @1-3/1
                                       GGGGGGGGGGGGGGGGGGGGGG
                                       +
                                       FFFFFFFFFFFFFFFFFFFFFF
                                       @1-2/1
                                       GGGGGGGGGGGGGGGGGGGGGG
                                       +
                                       FFFFFFFFFFFFFFFFFFFFFF
                                       @1-1/1
                                       GGGGGGGGGGGGGGGGGGGGGG
                                       +
                                       FFFFFFFFFFFFFFFFFFFFFF
                                       """
        ).strip()
        result_reverse_reads = dedent(
            """
                                       @1-5/2
                                       GGGGGGGGGGGGGGGGGGGGGG
                                       +
                                       FFFFFFFFFFFFFFFFFFFFFF
                                       @1-4/2
                                       GGGGGGGGGGGGGGGGGGGGGG
                                       +
                                       FFFFFFFFFFFFFFFFFFFFFF
                                       @1-3/2
                                       GGGGGGGGGGGGGGGGGGGGGG
                                       +
                                       FFFFFFFFFFFFFFFFFFFFFF
                                       @1-2/2
                                       GGGGGGGGGGGGGGGGGGGGGG
                                       +
                                       FFFFFFFFFFFFFFFFFFFFFF
                                       @1-1/2
                                       GGGGGGGGGGGGGGGGGGGGGG
                                       +
                                       FFFFFFFFFFFFFFFFFFFFFF
                                       """
        ).strip()
        trim_op = PairedEndTrimmer(
            common_side_sequencing_primer="TruSeq",
            barcode_side_sequencing_primer="TruSeq",
            common_side_cutsite_remnant="TTA",
            barcode_side_cutsite_remnant="CTGCA",
            barcodes=self.barcodes,
            minimum_length=1,
            error_rate=0,
            output_file_name_template="trimmed_{run}_{sample_name}_{orientation}{extension}",
            output_directory=self.tempdir.name,
            spacer="ACGT",
        )
        result_data, aux_data = trim_op.perform(self.paired_end_fastq_with_spacer)
        self.assertIsInstance(result_data, SequencingData)
        fastq_result = list(result_data)
        self.assertEquals(len(fastq_result), 1)
        self.assertIsInstance(fastq_result[0], PairedEndFastq)
        files = fastq_result[0].files
        self.assertFileContentEquals(files[0], result_forward_reads)
        self.assertFileContentEquals(files[1], result_reverse_reads)

    def test_trim_paired(self):
        trim_op = CutadaptTrimmer(
            common_side_sequencing_primer="GTGGAGCAGGTAC",
            barcode_side_sequencing_primer="ACATACCGCA",
            common_side_cutsite_remnant="ACT",
            barcode_side_cutsite_remnant="CAT",
            barcodes=self.barcodes,
            minimum_length=1,
            error_rate=0,
            output_file_name_template="trimmed_{run}_{sample_name}{orientation}{extension}",
            output_directory=self.tempdir.name,
            anchored_adapters=False,
        )
        forward_result = dedent(
            """\
                                @EU861894-140/1
                                CGGCCTGCCCGGGGATCTCAAACNCTGGTAAGCTTCTCCGGTTAGTGACGAATC
                                +
                                HAH#III#I:IHJIJG#JIJJI?3IIJ0JJ#G3JGHG#I90?HIJG9JEIIBD#
                                @EU861894-138/1
                                CCACATGTGGTCCCCCGCTTCGGGGCAGGTTGCCCACGTGTTACGCGACCGTTCGCCATTAACCAC
                                +
                                HG?BAJJG0BII#GI8;FJIBFBHGJI>+EC=BECBDCHDEAAD#=E6DDFF=9CD#A#8H@@>#D
                                """
        ).strip()

        reverse_result = dedent(
            """\
                                @EU861894-140/2
                                GAATTGACAGGGGCACG
                                +
                                F1FFEFFA#AGGJB!EH
                                @EU861894-138/2
                                CGGGGGTGGTTAGGCAACCCCCCCCGAAGCGGGGGACAACAGCCTTAAACGGTTCCTAATACCGCATGGTGA
                                +
                                FB2@FHB2HFJGFFHJ?8=##JDGHDEIBH?H#HI)EFFEF#C#B#HE?#D?#;#DDCA#:DD>BCB###D'
                                """
        ).strip()

        result_data, aux_data = trim_op.perform(self.paired_fastq)
        self.assertIsInstance(result_data, SequencingData)
        fastq_result = list(result_data)
        self.assertEquals(len(fastq_result), 1)
        self.assertIsInstance(fastq_result[0], PairedEndFastq)
        files = fastq_result[0].files
        # Check output file contents
        self.assertFileContentEquals(files[0], forward_result)
        self.assertFileContentEquals(files[1], reverse_result)

    def test_trim_single(self):
        result = dedent(
            """
                        @1-1/1
                        GGGGGGGGGGGGGGGGGGGGGG
                        +
                        FFFFFFFFFFFFFFFFFFFFFF
                        """
        ).strip()
        trim_op = SingleEndTrimmer(
            common_side_sequencing_primer="TruSeq",
            common_side_cutsite_remnant="TTA",
            barcode_side_cutsite_remnant="CTGCA",
            barcodes=self.barcodes,
            minimum_length=1,
            error_rate=0,
            output_file_name_template="trimmed_{run}_{sample_name}{orientation}_{extension}",
            output_directory=self.tempdir.name,
        )
        result_data, aux_data = trim_op.perform(self.single_end_fastq_with_spacer)
        self.assertIsInstance(result_data, SequencingData)
        fastq_result = list(result_data)
        self.assertEquals(len(fastq_result), 1)
        self.assertIsInstance(fastq_result[0], SingleEndFastq)
        files = fastq_result[0].files
        self.assertFileContentEquals(files[0], result)

    def test_trim_single_end_with_spacer_raises(self):
        with self.assertRaisesRegex(
            ValueError, "Trimming spacers is not supported for single-end data."
        ):
            SingleEndTrimmer(
                common_side_sequencing_primer="foo",
                common_side_cutsite_remnant="foo",
                barcode_side_cutsite_remnant="foo",
                barcodes="foo",
                minimum_length=1,
                error_rate=0,
                output_file_name_template="foo",
                output_directory="foo",
                spacer="ACGT",
            )

    def test_untrimmed_first_cutadapt_run_minimum_length(self):
        # Issue 17
        no_trimming = PairedEndTrimmer(
            common_side_sequencing_primer="TruSeq",
            barcode_side_sequencing_primer="TruSeq",
            common_side_cutsite_remnant="CCG",  # Wrong remnant: no trimming
            barcode_side_cutsite_remnant="CTGCA",
            barcodes=self.barcodes,
            minimum_length=72,
            error_rate=0,
            output_file_name_template="trimmed_{run}_{sample_name}_{orientation}{extension}",
            output_directory=self.tempdir.name,
            spacer="ACGT",
        )
        result_data, aux_data = no_trimming.perform(self.paired_end_fastq_with_spacer)
        result_forward = dedent(
            """\
                                @1-4/1
                                CCGCTTTGCAGGGGGGGGGGGGGGGGGGGGGGGTTAACGAGATCGGAAGAGCACACGTCTGAACTCCAGTCAC
                                +
                                FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF
                                @1-5/1
                                CCGCTTTGCAGGGGGGGGGGGGGGGGGGGGGGGTTAACGTAGATCGGAAGAGCACACGTCTGAACTCCAGTCAC
                                +
                                FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF
                                """
        ).strip()
        result_reverse = dedent(
            """\
                                @1-4/2
                                CGTTAAGGGGGGGGGGGGGGGGGGGGGGCTGCAAAGCGGAGATCGGAAGAGCGTCGTGTAGGGAAAGAGTGT
                                +
                                FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF
                                @1-5/2
                                ACGTTAAGGGGGGGGGGGGGGGGGGGGGGCTGCAAAGCGGAGATCGGAAGAGCGTCGTGTAGGGAAAGAGTGT
                                +
                                FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF
                                """
        ).strip()
        fastq_result = list(aux_data)
        files = fastq_result[0].files
        self.assertFileContentEquals(files[0], result_forward)
        self.assertFileContentEquals(files[1], result_reverse)


class TestRemovePatternFilter(CustomOperationTestCase):
    def setUp(self):
        self.forward_out = dedent(
            """
                                @EU861894-138/1
                                AGAGCGCATCCACATGTGGTCCCCCGCTTCGGGGCAGGTTGCCCACGTGTTACGCGACCGTTCGCCATTAACCAC
                                +
                                @CCF:#@DHHG?BAJJG0BII#GI8;FJIBFBHGJI>+EC=BECBDCHDEAAD#=E6DDFF=9CD#A#8H@@>#D
                                """
        ).strip()
        self.reverse_out = dedent(
            """
                                @EU861894-138/2
                                CTTCGGGGGTGGTTAGGCAACCCCCCCCGAAGCGGGGGACAACAGCCTTAAACGGTTCCTAATACCGCATGGTGA
                                +
                                BB@FB2@FHB2HFJGFFHJ?8=##JDGHDEIBH?H#HI)EFFEF#C#B#HE?#D?#;#DDCA#:DD>BCB###D'
                                """
        ).strip()
        super().setUp()

    def test_filter_length_paired(self):
        filter_operation = RemovePatternFilter(
            pattern="AAGCTTCT",
            output_directory=self.tempdir.name,
            output_file_name_template="{run}_{orientation}{extension}",
        )
        output_seq_data, _ = filter_operation.perform(self.paired_fastq)
        (fastq,) = output_seq_data
        forward, reverse = fastq.files

        # Check output file contents
        self.assertFileContentEquals(forward, self.forward_out)
        self.assertFileContentEquals(reverse, self.reverse_out)

        # Check output directory
        self.assertEqual(forward.parent, reverse.parent)
        self.assertEqual(self.tempdir.name, str(forward.parent))

        # Check output name
        run = self.single_end_fastq.run
        extension = self.single_end_fastq.extension
        self.assertEqual(forward.name, f"{run}_1{extension}")
        self.assertEqual(reverse.name, f"{run}_2{extension}")

    def test_filter_length_single(self):
        filter_operation = RemovePatternFilter(
            pattern="AAGCTTCT",
            output_directory=self.tempdir.name,
            output_file_name_template="{run}{extension}",
        )
        output_seq_data, _ = filter_operation.perform(self.single_end_fastq)
        (fastq,) = output_seq_data
        (forward,) = fastq.files

        # Check file contents
        self.assertFileContentEquals(forward, self.forward_out)

        # Check output directory
        self.assertEqual(str(forward.parent), self.tempdir.name)

        # Check output name
        run = self.single_end_fastq.run
        extension = self.single_end_fastq.extension
        self.assertEqual(str(forward.name), f"{run}{extension}")

    def test_filter_partial_pattern(self):
        # https://gitlab.com/dschaumont/GBprocesS/-/issues/19
        res_forward = dedent(
            """
            @EU861894-140/1
            CCGATCTCTCGGCCTGCCCGGGGATCTCAAACNCTGGTAAGCTTCTCCGGTTAGTGACGAATCACTGTACCTGCTCCACCGCTTGTGCGGGCCCTCGTCA
            +
            ??CFFF?;HHAH#III#I:IHJIJG#JIJJI?3IIJ0JJ#G3JGHG#I90?HIJG9JEIIBD#C#G@#C=)I@#BHBBCDCD;ACDCB;??CD>#D#:DA
            @EU861894-138/1
            AGAGCGCATCCACATGTGGTCCCCCGCTTCGGGGCAGGTTGCCCACGTGTTACGCGACCGTTCGCCATTAACCAC
            +
            @CCF:#@DHHG?BAJJG0BII#GI8;FJIBFBHGJI>+EC=BECBDCHDEAAD#=E6DDFF=9CD#A#8H@@>#D
            """
        ).strip()
        res_reverse = dedent(
            """
            @EU861894-140/2
            AGTGAATTGACAGGGGCACGCATAAGCGGTGCGGTATGTGCATTAATTCGTCACTAACTGAAGAACCTCACCAGGCTTTGAAACCCACGGAGAGCGGGAG
            +
            @1@F1FFEFFA#AGGJB!EHDI434:J?GJI##B#)BJIICJJGEBFIBJ>GGDJIGI#)II<H6=ID#E?CD4##CDEFB#C#CA#-<#?#FCE#!DC'
            @EU861894-138/2
            CTTCGGGGGTGGTTAGGCAACCCCCCCCGAAGCGGGGGACAACAGCCTTAAACGGTTCCTAATACCGCATGGTGA
            +
            BB@FB2@FHB2HFJGFFHJ?8=##JDGHDEIBH?H#HI)EFFEF#C#B#HE?#D?#;#DDCA#:DD>BCB###D'
            """
        ).strip()
        filter_operation = RemovePatternFilter(
            pattern="AAGCTTCTG",
            output_directory=self.tempdir.name,
            output_file_name_template="{run}_{orientation}{extension}",
        )
        output_seq_data, _ = filter_operation.perform(self.paired_fastq)
        (fastq,) = output_seq_data
        forward, reverse = fastq.files

        # Check output file contents
        self.assertFileContentEquals(forward, res_forward)
        self.assertFileContentEquals(reverse, res_reverse)

        # Check output directory
        self.assertEqual(forward.parent, reverse.parent)
        self.assertEqual(self.tempdir.name, str(forward.parent))

        # Check output name
        run = self.single_end_fastq.run
        extension = self.single_end_fastq.extension
        self.assertEqual(forward.name, f"{run}_1{extension}")
        self.assertEqual(reverse.name, f"{run}_2{extension}")
