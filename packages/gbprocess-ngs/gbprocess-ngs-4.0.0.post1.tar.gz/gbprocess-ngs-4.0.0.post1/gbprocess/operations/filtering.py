"""
Operations to perform .fastq filtering.
"""
import logging
from abc import ABC
from collections import deque
from pathlib import Path
from typing import Iterable, Type, Union

from ..data import Fastq, PairedEndFastq, SequencingData, SingleEndFastq
from ..utils import CommandLineWrapper, _is_valid_dna, fasta_to_dict
from .operation import Operation, register

LOGGER = logging.getLogger("Filtering")


class Filter(Operation, ABC):
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
                    "Could not predict operation outcome (paired- or single-end) "
                    f"for input '{fastq_class}'."
                )
            )


@register("MaxNFilter")
class MaxNFilter(CommandLineWrapper, Filter):
    """
    Filter .fastq reads based on the number of uncalled nucleotides present.
    Reads are discarded if more than the specified threshold of 'N' nucleotides are present.

    :param max_n: Maximum number of allowed uncalled nucleotides in the reads.
    :type max_n: int
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
    :raises ValueError: The maximum number of uncalled nucleotides could not be
        interpreted as an integer.
    :raises ValueError: The maximum number of uncalled nucleotides should be expressed
        as a POSITIVE integer (0 included).
    """

    #    :raises ValueError: The output directory is not an existing directory. should we add this?

    def __init__(
        self,
        max_n: int,
        output_file_name_template: str,
        output_directory: Union[Path, str],
    ):
        try:
            max_n = int(max_n)
        except ValueError:
            raise ValueError(
                "The maximum number of uncalled nucleotides should be expressed as an integer."
            )
        else:
            if not 0 <= max_n:
                raise ValueError(
                    "The maximum number of uncalled nucleotides "
                    "should be expressed as POSITIVE integer (0 included)."
                )
        self._max_n = max_n
        CommandLineWrapper.__init__(self, "cutadapt")
        Filter.__init__(self, output_file_name_template, output_directory)

    class Builder:
        def __init__(self, fastq_type: Type[Fastq]):
            self._fastq_type: Type[Fastq] = fastq_type

        def build(self, *args, **kwargs):
            return MaxNFilter(*args, **kwargs)

    def perform(self, fastq: Fastq) -> SequencingData:
        """Perform the filtering on the target .fastq sample.

        :param fastq: Input .fastq file(s). Both single-end and paired-end
            sequencing types are accepted. The Property attributes of the
            Fastq object that correspond to the field names of the output
            file name template must be defined.
        :type fastq: Fastq
        :raises ValueError: This operation requires one or two .fastq files
            as input, but more were specified.
        :return: A new SequencingData object, which specifies a list of
            samples that are the result of the filtering.
        :rtype: SequencingData
        """
        if not isinstance(fastq, Fastq):
            raise ValueError("Expected a Fastq object.")
        files = fastq.files
        output_fastq = fastq.create_from_properties(
            self._output_file_name_template,
            self._output_directory,
            orientation=fastq.orientation,
            run=fastq.run,
            extension=fastq.extension,
            sample_name=fastq.sample_name,
        )
        if fastq.empty:
            return SequencingData([output_fastq]), SequencingData()
        output_files = [file_.name for file_ in output_fastq.files]

        output_file_arg = [part for arg_ in list(zip(["-o", "-p"], output_files)) for part in arg_]
        args = [
            "--max-n",
            self._max_n,
            # "-j", self.cores
        ]
        args.extend(output_file_arg)
        args.extend(files)
        super().run(*args, working_directory=self._output_directory)
        return SequencingData([output_fastq]), SequencingData()

    def supports_multiprocessing(self):
        return False  # Cutadapt multiprocessing is slow


