import io
import unittest
from configparser import ConfigParser, DuplicateSectionError
from configparser import Error as ConfigError
from unittest.mock import NonCallableMock, patch, PropertyMock

from gbprocess import __version__
from gbprocess.__main__ import (
    SerialPipeline,
    main,
    parse_general_section,
    parse_other_sections,
    read_config,
)
from gbprocess.data import PairedEndFastq, SequencingData
from gbprocess.operations.filtering import MaxNFilter
from gbprocess.operations.operation import _ALL_OPERATIONS


class TestCommandLine(unittest.TestCase):
    @patch("argparse.ArgumentParser.print_usage")
    def test_main_sys_args(self, print_usage):
        """
        Fail if passed args only contain program name.
        Check if usage is printed.
        """
        with self.assertRaises(SystemExit) as cm:
            main(args=["gbprocess"])
        self.assertNotEqual(cm.exception.code, 0)
        print_usage.assert_called()

    @patch("argparse.ArgumentParser.print_usage")
    def test_main_without_args(self, print_usage):
        """
        Fail if passed args are empty.
        Check if usage is printed.
        """
        with self.assertRaises(SystemExit) as cm:
            main([])
        self.assertNotEqual(cm.exception.code, 0)
        print_usage.assert_called()

    @patch("argparse.ArgumentParser.print_help")
    def test_main_help(self, print_help):
        """
        Test if help is printed if --help is passed.
        """
        with self.assertRaises(SystemExit) as cm:
            main(args=["--help"])
        self.assertEqual(cm.exception.code, 0)
        print_help.assert_called()

    def test_main_no_config(self):
        """
        Fail if trying to parse an config, no file was specified.
        Do not test if usage was printed, argparse should handle this
        """
        with self.assertRaises(SystemExit) as cm:
            main(args=["--config"])
        self.assertNotEqual(cm.exception.code, 0)

    def test_config_path_does_not_exist(self):
        """
        Fail if config file does not exist.
        """
        error_message = "The config file does nog exist or is not a file."
        with self.assertRaisesRegex(FileNotFoundError, error_message):
            main(args=["--config", "/tmp/foo"])

    @patch("sys.stdout", new_callable=io.StringIO)
    def test_main_list_operations(self, mock_stdout):
        """
        Check if operations are properly listed when using --operations.
        """
        main(args=["--operations"])
        self.assertIn("\n".join(_ALL_OPERATIONS), mock_stdout.getvalue())

    @patch("sys.stderr", new_callable=io.StringIO)
    def test_main_both_operations_and_config_fails(self, mock_stderr):
        """
        Fail when using both --operation and --config
        """
        with self.assertRaises(SystemExit) as cm:
            main(args=["--operations", "--config", "/foo/bar"])
        self.assertNotEqual(cm.exception.code, 0)
        self.assertIn(
            ("gbprocess: error: argument --config/-c:" " not allowed with argument --operations"),
            mock_stderr.getvalue(),
        )

    @patch("sys.stderr", new_callable=io.StringIO)
    def test_main_both_operations_and_version_fails(self, mock_stderr):
        """
        Fail when using both --operations and --version
        """
        with self.assertRaises(SystemExit) as cm:
            main(args=["--operations", "--version"])
        self.assertNotEqual(cm.exception.code, 0)
        self.assertIn(
            ("gbprocess: error: argument --version:" " not allowed with argument --operations"),
            mock_stderr.getvalue(),
        )

    @patch("sys.stderr", new_callable=io.StringIO)
    def test_main_both_version_and_config_fails(self, mock_stderr):
        """
        Fail when using both --version and --config
        """
        with self.assertRaises(SystemExit) as cm:
            main(args=["--operations", "--config", "/foo/bar"])
        self.assertNotEqual(cm.exception.code, 0)
        self.assertIn(
            ("gbprocess: error: argument --config/-c:" " not allowed with argument --operations"),
            mock_stderr.getvalue(),
        )

    @patch("sys.stdout", new_callable=io.StringIO)
    def test_version(self, mock_stdout):
        """
        Check if version if printed when using --version
        """
        with self.assertRaises(SystemExit) as cm:
            main(args=["--version"])
        self.assertEqual(cm.exception.code, 0)
        self.assertIn(__version__ + "\n", mock_stdout.getvalue())


