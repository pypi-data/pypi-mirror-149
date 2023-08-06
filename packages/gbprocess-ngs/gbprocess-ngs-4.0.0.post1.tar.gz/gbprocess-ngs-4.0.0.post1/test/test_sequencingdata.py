import bz2
import gzip
import shutil
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory
from textwrap import dedent
from unittest.mock import patch
from utils import CustomTestCase
from gbprocess.data import (
    SequencingData,
    PairedEndFastq,
    SingleEndFastq,
    _FastqFileNameTemplate,
)
from data import fastq_forward, fastq_reverse


class TestPairedEndFastq(CustomTestCase):
    def setUp(self):
        self.tempdir = TemporaryDirectory()
        with open(
            self.tempdir.name + "/17146FL-13-01-01_S97_L002_R1_001.fastq", "w+"
        ) as temp_file_forward, open(
            self.tempdir.name + "/17146FL-13-01-01_S97_L002_R2_001.fastq", "w+"
        ) as temp_file_reverse:
            temp_file_forward.write(fastq_forward())
            temp_file_reverse.write(fastq_reverse())
            temp_file_forward.flush()
            temp_file_reverse.flush()
            self.forward = self.tempdir.name + "/17146FL-13-01-01_S97_L002_R1_001.fastq"
            self.reverse = self.tempdir.name + "/17146FL-13-01-01_S97_L002_R2_001.fastq"

        self.forward_gz = self.forward + ".gz"
        self.reverse_gz = self.reverse + ".gz"
        with open(self.forward, "rb") as f_in:
            with gzip.open(self.forward_gz, "w") as f_out:
                shutil.copyfileobj(f_in, f_out)

        with open(self.reverse, "rb") as f_in:
            with gzip.open(self.reverse_gz, "w") as f_out:
                shutil.copyfileobj(f_in, f_out)

        self.forward_bzip2 = self.forward + ".bzip2"
        self.reverse_bzip2 = self.reverse + ".bzip2"
        with open(self.forward, "rb") as f_in:
            with bz2.open(self.forward_bzip2, "w") as f_out:
                shutil.copyfileobj(f_in, f_out)

        with open(self.reverse, "rb") as f_in:
            with bz2.open(self.reverse_bzip2, "w") as f_out:
                shutil.copyfileobj(f_in, f_out)

    def assertFileContentEquals(self, file_to_check, contents):
        with file_to_check.open("r") as fh:
            file_contents = fh.read().strip()
            self.assertMultiLineEqual(file_contents, contents)

    def tearDown(self):
        self.tempdir.cleanup()

    def test_create_uncompressed(self):
        fastq = PairedEndFastq(self.forward, self.reverse, exists_ok=True)
        self.assertListEqual(fastq.files, [Path(self.forward), Path(self.reverse)])
        self.assertEqual(fastq.run, None)
        self.assertEqual(fastq.extension, None)
        self.assertEqual(fastq.sample_name, None)
        self.assertEqual(fastq.orientation, None)
        fastq = PairedEndFastq(
            self.forward,
            self.reverse,
            run="17146FL-13-01-01_S97",
            sample_name="",
            orientation=[1, 2],
            extension=".fastq",
            exists_ok=True,
        )
        self.assertEqual(fastq.run, "17146FL-13-01-01_S97")
        self.assertEqual(fastq.extension, ".fastq")
        self.assertEqual(fastq.sample_name, "")
        self.assertTupleEqual(fastq.orientation, (1, 2))

    def test_create_compressed(self):
        fastq = PairedEndFastq(self.forward_gz, self.reverse_gz, exists_ok=True)
        self.assertListEqual(fastq.files, [Path(self.forward_gz), Path(self.reverse_gz)])
        self.assertEqual(fastq.run, None)
        self.assertEqual(fastq.extension, None)
        self.assertEqual(fastq.sample_name, None)
        self.assertEqual(fastq.orientation, None)

        fastq = PairedEndFastq(self.forward_bzip2, self.reverse_bzip2, exists_ok=True)
        self.assertListEqual(fastq.files, [Path(self.forward_bzip2), Path(self.reverse_bzip2)])
        self.assertEqual(fastq.run, None)
        self.assertEqual(fastq.extension, None)
        self.assertEqual(fastq.sample_name, None)
        self.assertEqual(fastq.orientation, None)

    @patch("gbprocess.data.Path.is_file")
    @patch("gbprocess.data.Path.touch")
    def test_create_exists_not_ok_raises(self, mocked_touch, mocked_is_file):
        mocked_is_file.return_value = True
        mocked_touch.side_effect = FileExistsError
        with self.assertRaises(FileExistsError):
            PairedEndFastq("1.fastq", "2.fastq", exists_ok=False)

    @patch("gbprocess.data.Path.is_file")
    @patch("gbprocess.data.Path.samefile")
    def test_same_file_raises(self, mocked_samefile, mocked_is_file):
        mocked_is_file.return_value = True
        mocked_samefile.return_value = True
        error_message = "The forward and reverse path point to the same file."
        with self.assertRaisesRegex(ValueError, error_message):
            PairedEndFastq("1.fastq", "1.fastq", exists_ok=False)
        error_message_if_exists = "Some of the specified files are the same!"
        with self.assertRaisesRegex(ValueError, error_message_if_exists):
            PairedEndFastq("1.fastq", "1.fastq", exists_ok=True)

    @patch("gbprocess.data.Path.is_file")
    def test_pop_one_file_raises(self, patched_is_file):
        patched_is_file.return_value = True
        iterator = iter(["a_1.fastq"])
        error_message = "An odd number of fastq files was found!"
        with self.assertRaisesRegex(ValueError, error_message):
            PairedEndFastq.pop(iterator, "{run:1}_{orientation:1}{extension}")

    @patch("gbprocess.data.Path.is_file")
    @patch("gbprocess.data.Path.samefile")
    def test_pop(self, mocked_samefile, mocked_is_file):
        mocked_samefile.return_value = False
        mocked_is_file.return_value = True
        iterator = iter(["a_1.fastq", "a_2.fastq"])
        PairedEndFastq.pop(iterator, "{run:1}_{orientation:1}{extension}", exists_ok=True)
        with self.assertRaises(StopIteration):
            PairedEndFastq.pop(iterator, "{run:25}_R{orientation:1}_001{extension}")

    def test_split_without_extension(self):
        self.read1_f = dedent(
            """\
                                  @EU861894-140/1
                                  CCGATCTCTCGGCCTGCCCGGGGATCTCAAACNCTGGTAAGCTTCTCCGGTTAGTGACGAATCACTGTACCTGCTCCACCGCTTGTGCGGGCCCTCGTCA
                                  +
                                  ??CFFF?;HHAH#III#I:IHJIJG#JIJJI?3IIJ0JJ#G3JGHG#I90?HIJG9JEIIBD#C#G@#C=)I@#BHBBCDCD;ACDCB;??CD>#D#:DA

                                  """
        ).strip()
        self.read2_f = dedent(
            """\
                                  @EU861894-138/1
                                  AGAGCGCATCCACATGTGGTCCCCCGCTTCGGGGCAGGTTGCCCACGTGTTACGCGACCGTTCGCCATTAACCAC
                                  +
                                  @CCF:#@DHHG?BAJJG0BII#GI8;FJIBFBHGJI>+EC=BECBDCHDEAAD#=E6DDFF=9CD#A#8H@@>#D

                                  """
        ).strip()
        self.read1_r = dedent(
            """\
                                  @EU861894-140/2
                                  AGTGAATTGACAGGGGCACGCATAAGCGGTGCGGTATGTGCATTAATTCGTCACTAACTGAAGAACCTCACCAGGCTTTGAAACCCACGGAGAGCGGGAG
                                  +
                                  @1@F1FFEFFA#AGGJB!EHDI434:J?GJI##B#)BJIICJJGEBFIBJ>GGDJIGI#)II<H6=ID#E?CD4##CDEFB#C#CA#-<#?#FCE#!DC'

                                  """
        ).strip()
        self.read2_r = dedent(
            """\
                                  @EU861894-138/2
                                  CTTCGGGGGTGGTTAGGCAACCCCCCCCGAAGCGGGGGACAACAGCCTTAAACGGTTCCTAATACCGCATGGTGA
                                  +
                                  BB@FB2@FHB2HFJGFFHJ?8=##JDGHDEIBH?H#HI)EFFEF#C#B#HE?#D?#;#DDCA#:DD>BCB###D'

                                  """
        ).strip()

        fastq = PairedEndFastq(self.forward, self.reverse, exists_ok=True)
        fastq._SPLIT_BUFFER = 256
        fastq.split(2, self.tempdir.name)
        forward_1, reverse_1 = Path(
            self.tempdir.name + "/17146FL-13-01-01_S97_L002_R1_001.fastq_0"
        ), Path(self.tempdir.name + "/17146FL-13-01-01_S97_L002_R2_001.fastq_0")
        forward_2, reverse_2 = Path(
            self.tempdir.name + "/17146FL-13-01-01_S97_L002_R1_001.fastq_1"
        ), Path(self.tempdir.name + "/17146FL-13-01-01_S97_L002_R2_001.fastq_1")
        files = list(Path(self.tempdir.name).glob("*.fastq_*"))
        self.assertIn(forward_1, files)
        self.assertIn(reverse_1, files)
        self.assertIn(forward_2, files)
        self.assertIn(reverse_2, files)
        self.assertFileContentEquals(forward_1, self.read1_f)
        self.assertFileContentEquals(forward_2, self.read2_f)
        self.assertFileContentEquals(reverse_1, self.read1_r)
        self.assertFileContentEquals(reverse_2, self.read2_r)

    def test_split_with_extension(self):
        self.read1_f = dedent(
            """\
                                  @EU861894-140/1
                                  CCGATCTCTCGGCCTGCCCGGGGATCTCAAACNCTGGTAAGCTTCTCCGGTTAGTGACGAATCACTGTACCTGCTCCACCGCTTGTGCGGGCCCTCGTCA
                                  +
                                  ??CFFF?;HHAH#III#I:IHJIJG#JIJJI?3IIJ0JJ#G3JGHG#I90?HIJG9JEIIBD#C#G@#C=)I@#BHBBCDCD;ACDCB;??CD>#D#:DA

                                  """
        ).strip()
        self.read2_f = dedent(
            """\
                                  @EU861894-138/1
                                  AGAGCGCATCCACATGTGGTCCCCCGCTTCGGGGCAGGTTGCCCACGTGTTACGCGACCGTTCGCCATTAACCAC
                                  +
                                  @CCF:#@DHHG?BAJJG0BII#GI8;FJIBFBHGJI>+EC=BECBDCHDEAAD#=E6DDFF=9CD#A#8H@@>#D

                                  """
        ).strip()
        self.read1_r = dedent(
            """\
                                  @EU861894-140/2
                                  AGTGAATTGACAGGGGCACGCATAAGCGGTGCGGTATGTGCATTAATTCGTCACTAACTGAAGAACCTCACCAGGCTTTGAAACCCACGGAGAGCGGGAG
                                  +
                                  @1@F1FFEFFA#AGGJB!EHDI434:J?GJI##B#)BJIICJJGEBFIBJ>GGDJIGI#)II<H6=ID#E?CD4##CDEFB#C#CA#-<#?#FCE#!DC'

                                  """
        ).strip()
        self.read2_r = dedent(
            """\
                                  @EU861894-138/2
                                  CTTCGGGGGTGGTTAGGCAACCCCCCCCGAAGCGGGGGACAACAGCCTTAAACGGTTCCTAATACCGCATGGTGA
                                  +
                                  BB@FB2@FHB2HFJGFFHJ?8=##JDGHDEIBH?H#HI)EFFEF#C#B#HE?#D?#;#DDCA#:DD>BCB###D'

                                  """
        ).strip()

        fastq = PairedEndFastq(self.forward, self.reverse, exists_ok=True, extension=".fastq")
        fastq._SPLIT_BUFFER = 256
        fastq.split(2, self.tempdir.name)
        forward_1, reverse_1 = Path(
            self.tempdir.name + "/17146FL-13-01-01_S97_L002_R1_001_0.fastq"
        ), Path(self.tempdir.name + "/17146FL-13-01-01_S97_L002_R2_001_0.fastq")
        forward_2, reverse_2 = Path(
            self.tempdir.name + "/17146FL-13-01-01_S97_L002_R1_001_1.fastq"
        ), Path(self.tempdir.name + "/17146FL-13-01-01_S97_L002_R2_001_1.fastq")
        files = list(Path(self.tempdir.name).glob("*.fastq"))
        self.assertIn(forward_1, files)
        self.assertIn(reverse_1, files)
        self.assertIn(forward_2, files)
        self.assertIn(reverse_2, files)
        self.assertFileContentEquals(forward_1, self.read1_f)
        self.assertFileContentEquals(forward_2, self.read2_f)
        self.assertFileContentEquals(reverse_1, self.read1_r)
        self.assertFileContentEquals(reverse_2, self.read2_r)

    def test_join(self):
        self.read2_f = dedent(
            """\
                                  @EU861894-140/1
                                  CCGATCTCTCGGCCTGCCCGGGGATCTCAAACNCTGGTAAGCTTCTCCGGTTAGTGACGAATCACTGTACCTGCTCCACCGCTTGTGCGGGCCCTCGTCA
                                  +
                                  ??CFFF?;HHAH#III#I:IHJIJG#JIJJI?3IIJ0JJ#G3JGHG#I90?HIJG9JEIIBD#C#G@#C=)I@#BHBBCDCD;ACDCB;??CD>#D#:DA

                                  """
        ).strip()
        self.read1_f = dedent(
            """\
                                  @EU861894-138/1
                                  AGAGCGCATCCACATGTGGTCCCCCGCTTCGGGGCAGGTTGCCCACGTGTTACGCGACCGTTCGCCATTAACCAC
                                  +
                                  @CCF:#@DHHG?BAJJG0BII#GI8;FJIBFBHGJI>+EC=BECBDCHDEAAD#=E6DDFF=9CD#A#8H@@>#D

                                  """
        ).strip()
        self.read2_r = dedent(
            """\
                                  @EU861894-140/2
                                  AGTGAATTGACAGGGGCACGCATAAGCGGTGCGGTATGTGCATTAATTCGTCACTAACTGAAGAACCTCACCAGGCTTTGAAACCCACGGAGAGCGGGAG
                                  +
                                  @1@F1FFEFFA#AGGJB!EHDI434:J?GJI##B#)BJIICJJGEBFIBJ>GGDJIGI#)II<H6=ID#E?CD4##CDEFB#C#CA#-<#?#FCE#!DC'

                                  """
        ).strip()
        self.read1_r = dedent(
            """\
                                  @EU861894-138/2
                                  CTTCGGGGGTGGTTAGGCAACCCCCCCCGAAGCGGGGGACAACAGCCTTAAACGGTTCCTAATACCGCATGGTGA
                                  +
                                  BB@FB2@FHB2HFJGFFHJ?8=##JDGHDEIBH?H#HI)EFFEF#C#B#HE?#D?#;#DDCA#:DD>BCB###D'

                                  """
        ).strip()
        with open(
            self.tempdir.name + "/17146FL-13-01-01_S97_L002_R1_001_0.fastq", "w+"
        ) as temp_file_forward_0, open(
            self.tempdir.name + "/17146FL-13-01-01_S97_L002_R2_001_0.fastq", "w+"
        ) as temp_file_reverse_0, open(
            self.tempdir.name + "/17146FL-13-01-01_S97_L002_R1_001_1.fastq", "w+"
        ) as temp_file_forward_1, open(
            self.tempdir.name + "/17146FL-13-01-01_S97_L002_R2_001_1.fastq", "w+"
        ) as temp_file_reverse_1:

            temp_file_forward_0.write(self.read1_f)
            temp_file_forward_0.flush()
            temp_file_forward_1.write(self.read2_f)
            temp_file_forward_1.flush()
            temp_file_reverse_0.write(self.read1_r)
            temp_file_reverse_0.flush()
            temp_file_reverse_1.write(self.read2_r)
            temp_file_reverse_1.flush()

        p_fastq_0 = PairedEndFastq(
            temp_file_forward_0.name,
            temp_file_reverse_0.name,
            run="17146FL-13-01-01_S97",
            extension=".fastq",
            orientation=[1, 2],
            exists_ok=True,
        )
        p_fastq_1 = PairedEndFastq(
            temp_file_forward_1.name,
            temp_file_reverse_1.name,
            run="17146FL-13-01-01_S97",
            extension=".fastq",
            orientation=[1, 2],
            exists_ok=True,
        )

        result = p_fastq_1.join(p_fastq_0)
        foward_result, reverse_result = result.files
        self.assertFileContentEquals(foward_result, fastq_forward())
        self.assertFileContentEquals(reverse_result, fastq_reverse())

    def test_issue_11(self):
        foward_file = self.tempdir.name + "/P02_EUC_MS_1005.1.fq"
        reverse_file = self.tempdir.name + "/P02_EUC_MS_1005.2.fq"
        with open(foward_file, "w+") as temp_file_forward, open(
            reverse_file, "w+"
        ) as temp_file_reverse:
            temp_file_forward.write(fastq_forward())
            temp_file_reverse.write(fastq_reverse())
            temp_file_forward.flush()
            temp_file_reverse.flush()
        input_file_name_template = "{sample_name:15}.{orientation:1}{extension:3}"
        fastq = PairedEndFastq.pop(
            iter([foward_file, reverse_file]), input_file_name_template, exists_ok=True
        )
        fastq.split(2, self.tempdir.name)


