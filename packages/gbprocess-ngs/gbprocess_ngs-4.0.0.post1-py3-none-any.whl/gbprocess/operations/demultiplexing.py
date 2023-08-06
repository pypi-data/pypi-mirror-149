"""
Operations to perform .fastq demultiplexing.
"""

import logging
from abc import ABC
from pathlib import Path
from tempfile import NamedTemporaryFile
from typing import Dict, Type, Union

from Bio import Seq, SeqIO, SeqRecord

from ..data import Fastq, PairedEndFastq, SequencingData, SingleEndFastq
from ..utils import CommandLineWrapper, _is_valid_dna, fasta_to_dict, reverse_complement
from .operation import Operation, register

LOGGER = logging.getLogger("Demultiplexing")


class Demultiplexer(Operation, ABC):
    def introspect_outcome(self, fastq_class: Type[Fastq]) -> Type[Fastq]:
        possible_outcomes = {
            PairedEndFastq: PairedEndFastq,
            SingleEndFastq: SingleEndFastq,
        }
        try:
            return possible_outcomes[fastq_class]
        except KeyError:
            raise ValueError(
                (
                    "Could not predict operation outcome (paired- or single-end)"
                    f"for input '{fastq_class}'."
                )
            )


@register("CutadaptDemultiplex")
class CutadaptDemultiplex(CommandLineWrapper, Demultiplexer):
    """
    Perform sequence read demultiplexing using cutadapt.

    Split a .fastq file into one or more samples based on the presence of
    'barcodes': a short sequence of nucleotides that is uniquely linked
    to one sample. Barcodes can be 'anchored', meaning that they must
    be present at the beginning of the read. Additionally, in case of GBS data,
    the barcode sequence is typically followed by the remnant of the restriction
    enzyme cutsite that was used for digestion of the genomic DNA and
    ligation of the adapters. Specifying the barcode-side cutsite remnant
    sequence improves the demultiplexing specificity, as there is a longer
    sequence to match with.

    This operation adds the {sample_name} field to the file name template.

    :param error_rate: relative fraction of allowed mismatches for a barcode or
        barcode+remnant combination to be matched (0 for exact match;
        or between 0 and 1 to allow mismatches).
    :type error_rate: float
    :param barcodes: path to an existing barcodes .fasta file, where the name
        of the fasta record indicates the sample name, and the respective sequence
        defines the nucleotide sequence of its sample-specific barcode.
    :type barcodes: Union[Path, str]
    :param output_file_name_template: Template used to create the name of output files.
        The output file name template follows the
        syntax of format strings as descibed in
        `PEP 3101 <https://www.python.org/dev/peps/pep-3101/#id17/>`__. The
        template consists of text data that is transferred as-is to the output
        file name and replacement fields (indicated by curly braces) that
        describe what should be inserted in place of the field. The field name,
        the element inside the curly braces of the replacement field, must
        refer to a property attribute of the .fastq file if perform() is called.
    :type output_file_name_template: str
    :param output_directory: Path to an existing directory that will hold the
        output for this operation.
    :type output_directory: Union[Path, str]
    :param barcode_side_cutsite_remnant: String that describes the nucleotide
        sequence of the barcode-side cutsite remnant. defaults to ""
    :type barcode_side_cutsite_remnant: str, optional
    :param anchored_barcodes: Only look for the barcode sequence
        (or barcode + barcode-side cutsite remnant combination) at the beginning
        of the read. defaults to True
    :type anchored_barcodes: bool, optional
    :raises ValueError: error rate could not be interpreted as a floating point
        number.
    :raises AssertionError: The error rate must have a value between
        0 (incl.) and 1 (excl.).
    :raises ValueError: The barcodes .fasta file does not exist or is not a file.
    :raises ValueError: The barcode-side cutsite remnant sequence must only
        contain IUPAC nucleotide characters.
    """

    def __init__(
        self,
        error_rate: float,
        barcodes: Union[Path, str],
        output_file_name_template: str,
        output_directory: Union[Path, str],
        barcode_side_cutsite_remnant="",
        anchored_barcodes=True,
    ):
        try:
            error_rate = float(error_rate)
        except ValueError:
            raise ValueError("The error rate must be a floating number.")
        else:
            assert 0 <= error_rate < 1, (
                "The error rate must have a value ",
                "between 0 (incl.) and 1 (excl.).",
            )

        barcodes = Path(barcodes)
        if not barcodes.is_file():
            raise ValueError("The barcodes .fasta file does " + "not exist or is not a file.")
        try:
            self._barcode_side_cutsite_remnant = fasta_to_dict(barcode_side_cutsite_remnant)
        except FileNotFoundError:
            self._barcode_side_cutsite_remnant = barcode_side_cutsite_remnant.strip("\"'")
            if not _is_valid_dna(self._barcode_side_cutsite_remnant):
                raise ValueError(
                    (
                        "The barcode-side cutsite remnant is neither a "
                        "valid DNA sequence or a valid .fasta file."
                    )
                )
        self._error_rate = error_rate
        self._barcodes_dict = fasta_to_dict(barcodes)
        if not self._barcodes_dict:
            raise ValueError("The fasta file containing the barcodes seems to be empty.")
        self._anchored_barcodes = anchored_barcodes
        self._barcodes_with_re = self._combine_barcodes_with_restriction_site(self._barcodes_dict)

        CommandLineWrapper.__init__(self, "cutadapt")
        Demultiplexer.__init__(self, output_file_name_template, output_directory)

    def perform(self, fastq: Fastq) -> SequencingData:
        """Perform demultiplexing on the target .fastq sample.

        :param fastq: Input .fastq file(s). Both single-end and paired-end
            sequencing types are accepted. The Property attributes of the
            Fastq object that correspond to the field names of the output
            file name template, must be defined.
        :type fastq: Fastq
        :raises ValueError: This operation requires one or two .fastq files
            as input, but more were specified.
        :return: A new SequencingData object, which specifies a list of
            samples that are the result of the demultiplexing.
        :rtype: SequencingData
        """
        LOGGER.debug("Processing %r." % fastq)
        if not isinstance(fastq, Fastq):
            raise ValueError("Expected a Fastq object.")

        if len(fastq.files) > 2:
            raise ValueError("Cutadapt requires one or two input .fastq files.")

        output_fastq = [
            fastq.create_from_properties(
                self._output_file_name_template,
                self._output_directory,
                orientation=fastq.orientation,
                run=fastq.run,
                extension=fastq.extension,
                sample_name=sample_name,
            )
            for sample_name in self._barcodes_dict.keys()
        ]
        aux_fastq = fastq.create_from_properties(
            self._output_file_name_template,
            self._output_directory,
            orientation=fastq.orientation,
            run=fastq.run,
            extension=fastq.extension,
            sample_name="unknown",
        )

        LOGGER.debug("Created output fastq files %s.", str(output_fastq))

        if fastq.empty:
            LOGGER.debug("Input fastq is empty, returning empty files.")
            return SequencingData(output_fastq), SequencingData([aux_fastq])

        output_template_for_cutadapt = self._output_file_name_template.replace(
            "{sample_name}", "{{name}}"
        )
        filled_output_template = fastq.fill_template_to_path(
            output_template_for_cutadapt,
            orientation=fastq.orientation,
            run=fastq.run,
            extension=fastq.extension,
        )

        output_file_names_arg = [
            part for arg_ in list(zip(["-o", "-p"], filled_output_template)) for part in arg_
        ]
        with NamedTemporaryFile("w") as temp_barcodes_fasta:
            LOGGER.debug("Barcodes fasta: %s", temp_barcodes_fasta.name)
            LOGGER.debug("Length of barcodes fasta dict: %s", len(self._barcodes_with_re))
            SeqIO.write(self._barcodes_with_re.values(), temp_barcodes_fasta, "fasta")
            temp_barcodes_fasta.flush()
            LOGGER.debug("Barcodes fasta file flushed.")
            args = [
                "-e",
                str(self._error_rate),
                "--no-indels",
                "--action=none",
                "-g",
                "file:{}".format(str(temp_barcodes_fasta.name)),
                "--compression-level=9",
            ]
            args.extend(output_file_names_arg)
            args.extend([str(file_) for file_ in fastq.files])
            super().run(*args, working_directory=self._output_directory)
        return SequencingData(output_fastq), SequencingData([aux_fastq])

    def _combine_barcodes_with_restriction_site(
        self, barcodes_dict: dict
    ) -> Dict[str, SeqRecord.SeqRecord]:
        """
        For every barcode in the barcodes .fasta file, add the restriction enzyme cutsite remnant as
        a suffix. Additionally, if the barcodes should be anchored, add '^'
        to the beginning of each nucleotide sequence.
        """
        result = dict()
        for sample_name, barcode_sequence in barcodes_dict.items():
            restriction_site_sequence = self.barcode_side_cutsite_remnant(sample_name)
            combined = barcode_sequence + reverse_complement(restriction_site_sequence)
            final_sequence = f"^{combined}" if self._anchored_barcodes else combined
            result[sample_name] = SeqRecord.SeqRecord(
                Seq.Seq(final_sequence),
                id=sample_name,
                name=sample_name,
                description=sample_name,
            )
            if len(combined) < 10:
                LOGGER.warning(
                    "The length of the sequence used for "
                    + "demultiplexing sample %s is potentially "
                    + "too small (%s).",
                    sample_name,
                    len(barcode_sequence + restriction_site_sequence),
                )
        LOGGER.debug("Barcodes used: %s", result)
        return result

    def barcode_side_cutsite_remnant(self, sample_name: str):
        try:
            return self._barcode_side_cutsite_remnant[sample_name]
        except TypeError:
            return self._barcode_side_cutsite_remnant
        except KeyError:
            raise ValueError(
                (
                    f"Sample {sample_name} could not be found in "
                    "the barcode side cutsite remnants .fasta file."
                )
            )

    def supports_multiprocessing(self):
        """This operation does not support multiprocessing."""
        return False
