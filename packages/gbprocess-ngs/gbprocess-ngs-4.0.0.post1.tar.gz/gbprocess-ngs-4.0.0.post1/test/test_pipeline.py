import unittest
from gbprocess.pipeline import SerialPipeline
from tempfile import TemporaryDirectory
from gbprocess.operations.filtering import MaxNFilter, LengthFilter
from gbprocess.data import SequencingData, PairedEndFastq
from data import fastq_forward, fastq_reverse


class TestSerialPipeline(unittest.TestCase):
    def setUp(self):
        self.tempdir = TemporaryDirectory()
        self.pipeline = SerialPipeline(temp_dir=self.tempdir.name)

    def tearDown(self):
        self.tempdir.cleanup()

    def test_pass_none(self):
        with self.assertRaises(ValueError):
            self.pipeline.execute(None)

    def add_operation_pass_none(self):
        with self.assertRaises(ValueError):
            self.pipeline.add_operation(None)

    def test_run_without_operations(self):
        with TemporaryDirectory() as temp_dir:
            forward_fastq = str(temp_dir) + "/17146FL-13-01-01_S97_L002_R1_001.fastq"
            reverse_fastq = str(temp_dir) + "/17146FL-13-01-01_S97_L002_R2_001.fastq"
            with open(forward_fastq, "w+") as temp_file_forward, open(
                reverse_fastq, "w+"
            ) as temp_file_reverse:
                temp_file_forward.write(fastq_forward())
                temp_file_reverse.write(fastq_reverse())
            paired_fastq = PairedEndFastq(
                forward_fastq,
                reverse_fastq,
                run="17146FL-13-01-01_S97",
                extension=".fastq",
                orientation=[1, 2],
                exists_ok=True,
            )
            seq_data = SequencingData([paired_fastq])
            self.pipeline.execute(seq_data)

    def test_add_operation(self):
        operation = MaxNFilter(
            max_n=0,
            output_directory=self.tempdir.name,
            output_file_name_template="{run}_{orientation}{extension}",
        )
        self.pipeline.add_operation(operation)
        self.assertListEqual(self.pipeline._operations, [operation])

    def test_add_same_operation_twice(self):
        operation = MaxNFilter(
            max_n=0,
            output_directory=self.tempdir.name,
            output_file_name_template="{run}_{orientation}{extension}",
        )
        self.pipeline.add_operation(operation)
        self.assertListEqual(self.pipeline._operations, [operation])
        self.pipeline.add_operation(operation)
        self.assertListEqual(self.pipeline._operations, [operation, operation])

    def test_operation_order(self):
        operation1 = MaxNFilter(
            max_n=0,
            output_directory=self.tempdir.name,
            output_file_name_template="{run}_{orientation}{extension}",
        )

        operation2 = LengthFilter(
            minimum_length=100,
            output_directory=self.tempdir.name,
            output_file_name_template="{run}_{orientation}{extension}",
        )

        self.pipeline.add_operation(operation1)
        self.pipeline.add_operation(operation2)
        self.assertListEqual(self.pipeline._operations, [operation1, operation2])