class TestSingleEndFastq(CustomTestCase):
    def setUp(self):
        self.tempdir = TemporaryDirectory()
        with open(
            self.tempdir.name + "/17146FL-13-01-01_S97_L002_R1_001.fastq", "w+"
        ) as temp_file_forward:
            temp_file_forward.write(fastq_forward())
            temp_file_forward.flush()
            self.forward = self.tempdir.name + "/17146FL-13-01-01_S97_L002_R1_001.fastq"

    def tearDown(self):
        self.tempdir.cleanup()

    def test_create_uncompressed(self):
        SingleEndFastq(self.forward, exists_ok=True)

    def test_create_missing_file_raises(self):
        with self.assertRaises(ValueError):
            SingleEndFastq("/tmp/foo", exists_ok=True)

    def test_create_input_is_not_file(self):
        with self.assertRaises(ValueError):
            SingleEndFastq("/tmp/", exists_ok=True)

    def test_pop(self):
        iterator = iter([self.forward])
        SingleEndFastq.pop(iterator, "{run:25}_R{orientation:1}_001{extension}", exists_ok=True)

    def test_pop_raises(self):
        iterator = iter([self.forward])
        SingleEndFastq.pop(iterator, "{run:25}_R{orientation:1}_001{extension}", exists_ok=True)
        with self.assertRaises(StopIteration):
            SingleEndFastq.pop(iterator, "{run:25}_R{orientation:1}_001{extension}")

    def test_split(self):
        self.read1_f = dedent(
            """\
                                  @EU861894-140/1
                                  CCGATCTCTCGGCCTGCCCGGGGATCTCAAACNCTGGTAAGCTTCTCCGGTTAGTGACGAATCACTGTACCTGCTCCACCGCTTGTGCGGGCCCTCGTCA
                                  +
                                  ??CFFF?;HHAH#III#I:IHJIJG#JIJJI?3IIJ0JJ#G3JGHG#I90?HIJG9JEIIBD#C#G@#C=)I@#BHBBCDCD;ACDCB;??CD>#D#:DA

                                  """
        ).strip()
        self.read2_f = dedent(
            """\
                                  @EU861894-138/1
                                  AGAGCGCATCCACATGTGGTCCCCCGCTTCGGGGCAGGTTGCCCACGTGTTACGCGACCGTTCGCCATTAACCAC
                                  +
                                  @CCF:#@DHHG?BAJJG0BII#GI8;FJIBFBHGJI>+EC=BECBDCHDEAAD#=E6DDFF=9CD#A#8H@@>#D

                                  """
        ).strip()

        fastq = SingleEndFastq(self.forward, exists_ok=True)
        fastq._SPLIT_BUFFER = 256
        fastq.split(2, self.tempdir.name)
        files = list(Path(self.tempdir.name).glob("*.fastq_*"))
        forward_1, forward_2 = Path(
            self.tempdir.name + "/17146FL-13-01-01_S97_L002_R1_001.fastq_0"
        ), Path(self.tempdir.name + "/17146FL-13-01-01_S97_L002_R1_001.fastq_1")
        self.assertIn(forward_1, files)
        self.assertIn(forward_2, files)
        self.assertFileContentEquals(forward_1, self.read1_f)
        self.assertFileContentEquals(forward_2, self.read2_f)

    def test_join(self):
        self.read2_f = dedent(
            """\
                                  @EU861894-140/1
                                  CCGATCTCTCGGCCTGCCCGGGGATCTCAAACNCTGGTAAGCTTCTCCGGTTAGTGACGAATCACTGTACCTGCTCCACCGCTTGTGCGGGCCCTCGTCA
                                  +
                                  ??CFFF?;HHAH#III#I:IHJIJG#JIJJI?3IIJ0JJ#G3JGHG#I90?HIJG9JEIIBD#C#G@#C=)I@#BHBBCDCD;ACDCB;??CD>#D#:DA

                                  """
        ).strip()
        self.read1_f = dedent(
            """\
                                  @EU861894-138/1
                                  AGAGCGCATCCACATGTGGTCCCCCGCTTCGGGGCAGGTTGCCCACGTGTTACGCGACCGTTCGCCATTAACCAC
                                  +
                                  @CCF:#@DHHG?BAJJG0BII#GI8;FJIBFBHGJI>+EC=BECBDCHDEAAD#=E6DDFF=9CD#A#8H@@>#D

                                  """
        ).strip()

        with open(
            self.tempdir.name + "/17146FL-13-01-01_S97_L002_R1_001_0.fastq", "w+"
        ) as temp_file_forward_0, open(
            self.tempdir.name + "/17146FL-13-01-01_S97_L002_R1_001_1.fastq", "w+"
        ) as temp_file_forward_1:
            temp_file_forward_0.write(self.read1_f)
            temp_file_forward_0.flush()
            temp_file_forward_1.write(self.read2_f)
            temp_file_forward_1.flush()

        s_fastq_0 = SingleEndFastq(
            temp_file_forward_0.name,
            run="17146FL-13-01-01_S97",
            extension=".fastq",
            exists_ok=True,
        )
        s_fastq_1 = SingleEndFastq(
            temp_file_forward_1.name,
            run="17146FL-13-01-01_S97",
            extension=".fastq",
            exists_ok=True,
        )

        result = s_fastq_1.join(s_fastq_0)
        [foward_result] = result.files
        self.assertFileContentEquals(foward_result, fastq_forward())