@register("LengthFilter")
class LengthFilter(CommandLineWrapper, Filter):
    """Remove records from a .fastq file with a read length smaller than a predefined size.

    :param minimum_length: Minimum length of the sequencing read to be retained in the output.
    :type minimum_length: int
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
    :raises ValueError: The mimimum length of the reads could not be interpreted as an integer.
    :raises ValueError: The mimimum length of the reads should be
        expressed as a POSITIVE integer (0 included).
    """

    def __init__(
        self,
        minimum_length: int,
        output_file_name_template: str,
        output_directory: Union[Path, str],
    ):
        try:
            minimum_length = int(minimum_length)
        except ValueError:
            raise ValueError("The mimimum length of the read should be expressed as an integer.")
        else:
            if not 0 <= minimum_length:
                raise ValueError(
                    "The mimimum length of the reads should be "
                    "expressed as POSITIVE integer (0 included.)."
                )

        self._minimum_length = minimum_length
        CommandLineWrapper.__init__(self, "cutadapt")
        Filter.__init__(self, output_file_name_template, output_directory)

    class Builder:
        def __init__(self, fastq_type: Type[Fastq]):
            self._fastq_type: Type[Fastq] = fastq_type

        def build(self, *args, **kwargs):
            return LengthFilter(*args, **kwargs)

    def perform(self, fastq: Fastq):
        """Perform the filtering on the target .fastq sample.

        :param fastq: Input .fastq file(s). Both single-end and paired-end
            sequencing types are accepted. The Property attributes of the
            Fastq object that correspond to the field names of the output
            file name template must be defined.
        :type fastq: Fastq
        :return: A new SequencingData object, which specifies a list of
            samples that are the result of the filtering.
        :rtype: SequencingData
        """
        if not isinstance(fastq, Fastq):
            raise ValueError("Expected a Fastq object.")
        files = fastq.files
        output_fastq = fastq.create_from_properties(
            self._output_file_name_template,
            self._output_directory,
            orientation=fastq.orientation,
            run=fastq.run,
            extension=fastq.extension,
            sample_name=fastq.sample_name,
        )
        if fastq.empty:
            return SequencingData([output_fastq]), SequencingData()
        output_files = [file_.name for file_ in output_fastq.files]
        output_file_arg = [part for arg_ in list(zip(["-o", "-p"], output_files)) for part in arg_]
        args = [
            "--minimum-length",
            self._minimum_length
            # "-j", self.cores
        ]
        args.extend(output_file_arg)
        args.extend(files)
        super().run(*args, working_directory=self._output_directory)
        return SequencingData([output_fastq]), SequencingData()

    def supports_multiprocessing(self):
        return False  # Cutadapt multiprocessing is slow


@register("AverageQualityFilter")
class AverageQualityFilter(Filter):
    """
    Remove records from a .fastq file based on the average quality of the
    whole read.

    The ASCII quality score line of the .fastq records are interpreted
    using the Illumina 1.8+ Phred+33 encoding. An average of the resulting
    integers is compared to a set threshold. Reads with an average quality score
    below this threshold are discarded.

    :param average_quality: Minimum average quality threshold (Phred+33) to retain a read
        in the output.
    :type average_quality: int
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
    :raises ValueError: The average quality threshold could not be interpreted as an integer.
    """

    def __init__(
        self,
        average_quality: int,
        output_file_name_template: str,
        output_directory: Union[Path, str],
    ):
        try:
            average_quality = int(average_quality)
        except ValueError:
            raise ValueError("The average quality of the read should be expressed as an integer.")
        if average_quality < 0:
            raise ValueError("A phred score can not be lower than 0.")
        self._average_quality = average_quality
        super().__init__(output_file_name_template, output_directory)

    class Builder:
        def __init__(self, fastq_type: Type[Fastq]):
            self._fastq_type: Type[Fastq] = fastq_type

        def build(self, *args, **kwargs):
            return AverageQualityFilter(*args, **kwargs)

    def perform(self, fastq: Fastq):
        if not isinstance(fastq, Fastq):
            raise ValueError("Expected a Fastq object.")
        output_fastq = fastq.create_from_properties(
            self._output_file_name_template,
            self._output_directory,
            orientation=fastq.orientation,
            run=fastq.run,
            extension=fastq.extension,
            sample_name=fastq.sample_name,
        )
        if fastq.empty:
            return SequencingData([output_fastq]), SequencingData()
        output_records = [None] * 20000
        i = -1
        with fastq.open("rt") as open_fq:
            for records in open_fq.records():
                write_records = True
                for record in records:
                    phred_scores = record.letter_annotations.get("phred_quality")
                    average_score = sum(phred_scores) / len(phred_scores)
                    if average_score < self._average_quality:
                        write_records = False
                        break
                if write_records:
                    i += 1
                    try:
                        output_records[i] = records
                    except IndexError:
                        with output_fastq.open("at") as open_fq:
                            open_fq.write_records(*zip(*output_records))
                        output_records = [None] * 20000
                        output_records[0] = records
                        i = 0

        self.remove_trailing_none(output_records)
        if output_records:
            with output_fastq.open("at") as open_fq:
                open_fq.write_records(*zip(*output_records))

        return SequencingData([output_fastq]), SequencingData()

    def supports_multiprocessing(self):
        return False

    @staticmethod
    def remove_trailing_none(lst):
        while lst and lst[-1] is None:
            lst.pop()


