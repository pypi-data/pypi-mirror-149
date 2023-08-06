"""
Operations to perform .fastq trimming.
"""
import logging
from abc import ABC
from itertools import accumulate
from pathlib import Path
from typing import Type, Union

from ..data import Fastq, PairedEndFastq, SequencingData, SingleEndFastq
from ..utils import CommandLineWrapper, _is_valid_dna, fasta_to_dict, reverse_complement
from .operation import Operation, register

logger = logging.getLogger("Trimming")

# Barcode side primers are the same for Nextera and TruSeq
SEQUENCING_PRIMERS = {
    "Nextera": {
        "barcode_side": "ACACTCTTTCCCTACACGACGCTCTTCCGATCT",
        "common_side": "CGGTCTCGGCATTCCTGCTGAACCGCTCTTCCGATCT",
    },
    "TruSeq": {
        "barcode_side": "ACACTCTTTCCCTACACGACGCTCTTCCGATCT",
        "common_side": "GTGACTGGAGTTCAGACGTGTGCTCTTCCGATCT",
    },
}


class Trimmer(Operation, ABC):
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


@register("CutadaptTrimmer")
class CutadaptTrimmer(CommandLineWrapper, Trimmer):
    """
        Perform trimming of barcodes, restriction enzyme cutsite remnants,
        adapters, and possible variable spacers.

    Scheme of sequenced reads in a double-digest GBS experiment::

        (top strand of GBS fragment is shown)
        ...|--barcode adapter--|-barcode-|-RE1-|-genomic insert-|-RE2-|-(spacer)-|--common adapter--|... # noqa: E501

          F sequencing primer->|-------------------- forward read ---------------->
                    <---------------- reverse read ------------------------------|<-R sequencing primer # noqa: E501

        after first trimming round:
                                               |---- forward read ---------------->
                    <---------------- reverse read -------------|

    The operation consists of two subsequent phases:
    The behavior of the first phase is dependant on whether or not the data contains spacers.
    If spacers are present, the 5' sides of the forward and reverse reads are trimmed
    utilizing pattern trimming. In the forward reads, the barcodes and RE are removed.
    In the reverse reads (spacers and) restriction site remnants are removed.
    For each read the length difference between the barcode or spacer is calculated
    with the maximum barcode and spacer length. In order to level the reads for further
    operations, all reads are positionally trimmed at their 3' side by an amount of bases
    equal the previously calculated length difference.

    ::

        forward read:
        (sequenced read is shown as it appears in the .fastq file, after positional trimming)
        |-genomic insert-|-RE2-|-(spacer)-|--common adapter--|...

        reverse read:
        (sequenced read is shown as it appears in the .fastq file, after positional trimming)
        |-genomic insert-|-RE1-|-barcode-|--barcode adapter--|...

    The behavior of the first phase differs when no spacers are present.
    In this case, the sequences at the beginning of the forward (barcode + RE1)
    and reverse (RE2) are removed not by using the pattern of nucleotices,
    but by removing a fixed number of bases, regardless of which bases
    they may be (positional trimming).

    In the second phase, pattern matching is used to trim the possible remaining constructs at the
    3' sides of the forward and reverse reads.

    In the forward read (if the length of the read is a bit longer than the length
    of the genomic insert), a restriction enzyme cutsite remnant followed by an
    adapter sequence may be expected towards the 3' end (see scheme above).
    The adapter sequence usually corresponds with the Illumina sequencing
    primer used to obtain the reverse read.
    For forward reads, the restriction enzyme cutsite remnant to be removed is
    corresponds to the 'common-side cutsite remnant',
    and the adapter sequence corresponds to the 'common-side sequencing primer'.

    For reverse reads, a restriction enzyme cutsite remnant followed by
    the sample-specific barcode and an adapter sequence may be expected
    towards the 3' end (see scheme above). The adapter sequence usually corresponds
    with the Illumina sequencing primer used to obtain the forward read.
    For reverse reads, the restriction enzyme cutsite remnant to be removed
    corresponds to the 'barcode-side cutsite remnant',
    and the adapter sequence corresponds to the 'barcode-side sequencing primer'.

    If a variable spacer was used, then in the previous round, the variable spacer
    was determined for each read and can now be used to trim of the possible 3'
    restriction enzyme cutsite remnants, spacers, and common adapters from the
    forward reads.

    With pattern trimming, the reads are trimmed even if the searched pattern is only
    partially present at the 3' end of the read.
    Conversely, if the pattern is found internally in the read sequence,
    the remainder of the read towards the 3' end is also trimmed off.

    ::

        forward read:
        (sequenced read is shown as it appears in the .fastq file, after positional trimming)
        |-genomic insert-|

        reverse read:
        (sequenced read is shown as it appears in the .fastq file, after positional trimming)
        |-genomic insert-|

    This operation is tailored for GBS methods where the barcode and restriction enzyme
    cutsite remnant (RE) sequences must be removed from the 5' side of forward reads
    and the 3' side of reverse reads, and the restriction enzyme cutsite remnants and
    possible spacers from the 5' side of reverse reads and the 3' side of forward reads.
    The operation can handle variable length sample-specific barcodes and read-specific
    spacers.

    The user must provide the sequences of the restriction
    enzyme cutsite remants, the sequencing primers, the
    sample-specific barcodes, and possible variable spacers to :class:`.Trimming`.

    Depending on the protocol, one (single-digest GBS) or two (double-digest GBS)
    restriction enzymes are used to cut the genomic DNA before adapter ligation.

    In single-digest GBS, the restriction enzyme cutsite remnant sequence is the same for both
    the 'barcode-side cutsite remnant' and the 'common-side cutsite remnant'.
    In double-digest GBS, the restriction enzyme sequence used in the adapters
    that also carry the barcode is called the 'barcode-side cutsite remnant',
    while the restriction enzyme sequence used in the common adapters
    (without barcode) is called the 'common-side cutsite remnant'.

    How to determine the restriction enzyme cutsite remnant?

    The easiest way to deduce the restriction enzyme cutsite remnant is to first look up the
    restriction enzyme recognition site on e.g. `NEB <https://international.neb.com/>`__.
    If the result of double strand digestion would leave an overhang (sticky end)
    on the top strand, then the restriction enzyme cutsite remnant is equal
    to the sequence of the top strand up to the cut strand breakpoint
    (indicated by little diamonds on the top strand on NEB).In contrast, if the double
    strand digestion would leave an overhang (sticky end) on the bottom strand,
    then the restriction enzyme cutsite remnant is equal to the
    *complement* of the *bottom* strand sequence up to the cut strand breakpoint
    (indicated by little diamonds on the bottom strand on NEB)

    Below we show examples for `PstI <https://international.neb.com/products/r0140-psti>`__,
    `MspI <https://international.neb.com/products/r0106-mspi>`__,
    `ApeKI <https://www.neb.com/products/r0643-apeki>`__,
    and `EcoRI <https://international.neb.com/products/r0101-ecori>`__
    where the '|' symbol indicates where the endonuclease would cut the strand in the
    nucleotide sequence.

    ::

        #PstI
        before digestion  -->    after digestion
        5'--CTGCA|G--3'          5'--CTGCA|  Overhang located on top strand.
        3'--G|ACGTC--5'          3'--G|
        Sequence of top strand up to cut site: CTGCA
        Restriction enzyme cutsite remnant: CTGCA

        #MspI
        before digestion  -->    after digestion
        5'--C|CGG--3'            5'--C|
        3'--GGC|C--5'            3'--GGC|    Overhang located on bottom strand.
        Sequence of bottom strand up to cut site: GGC
        Restriction enzyme cutsite remnant: CCG

        #ApeKI
        before digestion  -->    after digestion
        5'--G|CWGC--3'           5'--G|
        3'--CGWC|G--5'           3'--CGWC|  Overhang located on bottom strand.
        Sequence of bottom strand up to cut site: CGWC
        Restriction enzyme cutsite remnant: GCWG

        #EcoRI
        before digestion:  -->   after digestion:
        5'--G|AATTC--3'          5'--G|
        3'--CTTAA|G--5'          3'--CTTAA|  Overhang located on bottom strand.
        Sequence of bottom strand up to cut site: CTTAA
        Restriction enzyme cutsite remnant: GAATT

    :param barcode_side_sequencing_primer: Either the nucleotide sequence of
        the primer that was used to initiate sequencing on the barcode-side or
        'Nextera' or 'TruSeq' to use a predefined value.
    :type barcode_side_sequencing_primer: str
    :param common_side_sequencing_primer: Either the nucleotide sequence of
        the primer that was used to initiate sequencing on the common-side or
        'Nextera' or 'TruSeq' to use a predefined value.
    :type common_side_sequencing_primer: str
    :param barcode_side_cutsite_remnant: Nucleotide sequence of the barcode-
        side cutsite remnant. May also be provided in a .fasta file where each
        sample is followed by its barcode_side_cutsite_remnant.
    :type barcode_side_cutsite_remnant: str
    :param common_side_cutsite_remnant: Nucleotide sequence of the common-
        side cutsite remnant. May also be provided in a .fasta file where each
        sample is followed by its common_side_cutsite_remnant.
    :type common_side_cutsite_remnant: str
    :param barcodes: path to an existing barcodes .fasta file, where the name
        of the fasta record indicates the sample name, and the respective sequence
        defines the nucleotide sequence of its sample-specific barcode.
    :type barcodes: Union[Path, str]
    :param anchored_adapters: Adapters must be present at the end of the read.
        In other words: the adapters must be the suffixes of the reads in order
        for them to be trimmed. defaults to True.
    :type anchored_adapters: bool
    :param spacer: sequence of the longest possible variable spacer in 5'-3' direction
        of the genomic fragment. GbprocesS will consider every iteratively
        smaller fragment, until only the 5' base is left, as a possible spacer.
        Parameter only available for paired-end data.
    :type spacer: str
    :param minimum_length: Minimum length of the reads after trimming, shorter
        reads are discarded from the output.
    :type minimum_length: int
    :param error_rate: rate of errors allowed between query sequences and the
        reads. Expressed as a floating point number from the interval ]0,1].
        The error rate is only applied when removing sequences from the 5' of
        the reads (phase 2).
    :type error_rate: float
    :param output_file_name_template: Template used to create
        the name of the output files. The output file name template follows the
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
    :raises ValueError: The minimum length of the trimmed read must be
        interpretable as an integer.
    :raises ValueError: The minimum length of the trimmed read must be
        an integer above 0.
    :raises ValueError: The error rate must be interpretable as a
        float.
    :raises ValueError: The barcode-side sequencing primer is neither a predefined
        value (e.g. "TruSeq" or "Nextera") nor a valid DNA sequence.
    :raises ValueError: The common-side sequencing primer is neither a predefined
        value (e.g. "TruSeq" or "Nextera") nor a valid DNA sequence.
    :raises ValueError: The common-side sequencing primer and the common-
        side cutsite remnant must be defined.
    :raises ValueError: The barcode-side cutsite remnant is not a valid DNA sequence.
    :raises ValueError: The common-side cutsite remnant is not a valid DNA sequence.
    :raises ValueError: If either the barcode-side sequencing primer or the
        barcode-side cutsite remnant are specified (to trim reverse reads),
        the other one must be defined as well.
    :raises ValueError: The barcodes .fasta file does not exist or is not a file.
    :raises ValueError: The error rate must have a value equal
        to 0 (perfect match) or larger than 0 and smaller than one ([0,1[).
    """

    def __init__(
        self,
        barcode_side_sequencing_primer: str,
        common_side_sequencing_primer: str,
        barcode_side_cutsite_remnant: str,
        common_side_cutsite_remnant: str,
        barcodes: Union[Path, str],
        minimum_length: int,
        error_rate: float,
        output_file_name_template: str,
        output_directory: Union[Path, str],
        anchored_adapters=True,
        spacer=None,
    ):
        # TODO: check input even more
        try:
            minimum_length = int(minimum_length)
        except ValueError:
            raise ValueError("The minimum length must be an integer.")

        if minimum_length <= 0:
            raise ValueError("The minimum length must have a value larger than 0.")

        try:
            error_rate = float(error_rate)
        except ValueError:
            raise ValueError("The error rate value must be a float.")

        if 0 > error_rate >= 1:
            raise ValueError(
                "The error rate must have a value equal to 0 (perfect match) "
                "or larger than 0 but smaller than one ([0,1[)."
            )

        if barcodes:
            self._barcodes = fasta_to_dict(barcodes)
        # self._input_file_names = input_file_name_template
        barcode_side_sequencing_primer = barcode_side_sequencing_primer.strip("\"'")
        common_side_sequencing_primer = common_side_sequencing_primer.strip("\"'")
        try:
            self._barcode_adapter_sequence = SEQUENCING_PRIMERS[barcode_side_sequencing_primer][
                "barcode_side"
            ]
        except KeyError:
            if not _is_valid_dna(barcode_side_sequencing_primer):
                raise ValueError(
                    "The barcode-side sequencing primer is not a "
                    f'value from "{SEQUENCING_PRIMERS.keys()} ",'
                    "or not a valid DNA sequence."
                )
            self._barcode_adapter_sequence = barcode_side_sequencing_primer

        try:
            self._common_adapter_sequence = SEQUENCING_PRIMERS[common_side_sequencing_primer][
                "common_side"
            ]
        except KeyError:
            if not _is_valid_dna(common_side_sequencing_primer):
                raise ValueError(
                    "The common-side sequencing primer is not a "
                    f'value from "{SEQUENCING_PRIMERS.keys()}",'
                    "or not a valid DNA sequence."
                )
            self._common_adapter_sequence = common_side_sequencing_primer
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

        try:
            self._common_side_cutsite_remnant = fasta_to_dict(common_side_cutsite_remnant)
        except FileNotFoundError:
            self._common_side_cutsite_remnant = common_side_cutsite_remnant.strip("\"'")
            if not _is_valid_dna(self._common_side_cutsite_remnant):
                raise ValueError(
                    (
                        "The common-side cutsite remnant is neither a "
                        "valid DNA sequence or a valid .fasta file."
                    )
                )

        if anchored_adapters in ("True", True):
            anchored_adapters = True
        elif anchored_adapters in ("False", False):
            anchored_adapters = False
        else:
            raise ValueError("The option 'anchored_adapters' must have a value True or False.")

        self._anchored_adapters = anchored_adapters

        if not self._common_adapter_sequence or not self._common_side_cutsite_remnant:
            raise ValueError(
                "The common-side sequencing primer and the barcode-"
                + "side cutsite remnant must be defined."
            )
        self._minimum_length = minimum_length
        self._error_rate = error_rate
        self._spacer = "" if spacer is None else spacer
        CommandLineWrapper.__init__(self, "cutadapt")
        Trimmer.__init__(self, output_file_name_template, output_directory)

    @classmethod
    def builder(cls, fastq_type: Type[Fastq]):
        builders = {
            SingleEndFastq: SingleEndTrimmer,
            PairedEndFastq: PairedEndTrimmer,
            Fastq: cls,
        }
        return builders[fastq_type]

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

    def common_side_cutsite_remnant(self, sample_name: str):
        try:
            return self._common_side_cutsite_remnant[sample_name]
        except TypeError:
            return self._common_side_cutsite_remnant
        except KeyError:
            raise ValueError(
                (
                    f"Sample {sample_name} could not be found in "
                    "the common side cutsite remnants .fasta file."
                )
            )

    def perform(self, fastq: Fastq):
        output_fastq = fastq.create_from_properties(
            self._output_file_name_template,
            self._output_directory,
            orientation=fastq.orientation,
            run=fastq.run,
            extension=fastq.extension,
            sample_name=fastq.sample_name,
        )
        common_side_cutsite_remnant = self.common_side_cutsite_remnant(fastq.sample_name)
        barcode_side_cutsite_remnant = self.barcode_side_cutsite_remnant(fastq.sample_name)

        # Get barcode information
        barcode = self._get_barcode(fastq)
        largest_barcode = max(self._barcodes.values(), key=len)

        # Calculate the compensation for variable barcode length
        forward_read_compenstation_length = len(largest_barcode) - len(barcode)

        # Sequences to be removed at the start of the forward read
        start_forward_read = barcode + reverse_complement(barcode_side_cutsite_remnant)

        # ACGT -> ['', 'T', 'GT', 'CGT', 'ACGT']
        possible_spacers = [""] + [
            spacer_part[::-1] for spacer_part in accumulate(self._spacer[::-1])
        ]
        previous_untrimmed = None
        sample_name = fastq.sample_name
        for possible_spacer in possible_spacers[::-1]:
            # Prepare files for the untrimmed reads in the first cutadapt round
            untrimmed = fastq.create_from_properties(
                self._output_file_name_template,
                self._output_directory,
                orientation=fastq.orientation,
                run=fastq.run,
                extension=fastq.extension,
                sample_name=f"untrimmed_{possible_spacer}{sample_name}",
            )
            if fastq.empty:
                return SequencingData([output_fastq]), SequencingData([untrimmed])

            output_untrimmed_file_arg = [
                part
                for arg_ in list(
                    zip(
                        ["--untrimmed-output", "--untrimmed-paired-output"],
                        untrimmed.files,
                    )
                )
                for part in arg_
            ]

            # Prepare output file for this spacer
            output_fastq_spacer = fastq.create_from_properties(
                f"{possible_spacer}_{self._output_file_name_template}",
                self._output_directory,
                orientation=fastq.orientation,
                run=fastq.run,
                extension=fastq.extension,
                sample_name=sample_name,
            )
            output_file_arg = [
                part for arg_ in list(zip(["-o", "-p"], output_fastq_spacer.files)) for part in arg_
            ]

            # Prepare files for the trimmed reads in the first cutadapt round
            trimmed = fastq.create_from_properties(
                f"trimmed_{possible_spacer}{self._output_file_name_template}",
                self._output_directory,
                orientation=fastq.orientation,
                run=fastq.run,
                extension=fastq.extension,
                sample_name=fastq.sample_name,
            )
            output_trimmed_file_arg = [
                part for arg_ in list(zip(["-o", "-p"], trimmed.files)) for part in arg_
            ]

            # Get sequences to trim from start of reverse read
            start_reverse_read = (
                f"{possible_spacer}{reverse_complement(common_side_cutsite_remnant)}"
            )

            # Calculate compensation for variable spacer length
            reverse_read_compensation_length = len(self._spacer) - len(possible_spacer)

            args_first_cutadapt_run = [
                "-g",
                f"^{start_forward_read};e=0",
            ]
            if len(fastq.files) == 2:
                args_first_cutadapt_run.extend(
                    [
                        "-G",
                        f"^{start_reverse_read};e=0",
                        "--pair-filter=any",
                        "--pair-adapters",
                        "--minimum-length",
                        self._minimum_length,
                    ]
                )

            # Add untrimmed output only in the case where we do not use -u for the first
            # cutadapt run (see comment directly below, where args get overwritten).
            # The -u option is not trimming, so only using -u without any trimming option
            # results in all reads being redirected to the untrimmed output.
            # We want the output in the trimmed output for the second run.
            args_first_cutadapt_run.extend(output_untrimmed_file_arg)

            if len(possible_spacers) == 1:
                # The user did not specify a spacer sequence, so possible_spacers=[""]
                # In this case we remove a number of bases from the front of the forward read,
                # irrespective of the sequences of the read. The number of bases removed is
                # equal to the combined length of the barcode and the
                args_first_cutadapt_run = ["-u", len(start_forward_read)]

                if len(fastq.files) == 2:
                    args_first_cutadapt_run.extend(["-U", len(common_side_cutsite_remnant)])

            args_first_cutadapt_run.extend(fastq.files)
            args_first_cutadapt_run.extend(output_trimmed_file_arg)
            super().run(*args_first_cutadapt_run, working_directory=self._output_directory)

            anchored = "X" if self._anchored_adapters else ""
            args_second_cutadapt_run = [
                "-e",
                self._error_rate,
                "-u",
                -forward_read_compenstation_length,
                "--minimum-length",
                self._minimum_length,
                "-a",
                common_side_cutsite_remnant
                + reverse_complement(possible_spacer)
                + f"{reverse_complement(self._common_adapter_sequence)}{anchored}",
            ]
            if len(fastq.files) == 2:
                args_second_cutadapt_run.extend(
                    [
                        "-A",
                        barcode_side_cutsite_remnant
                        + reverse_complement(barcode)
                        + f"{reverse_complement(self._barcode_adapter_sequence)}{anchored}",
                        "-U",
                        -reverse_read_compensation_length,
                    ]
                )
            args_second_cutadapt_run.extend(output_file_arg)
            args_second_cutadapt_run.extend(trimmed.files)
            super().run(*args_second_cutadapt_run, working_directory=self._output_directory)
            trimmed.remove()
            output_fastq.join(output_fastq_spacer)
            if previous_untrimmed:
                previous_untrimmed.remove()
            previous_untrimmed = untrimmed
            fastq = untrimmed
        return SequencingData([output_fastq]), SequencingData([untrimmed])

    def _get_barcode(self, fastq: Fastq) -> str:
        """
        Based on the sample name, get the barcode sequence for
        the sample from the barcode .fasta file.
        """
        # Get a list of possible file names
        sample_name = fastq.sample_name
        try:
            return self._barcodes[sample_name]
        except KeyError:
            raise ValueError("Barcode {} not found in barcodes file.".format(sample_name))

    def supports_multiprocessing(self):
        return False  # Cutadapt multiprocessing is slow