class TestReadConfig(unittest.TestCase):
    def test_not_a_valid_ini_file(self):
        """
        Fail if an invalid ini file is used.
        """
        error_message = "File contains no section headers"
        config = io.StringIO("Foobar\n")
        with self.assertRaisesRegex(ConfigError, error_message):
            read_config(config)

    def test_empty_ini_file(self):
        """
        Fail when the ini file is empty.
        """
        config = io.StringIO("\n")
        error_message = (
            "Please define the 'General' section " "at the top of your configuration file"
        )
        with self.assertRaisesRegex(ValueError, error_message):
            read_config(config)

    def test_config_no_general_section(self):
        """
        Fail if the config file does not contain a general section
        """
        config = io.StringIO("[Dummy Operation]\n")
        error_message = (
            "Please define the 'General' section " "at the top of your configuration file"
        )
        with self.assertRaisesRegex(ValueError, error_message):
            read_config(config)

    def test_general_section_not_first(self):
        """
        Fail if the general section does not come first in the config file.
        """
        error_message = (
            "Please define the 'General' section " "at the top of your configuration file"
        )
        config = io.StringIO(
            """
                             [Dummy Operation]
                             output_directory = ./01_max_n_filter
                             output_file_name_template = {run}{extension}

                             [General]
                             cores = 1
                             input_directory = /foo/bar
                             sequencing_type = pe
                             input_file_name_template = foobar\n
                             """
        )
        with self.assertRaisesRegex(ValueError, error_message):
            read_config(config)

    @patch.object(SerialPipeline, "add_operation", NonCallableMock)
    @patch("gbprocess.__main__.parse_general_section")
    def test_no_operations(self, mocked_general_section):
        mocked_general_section.return_value = (
            SequencingData([]),
            SerialPipeline(),
            PairedEndFastq,
        )
        config = io.StringIO(
            """
                             [General]
                             cores = 1
                             input_directory = /foo/bar
                             sequencing_type = pe
                             input_file_name_template = foobar\n
                             """
        )
        read_config(config)

    def test_duplicate_operations_raises(self):
        config = io.StringIO(
            """
                [General]
                cores = 1
                input_directory = foobar
                sequencing_type = pe
                input_file_name_template = foobar

                [MaxNFilter]
                max_n = 0

                [MaxNFilter]
                max_n = 0
                """
        )
        with self.assertRaises(DuplicateSectionError):
            read_config(config)