@register("SlidingWindowQualityFilter")
class SlidingWindowQualityFilter(Filter):
    """
    Remove records from a .fastq file based on quality scores within small
    regions of the read.

    The whole read is scanned by focussing on subsequent fixed-sized regions
    of the read ('windows'). For each window, the avarage quality score is calculated
    from the quality scores per nucleotide within that window. The quality scores
    are assumed to be Illumina 1.8+ Phred+33 encoded. If the average quality score
    of the window is smaller then a defined threshold, it is counted as a "bad" window.
    Once calculations for a window have finished, the next window is selected by
    moving the selection one nucleotide forward. If the number of windows counted as "bad"
    is above a user defined limit, the entire read is discarded.

    example::

        window_size = 21
        count = 1 (maximum number of "bad" windows allowed to retain the read)
        average_quality = 25 (minimum required threshold to retain a window as "good")

        @EU861894-140/1
        CCGATCTCTCGGCCTGCCCGGGGA
        ??CFFF?;HHAH#III??CFFF?,
        |.........20........|       average quality score < 25 : total count of "bad" windows = 1
         |.........25........|      average quality score = 25 : total count of "bad" windows = 1
          |.........30........|     average quality score > 25 : total count of "bad" windows = 1
           |.........24........|    average quality score < 25 : total count of "bad" windows = 2

        total count of bad windows (2) is greater than user defined count threshold (1).
        So, the read is discarded.


    :param window_size: Length of the nucleotide sequence per 'window',
        used to extract quality scores from the fastq file.
    :type window_size: int
    :param average_quality: Quality threshold for a window to be treated
        as having a "bad" average quality score.
    :type average_quality: int
    :param count: Threshold for the maximum number of "bad" windows allowed to retain the read.
    :type count: int
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
    :raises ValueError: The average quality within the window could not be
        interpreted as an integer.
    :raises ValueError: The window size could not be interpreted as an integer.
    :raises ValueError: The window size of the reads should be expressed as a
        strictly POSITIVE integer.
    :raises ValueError: The count could not be interpreted as an integer.
    :raises ValueError: The count should be expressed as a strictly POSITIVE integer.
    """

    def __init__(
        self,
        window_size: int,
        average_quality: int,
        count: int,
        output_file_name_template: str,
        output_directory: Union[Path, str],
    ):
        try:
            average_quality = int(average_quality)
        except ValueError:
            raise ValueError(
                "The average quality threshold within the window should be expressed as an integer."
            )

        try:
            window_size = int(window_size)
        except ValueError:
            raise ValueError("The window size should be expressed as an integer.")
        else:
            if not 0 < window_size:
                raise ValueError(
                    "The window size should be expressed as a strictly POSITIVE integer."
                )

        try:
            count = int(count)
        except ValueError:
            raise ValueError("The count should be expressed as an integer.")
        else:
            if not 0 < count:
                raise ValueError("The count should be expressed as a strictly POSITIVE integer.")

        self._count = count
        self._window_size = window_size
        self._average_quality = average_quality
        Filter.__init__(self, output_file_name_template, output_directory)

    class Builder:
        def __init__(self, fastq_type: Type[Fastq]):
            self._fastq_type: Type[Fastq] = fastq_type

        def build(self, *args, **kwargs):
            return SlidingWindowQualityFilter(*args, **kwargs)

    def perform(self, fastq: Fastq):
        output_fastq = fastq.create_from_properties(
            self._output_file_name_template,
            self._output_directory,
            orientation=fastq.orientation,
            run=fastq.run,
            extension=fastq.extension,
            sample_name=fastq.sample_name,
        )
        if fastq.empty:
            return SequencingData([output_fastq]), SequencingData()

        output_records = [None] * 20000
        i = -1
        with fastq.open("rt") as open_fastq:
            for records in open_fastq.records():
                write_records = True
                count_violation = 0
                for record in records:
                    if not write_records:
                        break
                    phred_scores = record.letter_annotations.get("phred_quality")
                    windows = self.windows(phred_scores, self._window_size)
                    curr_window = next(windows)
                    window_sum = sum(next(windows))
                    last_int = curr_window.popleft()
                    for curr_window in windows:
                        window_sum = window_sum - last_int
                        last_int = curr_window.popleft()
                        window_sum += last_int
                        average_window_score = window_sum / self._window_size
                        if average_window_score < self._average_quality:
                            count_violation += 1
                            if count_violation >= self._count:
                                write_records = False
                            break

                if write_records:
                    i += 1
                    try:
                        output_records[i] = records
                    except IndexError:
                        with output_fastq.open("at") as open_fq:
                            open_fq.write_records(*zip(*output_records))
                        output_records = [None] * 20000
                        output_records[0] = records
                        i = 0

        self.remove_trailing_none(output_records)
        if output_records:
            with output_fastq.open("at") as open_fq:
                open_fq.write_records(*zip(*output_records))

        return SequencingData([output_fastq]), SequencingData()

    @staticmethod
    def remove_trailing_none(lst):
        while lst and lst[-1] is None:
            lst.pop()

    @staticmethod
    def windows(seq: Iterable, size: int):
        it = iter(seq)
        win = deque((next(it, None) for _ in range(size)), maxlen=size)
        yield win
        append = win.append
        for e in it:
            append(e)
            yield win

    def supports_multiprocessing(self):
        return False


