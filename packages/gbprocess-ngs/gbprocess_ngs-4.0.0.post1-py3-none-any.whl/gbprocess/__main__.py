import argparse
import logging
import sys
from collections import OrderedDict
from configparser import ConfigParser, DuplicateSectionError
from pathlib import Path
from typing import TextIO, Union

from gbprocess import __version__
from gbprocess.data import PairedEndFastq, SequencingData, SingleEndFastq
from gbprocess.operations.operation import _ALL_OPERATIONS, get_operation
from gbprocess.pipeline import MultiProcessPipeline, SerialPipeline


def main(args=None):
    # Get the location and process the INI file.
    parser = argparse.ArgumentParser(prog="gbprocess")
    parser.add_argument("--debug", help="Enable verbose logging.", action="store_true")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument(
        "--config",
        "-c",
        help="INI file containing the pipeline's config",
        metavar="CONFIG",
    )
    group.add_argument("--operations", help="List the possible operations", action="store_true")
    group.add_argument("--version", action="version", version=__version__)

    if args is None:
        args = sys.argv[1:]

    if len(args) < 1:
        parser.print_usage()
        parser.exit(1)

    parsed_args = parser.parse_args(args)
    if parsed_args.debug:
        level = logging.DEBUG
    else:
        level = logging.INFO
        # sys.tracebacklimit = 0 # Suppress traceback information on errors.

    logging.basicConfig(
        stream=sys.stdout,
        level=level,
        format="%(asctime)s %(name)s - %(levelname)s: %(message)s",
    )
    logging.info(f"This is version {__version__}")

    if parsed_args.operations:
        print("\n".join(_ALL_OPERATIONS.keys()))
    elif parsed_args.config:
        ini_file = Path(parsed_args.config)
        if not ini_file.is_file():
            raise FileNotFoundError("The config file does nog exist or is not a file.")
        logging.info("Parsing configuration file {}".format(ini_file))
        with ini_file.open("rt") as handler:
            read_config(handler)


def sequencingdata_from_dir(
    directory: Union[Path, str], sequencing_type: str, file_name_template: str
):
    string_to_type = {"pe": PairedEndFastq, "se": SingleEndFastq}
    try:
        sequencing_type_o = string_to_type[sequencing_type]
    except KeyError:
        raise ValueError(
            "The sequencing type must be a value from {}".format(",".join(string_to_type.keys()))
        )
    else:
        return (
            SequencingData.from_directory(sequencing_type_o, directory, file_name_template),
            sequencing_type_o,
        )


def read_config(ini_fh: TextIO):
    config_parser = ConfigParser(dict_type=OrderedDict, strict=True)
    try:
        config_parser.read_file(ini_fh)
    except DuplicateSectionError as e:
        logging.error(
            (
                "Please make sure that the sections headers are "
                "unique. The format of a header can be [operation] "
                "if the operation is only performed once, or "
                "[operation.<unique>], with <unique> some text that "
                "is not shared between the two or more section titles "
                "(for example: [MaxNFilter.2])."
            )
        )
        raise e
    logging.debug(
        f"Configuration: { {section: dict(config_parser[section]) for section in config_parser} }"
    )

    first = True
    other_args = []
    general_section_args = None
    for section, arguments in config_parser.items():
        if section == "DEFAULT":
            pass
        elif section.lower() == "general" and first:
            general_section_args = arguments
        else:
            other_args.append((section, arguments))
            first = False
    if not general_section_args:
        raise ValueError(
            "Please define the 'General' section at the top of your configuration file"
        )
    seqs, empty_pipeline, fastq_type = parse_general_section(general_section_args)
    pipeline = parse_other_sections(other_args, empty_pipeline, fastq_type)
    pipeline.execute(seqs)


def parse_general_section(arguments):
    logging.info(
        f"""General run information:\r
                            Input directory: {arguments.get("input_directory")}\r
                            Sequencing type: {arguments.get("sequencing_type")}\r
                            Input file template: {arguments.get("input_file_name_template")}
                            Cores/threads: {arguments.get('cores')}"""
    )

    seqs, fastq_type = sequencingdata_from_dir(
        arguments["input_directory"],
        arguments["sequencing_type"],
        arguments["input_file_name_template"],
    )
    try:
        cpu = int(arguments["cores"])
    except ValueError:
        raise ValueError("Could not interprete number of cpu cores as an integer.")
    else:
        if cpu == 1:
            pipeline = SerialPipeline(temp_dir=arguments.get("temp_dir", "/tmp"))
        else:
            pipeline = MultiProcessPipeline(cpu=cpu, temp_dir=arguments.get("temp_dir", "/tmp"))
    return seqs, pipeline, fastq_type


def parse_other_sections(sections, pipeline, fastq_type):
    for (section, arguments) in sections:
        operation_name, _, _ = section.partition(".")
        operation_builder = get_operation(operation_name).builder(fastq_type)
        try:
            operation = operation_builder(**dict(arguments))
        except TypeError as e:
            raise ValueError(
                (f"Could not configure operation {section}. " "Please check the configuration.")
            ) from e
        fastq_type = operation.introspect_outcome(fastq_type)
        pipeline.add_operation(operation)
    return pipeline


if __name__ == "__main__":
    main()
