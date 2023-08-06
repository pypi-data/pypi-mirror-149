"""
Operations to merge paired-end .fastq files.
"""
import logging
from abc import ABC
from pathlib import Path
from typing import Type, Union

from ..data import Fastq, PairedEndFastq, SequencingData, SingleEndFastq
from ..utils import CommandLineWrapper
from .operation import Operation, register

logger = logging.getLogger("Merging")


class Merger(Operation, ABC):
    def introspect_outcome(self, fastq_class: Type[Fastq]) -> Type[Fastq]:
        if fastq_class == SingleEndFastq:
            raise ValueError("It is not possible to merge single-end .fastq files!")
        possible_outcomes = {PairedEndFastq: PairedEndFastq}
        try:
            return possible_outcomes[fastq_class]
        except KeyError:
            raise ValueError(
                (
                    "Could not predict operation outcome (paired- or single-end)"
                    f"for input '{fastq_class}'."
                )
            )


@register("Pear")
class Pear(CommandLineWrapper, Merger):
    """
    Perform merging: the construction of a single read from the overlap between
    pairs of forward and reverse reads. Merging is performed by PEAR.

    :param minimum_overlap: minimum overlap between the two reads to be considered
        for merging.
    :type minimum_overlap: int
    :param minimum_length: The minimum length of the reads after merging.
        Reads shorter than the specified length will be discarded.
    :type minimum_length: int
    :param output_file_name_template: Template used to create the name of output files.
        The output file name template follows the syntax of format strings as descibed in
        `PEP 3101 <https://www.python.org/dev/peps/pep-3101/#id17/>`__. The
        template consists of text data that is transferred as-is to the output
        file name and replacement fields (indicated by curly braces) that
        describe what should be inserted in place of the field. The field name,
        the element inside the curly braces of the replacement field, must
        refer to a property attribute of the .fastq file if perform() is called.
        For this operation, an extra condition applies for the output filename
        template: it must end on '.assembled{extension}.', as this is the way
        PEAR formats the output file names.
    :type output_file_name_template: str
    :param output_directory: Path to an existing directory that will hold the
        output for this operation.
    :type output_directory: Union[Path, str]
    :raises ValueError: The minimum overlap is not an integer.
    :raises ValueError: The minimum overlap must have a value larger than 0.
    :raises ValueError: The minimum length must be an integer.
    :raises ValueError: The minimum length must have a value larger than 0.
    :raises ValueError: The output files from PEAR end with '.assembled{extension}.'
        Please specify this in the template for the output files in the configuration .ini file.
    """

    def __init__(
        self,
        minimum_overlap: int,
        minimum_length: int,
        output_file_name_template: str,
        output_directory: Union[Path, str],
    ):
        try:
            minimum_overlap = int(minimum_overlap)
        except ValueError:
            raise ValueError("The minimum overlap must be an integer.")

        if minimum_overlap <= 0:
            raise ValueError("The minimum overlap must have a value larger than 0.")

        try:
            minimum_length = int(minimum_length)
        except ValueError:
            raise ValueError("The minimum length must be an integer.")

        if minimum_length <= 0:
            raise ValueError("The minimum length must have a value larger than 0.")

        self._minimum_overlap = minimum_overlap
        self._minimum_length = minimum_length

        logger.debug(
            "Creating PEAR merge operation with options: output directory: "
            f"{output_directory}, output file name template: "
            f"{output_file_name_template}, minimum overlap between reads: "
            f"{self._minimum_overlap}, minimum read length: {self._minimum_length}"
        )

        CommandLineWrapper.__init__(self, "pear")
        Merger.__init__(self, output_file_name_template, output_directory)

    def perform(self, fastq: Fastq):
        if not isinstance(fastq, Fastq):
            raise ValueError("Expected a Fastq object.")
        if len(fastq.files) != 2:
            raise ValueError("Merging can only occur between two .fastq files.")
        pear_output_template = (
            self._output_file_name_template.replace("{extension}", ".assembled{extension}")
            if self.output_file_name_template.endswith("{extension}")
            else self._output_file_name_template + ".assembled.{extension}"
        )

        pear_unassembled_template = (
            self._output_file_name_template.replace("{extension}", ".unassembled{extension}")
            if self.output_file_name_template.endswith("{extension}")
            else self._output_file_name_template + ".unassembled.{extension}"
        )

        forward, reverse = [file_.resolve() for file_ in fastq.files]
        output_fastq = SingleEndFastq.create_from_properties(
            pear_output_template,
            self._output_directory,
            run=fastq.run,
            extension=".fastq",
            sample_name=fastq.sample_name,
            orientation=("3",),
        )
        unassembled_fastq = SingleEndFastq.create_from_properties(
            pear_unassembled_template,
            self._output_directory,
            run=fastq.run,
            extension=".fastq",
            sample_name=fastq.sample_name,
            orientation=("3",),
        )
        logger.debug(f"Created output fastq files {output_fastq}")
        if fastq.empty:
            output_fastq = output_fastq.rename(
                self._output_file_name_template,
                **{
                    **fastq.properties,
                    "orientation": "3",
                    "extension": fastq.extension,
                },
            )
            return SequencingData([output_fastq]), SequencingData()
        output_file = output_fastq.files[0]
        output_prefix_template = output_file.name[: -len(".assembled.fastq")]

        args = [
            "-f",
            str(forward),
            "-r",
            str(reverse),
            "-v",
            str(self._minimum_overlap),
            "-n",
            str(self._minimum_length),
            "-o",
            output_prefix_template,
            "-j",
            str(self._cores),
        ]
        super().run(*args, working_directory=self._output_directory)
        output_fastq = output_fastq.rename(
            self._output_file_name_template,
            **{**fastq.properties, "orientation": "3", "extension": fastq.extension},
        )

        if fastq.compressed:
            output_fastq = output_fastq.compress(self._output_directory, fastq.compression)
            unassembled_fastq = unassembled_fastq.compress(
                self._output_directory, fastq.compression
            )

        return SequencingData([output_fastq]), SequencingData([unassembled_fastq])

    def supports_multiprocessing(self):
        return True