@register("RemovePatternFilter")
class RemovePatternFilter(CommandLineWrapper, Filter):
    """
    Remove reads from fastq files based on the presence of a sequence
    pattern. The pattern must occur in the read without error.

    :param pattern: The pattern that will be searched for in the read.
    :type pattern: str
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
    """

    def __init__(
        self,
        pattern: Union[str, Path],
        output_file_name_template: str,
        output_directory: Union[Path, str],
    ):
        try:
            self._pattern = fasta_to_dict(pattern)
        except FileNotFoundError:
            self._pattern = pattern.strip("\"'")
            if not _is_valid_dna(self._pattern):
                raise ValueError(
                    ("The pattern is neither a valid DNA sequence " "or a valid .fasta file.")
                )
        CommandLineWrapper.__init__(self, "cutadapt")
        Filter.__init__(self, output_file_name_template, output_directory)

    class Builder:
        def __init__(self, fastq_type: Type[Fastq]):
            self._fastq_type: Type[Fastq] = fastq_type

        def build(self, *args, **kwargs):
            return RemovePatternFilter(*args, **kwargs)

    def pattern(self, sample_name: str):
        try:
            return self._pattern[sample_name]
        except TypeError:
            return self._pattern
        except KeyError as e:
            raise ValueError("Could not find sample in the pattern fasta file.") from e

    def perform(self, fastq: Fastq):
        files = fastq.files
        output_fastq = fastq.create_from_properties(
            self._output_file_name_template,
            self._output_directory,
            orientation=fastq.orientation,
            run=fastq.run,
            extension=fastq.extension,
            sample_name=fastq.sample_name,
        )
        if fastq.empty:
            return SequencingData([output_fastq]), SequencingData()
        output_files = [file_.name for file_ in output_fastq.files]

        output_file_arg = [part for arg_ in list(zip(["-o", "-p"], output_files)) for part in arg_]
        pattern = self.pattern(fastq.sample_name)
        args = [
            # https://cutadapt.readthedocs.io/en/stable/guide.html#regular-3-adapters
            # Cutadapt allows regular 3’ adapters to occur in full anywhere within the read
            "-a",
            pattern,
            "--no-indels",
            "-e",
            "0",
            "--discard-trimmed",
            "-o",
            len(pattern)
            # "-j", self.cores,
        ]
        args.extend(output_file_arg)
        args.extend(files)
        super().run(*args, working_directory=self._output_directory)
        return SequencingData([output_fastq]), SequencingData()

    def supports_multiprocessing(self):
        return False  # Cutadapt multiprocessing is slow