class TestSequencingData(unittest.TestCase):
    def setUp(self):
        self.tempdir_paired = TemporaryDirectory()
        with open(
            self.tempdir_paired.name + "/17146FL-13-01-01_S97_L002_R1_001.fastq", "w+"
        ) as temp_file_forward, open(
            self.tempdir_paired.name + "/17146FL-13-01-01_S97_L002_R2_001.fastq", "w+"
        ) as temp_file_reverse:
            temp_file_forward.write(fastq_forward())
            temp_file_reverse.write(fastq_reverse())
            temp_file_forward.flush()
            temp_file_reverse.flush()
            self.p_fastq = PairedEndFastq(
                temp_file_forward.name,
                temp_file_reverse.name,
                run="17146FL-13-01-01_S97",
                extension=".fastq",
                orientation=[1, 2],
                exists_ok=True,
            )

        self.tempdir_single = TemporaryDirectory()
        with open(
            self.tempdir_single.name + "/17146FL-13-01-01_S97_L002_R1_001.fastq", "w+"
        ) as temp_file_forward:
            temp_file_forward.write(fastq_forward())
            temp_file_forward.flush()
            self.s_fastq = SingleEndFastq(
                temp_file_forward.name,
                run="17146FL-13-01-01_S97",
                extension=".fastq",
                exists_ok=True,
            )

    def tearDown(self):
        self.tempdir_paired.cleanup()
        self.tempdir_single.cleanup()

    def test_create_single_end_default(self):
        SequencingData([self.s_fastq])

    def test_create_single_end_from_directory(self):
        SequencingData.from_directory(
            SingleEndFastq, self.tempdir_single.name, "{run:25}_R1_001{extension}"
        )

    def test_create_paired_end_default(self):
        SequencingData([self.p_fastq])

    def test_create_paired_end_from_directory(self):
        SequencingData.from_directory(
            PairedEndFastq,
            self.tempdir_paired.name,
            "{run:25}_R{orientation:1}_001{extension}",
        )