class SingleEndTrimmer(CutadaptTrimmer):
    def __init__(
        self,
        common_side_sequencing_primer: str,
        common_side_cutsite_remnant: str,
        barcode_side_cutsite_remnant: str,
        barcodes: Union[Path, str],
        minimum_length: int,
        error_rate: float,
        output_file_name_template: str,
        output_directory: Union[Path, str],
        anchored_adapters=True,
        spacer="",
    ):  # Add spacer here so we can catch the input
        if spacer:
            raise ValueError("Trimming spacers is not supported for single-end data.")
        super().__init__(
            "",
            common_side_sequencing_primer,
            barcode_side_cutsite_remnant,
            common_side_cutsite_remnant,
            barcodes,
            minimum_length,
            error_rate,
            output_file_name_template,
            output_directory,
            anchored_adapters=anchored_adapters,
            spacer="",
        )


class PairedEndTrimmer(CutadaptTrimmer):
    def __init__(
        self,
        barcode_side_sequencing_primer: str,
        common_side_sequencing_primer: str,
        barcode_side_cutsite_remnant: str,
        common_side_cutsite_remnant: str,
        barcodes: Union[Path, str],
        minimum_length: int,
        error_rate: float,
        output_file_name_template: str,
        output_directory: Union[Path, str],
        anchored_adapters=True,
        spacer="",
    ):
        super().__init__(
            barcode_side_sequencing_primer,
            common_side_sequencing_primer,
            barcode_side_cutsite_remnant,
            common_side_cutsite_remnant,
            barcodes,
            minimum_length,
            error_rate,
            output_file_name_template,
            output_directory,
            anchored_adapters=anchored_adapters,
            spacer=spacer,
        )