class TestParseGeneralSection(unittest.TestCase):
    def test_wrong_sequencing_type(self):
        error_message = "The sequencing type must be a value from pe,se"
        config_parser = ConfigParser()
        config = io.StringIO(
            """
                             [General]
                             cores = 1
                             input_directory = foobar
                             sequencing_type = wrong_type
                             input_file_name_template = foobar
                             """
        )
        config_parser.read_file(config)
        with self.assertRaisesRegex(ValueError, error_message):
            parse_general_section(config_parser["General"])

    @patch("gbprocess.__main__.sequencingdata_from_dir")
    def test_config_cpu_count_not_int(self, mocked_seq_data):
        mocked_seq_data.return_value = (SequencingData([]), PairedEndFastq)
        error_message = "Could not interprete number of cpu cores as an integer."
        config_parser = ConfigParser()
        config = io.StringIO(
            """
                             [General]
                             cores = 'a'
                             input_directory = foobar
                             sequencing_type = pe
                             input_file_name_template = foobar
                             """
        )
        config_parser.read_file(config)
        with self.assertRaisesRegex(ValueError, error_message):
            parse_general_section(config_parser["General"])

    @patch("gbprocess.__main__.sequencingdata_from_dir")
    @patch("gbprocess.__main__.MultiProcessPipeline")
    def test_create_multiprocessing_pipeline(self, mocked_pipeline, mocked_seq_data):
        mocked_seq_data.return_value = (SequencingData([]), PairedEndFastq)
        config_parser = ConfigParser()
        config = io.StringIO(
            """
                             [General]
                             cores = 3
                             input_directory = foobar
                             sequencing_type = pe
                             input_file_name_template = foobar
                             """
        )
        config_parser.read_file(config)
        seq, pipeline, fastq_type = parse_general_section(config_parser["General"])
        mocked_pipeline.assert_called_once_with(cpu=3, temp_dir="/tmp")
        self.assertIs(mocked_pipeline.return_value, pipeline)
        self.assertIs(mocked_seq_data.return_value[0], seq)

    @patch("gbprocess.__main__.sequencingdata_from_dir")
    @patch("gbprocess.__main__.SerialPipeline")
    def test_create_serial_pipeline(self, mocked_pipeline, mocked_seq_data):
        mocked_seq_data.return_value = (SequencingData([]), PairedEndFastq)
        config_parser = ConfigParser()
        config = io.StringIO(
            """
                             [General]
                             cores = 1
                             input_directory = foobar
                             sequencing_type = pe
                             input_file_name_template = foobar
                             """
        )
        config_parser.read_file(config)
        seq, pipeline, fastq_type = parse_general_section(config_parser["General"])
        mocked_pipeline.assert_called_once_with(temp_dir="/tmp")
        self.assertIs(mocked_pipeline.return_value, pipeline)
        self.assertIs(mocked_seq_data.return_value[0], seq)

    @patch("gbprocess.__main__.sequencingdata_from_dir")
    @patch("gbprocess.__main__.SerialPipeline")
    def test_create_pipeline_temp_dir(self, mocked_pipeline, mocked_seq_data):
        """
        Issue 3
        """
        mocked_seq_data.return_value = (SequencingData([]), PairedEndFastq)
        config_parser = ConfigParser()
        config = io.StringIO(
            """
                             [General]
                             cores = 1
                             input_directory = foobar
                             sequencing_type = pe
                             input_file_name_template = foobar
                             temp_dir = /test_this
                             """
        )
        config_parser.read_file(config)
        seq, pipeline, fastq_type = parse_general_section(config_parser["General"])
        mocked_pipeline.assert_called_once_with(temp_dir="/test_this")
        self.assertIs(mocked_pipeline.return_value, pipeline)
        self.assertIs(mocked_seq_data.return_value[0], seq)


class TestParseOperationSections(unittest.TestCase):
    def setUp(self):
        class NonExecutablePipeline(SerialPipeline):
            def __init__(self):
                self._operations = []

            def execute(self):
                raise NotImplementedError

        self.pipeline = NonExecutablePipeline()

    @patch("gbprocess.operations.operation.Operation.output_directory", new_callable=PropertyMock)
    def test_duplicate_operations(self, mocked_operation):
        config = io.StringIO(
            """
            [General]
            cores = 1
            input_directory = foobar
            sequencing_type = pe
            input_file_name_template = {run}{extension}

            [MaxNFilter]
            max_n = 0
            output_directory = ./01_max_n_filter
            output_file_name_template = {run}{extension}

            [MaxNFilter.2]
            max_n = 0
            output_directory = ./02_max_n_filter
            output_file_name_template = {run}{extension}
            """
        )
        config_parser = ConfigParser()
        config_parser.read_file(config)
        returned_pipeline = parse_other_sections(
            [
                ("MaxNFilter", config_parser["MaxNFilter"]),
                ("MaxNFilter.2", config_parser["MaxNFilter.2"]),
            ],
            self.pipeline,
            PairedEndFastq,
        )
        self.assertIs(returned_pipeline, self.pipeline)
        operations = self.pipeline._operations
        self.assertEquals(len(operations), 2)
        self.assertIsInstance(operations[0], MaxNFilter)