class TestFileNameTemplate(unittest.TestCase):
    def test_no_template(self):
        error_message = "Expected a non-zero length file name template."
        with self.assertRaisesRegex(ValueError, error_message):
            _FastqFileNameTemplate("")

    def test_regex_creation(self):
        fastq_name_template = _FastqFileNameTemplate("{a:1}_R{b:2}_001{c}")
        self.assertEqual(
            fastq_name_template._regex_expression,
            "(?P<a>.{1})_R(?P<b>.{2})_001(?P<c>.*)",
        )

    def test_groups(self):
        fastq_name_template = _FastqFileNameTemplate("{a:1}_{b:2}_001{c}")
        self.assertListEqual(fastq_name_template._groups, ["a", "b", "c"])

    def test_parse_filename(self):
        fastq_name_template = _FastqFileNameTemplate("{run:25}_R{orientation:1}_001{extension}")
        result = fastq_name_template.parse("17146FL-13-01-01_S97_L002_R1_001.fastq")
        self.assertDictEqual(
            result,
            {
                "extension": ".fastq",
                "orientation": "1",
                "run": "17146FL-13-01-01_S97_L002",
            },
        )

    def test_parse_filename_special_char(self):
        for special_char in (
            "$",
            "^",
            ".",
            "|",
            "?",
            "!",
            "*",
            "]",
            "(",
            ")",
            "[",
            "]",
            "\\",
        ):
            template = "{run:25}_" + special_char + "{orientation:1}_001{extension}"
            fastq_name_template = _FastqFileNameTemplate(template)
            to_parse = "17146FL-13-01-01_S97_L002_" + special_char + "1_001.fastq"
            result = fastq_name_template.parse(to_parse)
            self.assertDictEqual(
                result,
                {
                    "extension": ".fastq",
                    "orientation": "1",
                    "run": "17146FL-13-01-01_S97_L002",
                },
            )

        template = "{run:25}_{{{orientation:1}_001{extension}"
        fastq_name_template = _FastqFileNameTemplate(template)
        to_parse = "17146FL-13-01-01_S97_L002_{1_001.fastq"
        result = fastq_name_template.parse(to_parse)
        self.assertDictEqual(
            result,
            {
                "extension": ".fastq",
                "orientation": "1",
                "run": "17146FL-13-01-01_S97_L002",
            },
        )

        template = "{run:25}_}}{orientation:1}_001{extension}"
        fastq_name_template = _FastqFileNameTemplate(template)
        to_parse = "17146FL-13-01-01_S97_L002_}1_001.fastq"
        result = fastq_name_template.parse(to_parse)
        self.assertDictEqual(
            result,
            {
                "extension": ".fastq",
                "orientation": "1",
                "run": "17146FL-13-01-01_S97_L002",
            },
        )

    def test_parse_empty_filename_raises(self):
        fastq_name_template = _FastqFileNameTemplate("{run:25}_R{orientation:1}_001{extension}")
        message = (
            "Could not parse the file name template "
            "'{run:25}_R{orientation:1}_001{extension}' "
            "with the given path ''"
        )
        with self.assertRaisesRegex(ValueError, message):
            fastq_name_template.parse("")

    def test_parse_longest_segment(self):
        fastq_name_template = _FastqFileNameTemplate(
            "{sample_name}_{run:24}_{orientation:1}{extension:9}"
        )
        result = fastq_name_template.parse("LV_1_17146FL-22-01-01_S1_L003_1.fastq.gz")
        self.assertDictEqual(
            result,
            {
                "extension": ".fastq.gz",
                "orientation": "1",
                "run": "17146FL-22-01-01_S1_L003",
                "sample_name": "LV_1",
            },
        )


if __name__ == "__main__":
    unittest.main()
