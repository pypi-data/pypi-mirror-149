from __future__ import annotations

import bz2
import gzip
import logging
import multiprocessing
import os
import re
import shutil
from abc import ABC, abstractclassmethod, abstractmethod
from copy import deepcopy
from functools import partial
from io import SEEK_CUR, SEEK_END
from itertools import chain, islice, repeat, zip_longest
from math import ceil
from pathlib import Path
from typing import TYPE_CHECKING, Iterable, Iterator, Union

from Bio import SeqIO
from xopen import xopen

if TYPE_CHECKING:
    from .operations.operation import Operation

multiprocessing.set_start_method("spawn", True)

LOGGER = logging.getLogger("Data")


class Editable(ABC):
    @abstractmethod
    def edit(self, operation: Operation):
        """Edit data by performing an operation."""


class MultiprocessEditable(Editable, ABC):
    @abstractmethod
    def edit_parallel(self, pool: multiprocessing.Pool, operation: Operation, cpu: int = 1):
        """Edit data by performing an operation in parallel."""

    @staticmethod
    def worker_function(operation: Operation, editable: Editable):
        return editable.edit(operation)


class SequencingData(MultiprocessEditable):
    """Represents a collection of .fastq sequencing samples.

    SequencingData groups a number of Fastq objects.

    """

    def __init__(self, fastq_files: Iterable[Fastq] = None):
        if fastq_files is None:
            fastq_files = []
        for fastq in fastq_files:
            if not isinstance(fastq, Fastq):
                raise ValueError("Expected an iterable of fastq files.")
        self._fastq_files = list(fastq_files)

    def __add__(self, other):
        return SequencingData(self._fastq_files + other._fastq_files)

    def __iadd__(self, other):
        return self + other

    def __radd__(self, other):
        if other == 0:
            return self
        return self + other

    def __iter__(self):
        yield from iter(self._fastq_files)

    def __len__(self):
        return len(self._fastq_files)

    @classmethod
    def from_directory(
        cls,
        model: Fastq,
        directory: Union[Path, str],
        file_name_template: str,
        exclude=None,
    ):
        LOGGER.info("Looking for fastq files in %s.", directory)
        directory_path = Path(directory)
        if not directory_path.is_dir():
            raise ValueError(f"Path {directory_path} does not exist or is not a directory.")
        excluded_files = list(directory.glob(exclude)) if exclude else []
        LOGGER.info("Excluded files: %s.", excluded_files)
        fastq_files = sorted(
            [
                file_
                for file_ in directory_path.iterdir()
                if file_.is_file()
                and file_.suffix in (".fastq", ".fq", ".bzip2", ".bzp2", ".bz2", ".gzip", ".gz")
                and file_ not in excluded_files
            ]
        )
        LOGGER.debug("Fast files found: %s", fastq_files)
        if not fastq_files:
            raise ValueError("No sequence files found.")
        iterator = iter(fastq_files)
        result = []
        while True:
            try:
                result.append(model.pop(iterator, file_name_template, exists_ok=True))
            except StopIteration:
                break
        LOGGER.info("Number of fastq samples: %s", len(result))
        return cls(result)

    def edit(self, operation: Operation) -> SequencingData:
        result_seq, aux_seq = SequencingData(), SequencingData()
        for fastq in self._fastq_files:
            result, aux_data = operation.perform(fastq)
            result_seq += result
            aux_seq += aux_data
        return result_seq, aux_seq

    def edit_parallel(self, pool: multiprocessing.Pool, operation: Operation, cpu: int):
        result_seq, aux_seq = SequencingData(), SequencingData()
        seq_list = pool.map(partial(self.worker_function, operation), self._fastq_files)
        for (seq, aux_data) in seq_list:
            result_seq += seq
            aux_seq += aux_data
        return result_seq, aux_seq

    def split(self, pieces: int, output_dir: Path) -> _SplitSequencingData:
        result = []

        for fastq_sample in self._fastq_files:
            result.append(fastq_sample.split(pieces, output_dir))

        # Transpose list
        result = [SequencingData(lst) for lst in map(list, zip(*result))]
        return _SplitSequencingData(result, self._fastq_files)

    def join(self, other: SequencingData) -> SequencingData:
        new_fastq = []
        if not self._fastq_files:
            return other
        if not other._fastq_files:
            return self

        for fastq1, fastq2 in zip(self, other):
            new_fastq.append(fastq1.join(fastq2))
        return SequencingData(new_fastq)

    def remove(self):
        for fastq in self:
            fastq.remove()


class _SplitSequencingData(MultiprocessEditable):
    def __init__(self, seq_data_list: Iterable[SequencingData], original_fastqs: Iterable[Fastq]):
        self._seq_data_list: Iterable[SequencingData] = seq_data_list
        self._original_fastqs: Iterable[Fastq] = original_fastqs

    def __iter__(self):
        yield from self._seq_data_list

    def edit(self, operation: Operation):
        seq_list, aux_list = zip(*[self.worker_function(operation, seq) for seq in iter(self)])
        return _SplitSequencingData(seq_list, self._original_fastqs), _SplitSequencingData(
            aux_list, self._original_fastqs
        )

    def join(self, output_file_name_template):
        joined_results = SequencingData()
        for seq in self._seq_data_list:
            joined_results = joined_results.join(seq)

        renamed_fastqs = []
        original_fastq_repeated = list(
            chain.from_iterable(
                repeat(fastq, len(joined_results) // len(self._original_fastqs))
                for fastq in self._original_fastqs
            )
        )
        assert len(original_fastq_repeated) == len(joined_results)
        for original_fastq, fastq in zip(original_fastq_repeated, joined_results):
            original_extension = original_fastq.extension
            new_properties = fastq.properties
            new_properties["extension"] = original_extension
            renamed_fastqs.append(fastq.rename(output_file_name_template, **new_properties))

        return SequencingData(renamed_fastqs)

    def edit_parallel(self, pool: multiprocessing.Pool, operation: Operation, cpu: int):
        seq_list, aux_list = zip(*pool.map(partial(self.worker_function, operation), iter(self)))
        return _SplitSequencingData(seq_list, self._original_fastqs), _SplitSequencingData(
            aux_list, self._original_fastqs
        )

    def remove(self):
        for seq in iter(self):
            seq.remove()


class Fastq(Editable, ABC):
    @abstractmethod
    def __init__(
        self,
        *files: Union[str, Path],
        run=None,
        sample_name=None,
        extension=None,
        orientation=None,
        exists_ok=False,
    ):
        fastq_paths = [Path(file_) for file_ in files]
        if not fastq_paths:
            raise ValueError("No files specified to create fastq sample.")
        if exists_ok:
            if not all([file_.is_file() for file_ in fastq_paths]):
                raise ValueError("A fastq file that was specified does not exists.")
            if any(
                [
                    file_.samefile(file2_)
                    for i, file_ in enumerate(fastq_paths)
                    for j, file2_ in enumerate(fastq_paths)
                    if i != j
                ]
            ):
                raise ValueError("Some of the specified files are the same!")
        else:
            if any(
                [
                    file_ == file2_
                    for i, file_ in enumerate(fastq_paths)
                    for j, file2_ in enumerate(fastq_paths)
                    if i != j
                ]
            ):
                raise ValueError("The forward and reverse path point to the same file.")
            for file_ in fastq_paths:
                file_.touch(exist_ok=False)

        self._files = [file_.resolve() for file_ in fastq_paths]
        self.run = run
        self.extension = extension
        self.sample_name = sample_name
        self.orientation = orientation
        # Read buffer when splitting files
        self._SPLIT_BUFFER = 25 * 16 * 1024  # 25 Mb

    def __eq__(self, other):
        """Override the default Equals behavior"""
        if isinstance(other, type(self)):
            return self._files == other.files
        return False

    def __ne__(self, other):
        """Override the default Equals behavior"""
        if isinstance(other, type(self)):
            return self._files != other.files
        return False

    def __hash__(self) -> int:
        return hash(self.files)

    @abstractclassmethod
    def pop(cls, iterator: Iterator):
        raise NotImplementedError

    @classmethod
    def create_from_properties(
        cls, file_name_template: str, directory: Union[str, Path], **template_values
    ):
        directory = Path(directory)
        if not directory.is_dir():
            raise ValueError("The given path does not seem to be a directory.")
        paths = cls.fill_template_to_path(file_name_template, directory, **template_values)
        if len(paths) != len(set(paths)):
            raise ValueError(
                "Could not create unique file paths by filling file name template "
                f"{file_name_template} with values {template_values}. "
                "Please consider using a different file name template."
            )
        return cls(*paths, **template_values)

    def open(self, mode="rb", threads=0):
        return _OpenFastq(self, mode=mode, threads=threads)

    def edit(self, operation: Operation):
        return operation.perform(self)

    def number_of_records(self):
        open_fastq = self.open(mode="r")
        number_of_newlines = []
        while True:
            parts = open_fastq.read(65536)
            if not parts:
                raise ValueError("No results from reading file?")
            if not any(parts):
                if not number_of_newlines:
                    return 0
                numbers_per_file = list(map(list, zip(*number_of_newlines)))
                sum_per_file = set([sum(numbers) for numbers in numbers_per_file])
                if len(sum_per_file) > 1:
                    raise ValueError("Got different number of lines per file in sample %r", self)
                return sum_per_file.pop() // 4
            counts = [part.count("\n") for part in parts]
            number_of_newlines.append(counts)

    @property
    def properties(self):
        return {
            "run": self.run,
            "extension": self.extension,
            "sample_name": self.sample_name,
            "orientation": self.orientation,
        }

    @property
    def files(self) -> Iterable:
        return self._files.copy()

    @property
    def empty(self):
        if any([os.stat(file_).st_size for file_ in self.files]):
            return False
        for file_ in self.files:
            with file_.open("rt") as open_fastq:
                buf = open_fastq.read(16)
                while buf:
                    if len(buf.strip()):
                        return False
                    buf = open_fastq.read(16)
        return True

    @property
    def run(self) -> str:
        return self._run

    @run.setter
    def run(self, val):
        if val is None:
            self._run = None
        elif isinstance(val, str):
            self._run = val
        else:
            raise ValueError(
                "The run name must be the same for all files in a sample, "
                f"got more than one value: {val}"
            )

    @property
    def extension(self) -> str:
        return self._extension

    @extension.setter
    def extension(self, val):
        if val is None:
            self._extension = None
        elif isinstance(val, str):
            self._extension = val
        else:
            raise ValueError(
                "The extension name must be the same for all files in a sample, "
                f"got more than one value: {val}"
            )

    @property
    def sample_name(self) -> str:
        return self._sample_name

    @sample_name.setter
    def sample_name(self, val):
        if val is None:
            self._sample_name = None
        elif isinstance(val, str):
            self._sample_name = val
        else:
            raise ValueError(
                f"The sample name must be the same for all files in a sample, "
                f"got more than one value: {val}"
            )

    @property
    @abstractmethod
    def orientation(self):
        raise NotImplementedError

    @orientation.setter
    @abstractmethod
    def orientation(self):
        raise NotImplementedError

    @property
    def compression(self):
        suffixes = set(self._check_compression(path_) for path_ in self.files)
        if len(suffixes) > 1:
            raise ValueError("The different files seem to have a different compression format.")
        return suffixes.pop()

    @property
    def compressed(self):
        if self.compression in (".fq", ".fastq"):
            return False
        return True

    def rename(self, file_name_template: str, **props):
        names = self.fill_template_to_path(template=file_name_template, directory=None, **props)
        if len(names) != len(self.files):
            raise ValueError(
                "Could not rename files: number of new names"
                "does not match number of files to rename."
            )

        new_paths = []
        for new_name, old_fastq in zip(names, self.files):
            new_paths.append(old_fastq.with_name(new_name))
            old_fastq.rename(old_fastq.with_name(new_name))
        return type(self)(*new_paths, **props, exists_ok=True)

    def remove(self):
        for file_ in self.files:
            os.remove(file_)

    @staticmethod
    def _check_compression(input_file: Path):
        if not input_file.is_file():
            raise ValueError("File does not exist or is not a file.")

        suffix_to_handler_generator = {
            ".gz": gzip.open,
            ".bz2": bz2.open,
            ".fastq": open,
            ".fq": open,
        }

        suffix = input_file.suffix
        if suffix in suffix_to_handler_generator.keys():
            return suffix
        else:
            if os.stat(input_file).st_size:  # file is not empty
                for suffix, handler in suffix_to_handler_generator.items():
                    with handler(input_file, "r") as handle:
                        try:
                            handle.read(2048)
                        except (OSError, EOFError, UnicodeDecodeError):
                            pass
                        else:
                            return suffix
            else:
                raise ValueError(
                    "Could not determine file format "
                    + "because the file is empty and the "
                    + "extension is not recognized."
                )
        raise RuntimeError("Could not open file %s, unknown format." % input_file)

    @classmethod
    def _get_property_value_from_filenames(
        cls, file_name_template: str, files: Iterable, property_: str
    ):
        parsed_file_names = [
            _FastqFileNameTemplate(file_name_template).parse(file_.name) for file_ in files
        ]
        return cls._get_property_from_parsed_filenames(parsed_file_names, property_)

    @classmethod
    def _get_property_from_parsed_filenames(cls, parsed_file_names: Iterable, property_: str):
        if None in parsed_file_names:
            raise ValueError("Could not parse the file name to a properties.")
        try:
            result = [parsed_file_name[property_] for parsed_file_name in parsed_file_names]
            if len(set(result)) == 1:
                return str(result.pop())
            else:
                return result
        except KeyError:
            return None

    @classmethod
    def fill_template_to_path(cls, template, directory=None, **template_values):
        template_values_no_none = {
            key_: value_ for key_, value_ in template_values.items() if value_ is not None
        }
        if not template_values_no_none:
            raise ValueError("The template values contained only None values.")
        flattened_template_values = cls._split_dict(template_values_no_none)
        paths = []
        for template_value in flattened_template_values:
            try:
                if directory:
                    paths.append(directory / template.format_map(template_value))
                else:
                    paths.append(template.format_map(template_value))
            except KeyError:
                raise ValueError(
                    "Not all values within the file template were filled to form a file name."
                )
        return paths

    @staticmethod
    def _split_dict(to_flatten):
        temp_dict = [{}]
        for field_name, template_values in to_flatten.items():
            if bool(iter(template_values)) and not isinstance(template_values, str):
                temp_dict = [deepcopy(item) for item in repeat(temp_dict, len(template_values))]
                for part, new_value in zip(temp_dict, template_values):
                    for to_update_dict in part:
                        to_update_dict[field_name] = new_value
                temp_dict = [subitem for item in temp_dict for subitem in item]
            else:
                for to_update_dict in temp_dict:
                    to_update_dict[field_name] = template_values

        return temp_dict

    def split(self, pieces: int, output_directory: Path):
        output_directory = Path(output_directory)
        # Function to read a part from a file

        def read_next_part(file_, read_buffer=self._SPLIT_BUFFER):
            next_bytes = file_.read(read_buffer)
            while next_bytes:
                yield next_bytes
                next_bytes = file_.read(read_buffer)

        # Function to find a fastq record start (e.i. '@')
        def find_record_start(part, parts_iter, file_):
            record_position = part.rfind(b"\n@")
            # This @ can be a an @ at the beginning of the quality sequence or sequence identifier
            # Find the '+' before the @ to check what type of @ it is.
            qual_position = part.rfind(b"\n+", 0, record_position)
            if record_position < 0 or qual_position < 0:
                # Failed to find both. One part might be too small to find the positions
                # Add another part and try again.
                try:
                    part += next(parts_iter)
                except StopIteration:
                    return part, None, None
                else:
                    return find_record_start(part, parts_iter, file_)
            # The amount of newlines in between the @ and the + destinguishe
            # between an @ at the beginning of the quality sequence or a
            # sequence identifier
            newlines_inbetween = part.count(b"\n", qual_position + 1, record_position)
            if newlines_inbetween == 1:
                # The @ that was found is not a quality score but a sequence identifier!
                split_bytes_before, split_bytes_after = (
                    part[: record_position + 1],
                    part[record_position + 1 :],
                )
                file_.seek(-len(split_bytes_after), SEEK_CUR)
                return split_bytes_before, record_position, qual_position
            else:
                # The @ that was found was the beginning of a quality score line
                # Try again with another sequence.
                try:
                    part += next(parts_iter)
                except StopIteration:
                    return part, None, None
                else:
                    return find_record_start(part, parts_iter, file_)

        # Prepare output files
        props = {
            "run": self.run,
            "orientation": self.orientation,
            "sample_name": self.sample_name,
        }

        extension_str = self.extension if self.extension else ""
        extension_index = -len(self.extension) if self.extension else None
        new_paths = [
            [
                output_directory / f"{file_.name[:extension_index]}_{i}{extension_str}"
                for file_ in self._files
            ]
            for i in range(pieces)
        ]

        new_paths_t = map(list, zip(*new_paths))
        new_fastqs_list = [
            type(self)(*new_path, **props, extension=f"_{i}{extension_str}")
            for i, new_path in enumerate(new_paths)
        ]

        # Do not split if empty, return the empty output files
        if self.empty:
            return SequencingData(new_fastqs_list)

        with self.open(mode="rb") as open_fastq:
            (first_file, *other_files) = open_fastq._opened_files
            new_paths_list_iter = iter(new_paths_t)

            # Split the first file based on the file size
            # Get the size of one split file
            output_files = next(new_paths_list_iter)
            curr_output_file = output_files.pop(0).open("wb")
            target_one_chunk_size = ceil(os.stat(first_file.name).st_size / pieces)

            # Keep statistics for for current file
            curr_chunk_size = 0
            curr_chunk_lines = 0
            newlines_per_written_per_file = []  # Needed to split other files

            # Read the file in parts untill the chunk size is reached.
            file_parts = read_next_part(first_file)
            for next_bytes in file_parts:  # Loop over the file parts
                if (
                    curr_chunk_size + len(next_bytes) < target_one_chunk_size
                ):  # If the part still fits in the current chunk, add it.
                    curr_chunk_size += len(next_bytes)
                    curr_chunk_lines += next_bytes.count(b"\n")
                    curr_output_file.write(next_bytes)
                else:  # Maximum size of chunk reached, push (partially) to next chunk
                    # We want the file to end with a full record, get everything up to that part.
                    to_write, _, _ = find_record_start(next_bytes, file_parts, first_file)

                    # Write to file
                    curr_chunk_size += len(to_write)
                    curr_chunk_lines += to_write.count(b"\n")
                    curr_output_file.write(to_write)

                    # Close the current file and open the next one.
                    curr_output_file.close()
                    newlines_per_written_per_file.append(curr_chunk_lines)
                    curr_output_file = output_files.pop(0).open("wb")

                    # Reset stats
                    curr_chunk_lines = 0
                    curr_chunk_size = 0

            if curr_chunk_lines != 0:
                newlines_per_written_per_file.append(curr_chunk_lines + 1)

            curr_output_file.close()
            # Split the other files, this time based on the number of lines.
            if other_files:
                for other_file, destination_files in zip(other_files, new_paths_list_iter):
                    reads_list = [
                        islice(other_file, elem) for elem in newlines_per_written_per_file
                    ]
                    for reads, destination_file in zip(reads_list, destination_files):
                        with destination_file.open("wb") as open_dest:
                            open_dest.writelines(reads)

        return SequencingData(new_fastqs_list)

    def decompress(self, output_directory: Union[Path, str] = None, threads=0):
        if self.compressed:
            props_uncompressed = {
                "run": self.run,
                "orientation": self.orientation,
                "sample_name": self.sample_name,
                "extension": ".fastq",
            }
            uncompressed_fastq = type(self)(
                *[
                    (file_.parent if not output_directory else Path(output_directory))
                    / (Path(file_.stem).stem + ".fastq")
                    for file_ in self.files
                ],
                **props_uncompressed,
            )
            with self.open("rb", threads=threads) as f_in:
                with uncompressed_fastq.open("wb") as f_out:
                    f_out.copyfileobj(f_in)
            return uncompressed_fastq
        else:
            raise ValueError("Already decompressed.")

    def compress(
        self,
        compression_suffix: str,
        output_directory: Union[str, Path] = None,
        threads=0,
    ):
        if not self.compressed:
            props_compressed = {
                "run": self.run,
                "orientation": self.orientation,
                "sample_name": self.sample_name,
            }
            new_paths = [
                (output_directory if output_directory else file_.parent)
                / f"{file_.name}{compression_suffix}"
                for file_ in self.files
            ]
            fastq_comp = type(self)(
                *new_paths,
                **props_compressed,
                extension=f"{self.extension}{compression_suffix}",
            )

            with self.open("rb") as f_in:
                with fastq_comp.open("wb", threads=threads) as f_out:
                    f_out.copyfileobj(f_in)
            return fastq_comp
        else:
            raise ValueError("Already compressed.")

    def join(self, other):
        if other.empty:
            LOGGER.debug(f"Fastq sample {other} is empty, not merging and removing.")
            other.remove()
            return self

        write_newline = False
        if not self.empty:
            with self.open("rb") as into:
                into.seek(-1, SEEK_END)
                last_bytes = set(into.read(1))
                if len(last_bytes) != 1 or not last_bytes.pop().endswith(b"\n"):
                    write_newline = True

            if write_newline:
                with self.open("ab") as into:
                    into.write(*([b"\n"] * len(other.files)))

        LOGGER.debug(f"Copying contents from {self} to {other}")
        for file_dest, file_ in zip(self.files, other.files):
            with open(file_dest, "ab") as dest, open(file_, "rb") as src:
                write_newline = False
                src.seek(-1, 2)
                last_bytes = src.read(1)
                if not last_bytes.endswith(b"\n"):
                    write_newline = True
                src.seek(0, 0)
                shutil.copyfileobj(src, dest)
                if write_newline:
                    dest.write(b"\n")
        other.remove()
        return self


class _OpenFastq(object):
    def __init__(self, fastq: Fastq, mode: str = None, threads: int = 1):
        if not fastq.files:
            raise ValueError("Could not open sample %r, because files specified.", fastq)
        self._opened_files = [xopen(file_, mode=mode, threads=threads) for file_ in fastq.files]

    def __iter__(self):
        def chunks(iterable, size=4):
            args = [iter(iterable)] * size
            yield from zip_longest(fillvalue=size, *args)

        yield from zip(*[chunks(file_) for file_ in self._opened_files])

    def __enter__(self):
        return self

    def __exit__(self, exception_type, exception_value, traceback):
        for file_ in self._opened_files:
            file_.close()

    def copyfileobj(self, other: _OpenFastq):
        for file_dest, file_ in zip(self._opened_files, other._opened_files):
            shutil.copyfileobj(file_, file_dest)
        return self

    def records(self):
        yield from zip(*[SeqIO.parse(file_, "fastq") for file_ in self._opened_files])

    def write_records(self, *records_per_file):
        for records, file_ in zip(records_per_file, self._opened_files):
            SeqIO.write(records, file_, "fastq")

    def writelines(self, *lines_per_file):
        for lines, file_ in zip(lines_per_file, self._opened_files):
            file_.writelines(lines)

    def write(self, *to_write):
        for lines, file_ in zip(to_write, self._opened_files):
            file_.write(lines)

    def close(self):
        for file_ in self._opened_files:
            file_.close()

    def seek(self, offset, whence):
        for file_ in self._opened_files:
            file_.seek(offset, whence)

    def read(self, size):
        return [file_.read(size) for file_ in self._opened_files]

    def truncate(self, size=None):
        for file_ in self._opened_files:
            file_.truncate(size)


class PairedEndFastq(Fastq):
    def __init__(
        self,
        fastq_forward: Union[str, Path],
        fastq_reverse: Union[str, Path],
        run=None,
        sample_name=None,
        orientation=None,
        extension=None,
        exists_ok=False,
    ):
        if not orientation:
            LOGGER.warning("Paired-end fastq files might need to have the orientation set.")
        super().__init__(
            fastq_forward,
            fastq_reverse,
            run=run,
            sample_name=sample_name,
            orientation=orientation,
            extension=extension,
            exists_ok=exists_ok,
        )

    def __repr__(self):
        return "PairedEndFastq(files=%r,run=%r,extension=%r,sample_name=%r, orientation=%r)" % (
            self._files,
            self.run,
            self.extension,
            self.sample_name,
            self.orientation,
        )

    @classmethod
    def pop(cls, iterator: Iterator, file_name_template: str, exists_ok=False):
        forward = next(iterator)
        try:
            reverse = next(iterator)
        except StopIteration:
            raise ValueError("An odd number of fastq files was found!")
        forward, reverse = Path(forward), Path(reverse)
        if not forward.is_file() and not reverse.is_file():
            raise ValueError("Expected two existing files.")
        LOGGER.debug(f"Found forward file {forward} together with reverse file {reverse}.")
        if file_name_template:
            properties = ["run", "sample_name", "orientation", "extension"]
            filled_properties = {
                property_: cls._get_property_value_from_filenames(
                    file_name_template, [forward, reverse], property_
                )
                for property_ in properties
            }
            return cls(forward, reverse, **filled_properties, exists_ok=exists_ok)
        else:
            return cls(forward, reverse, exists_ok=exists_ok)

    @property
    def orientation(self):
        return self._orientation

    @orientation.setter
    def orientation(self, val):
        if val is None:
            self._orientation = None
        else:
            if len(val) != 2 or len(set(val)) != len(val):
                raise ValueError(
                    "The orientation must be specified by a list of 2 unique characters."
                )
            self._orientation = tuple(val)


class SingleEndFastq(Fastq):
    def __init__(
        self,
        fastq_path: Union[str, Path],
        run=None,
        sample_name=None,
        extension=None,
        orientation=None,
        exists_ok=False,
    ):
        super().__init__(
            fastq_path,
            run=run,
            sample_name=sample_name,
            extension=extension,
            orientation=orientation,
            exists_ok=exists_ok,
        )

    def __repr__(self):
        return "SingleEndFastq(files=%r,run=%r,extension=%r,sample_name=%r, orientation=%r)" % (
            self._files,
            self.run,
            self.extension,
            self.sample_name,
            self.orientation,
        )

    @classmethod
    def pop(
        cls,
        iterator: Iterator[Union[str, Path]],
        file_name_template: str,
        exists_ok=False,
    ):
        file_ = next(iterator)
        file_ = Path(file_)
        if not file_.is_file():
            raise ValueError("Expected (an) existing file(s).")
        if file_name_template:
            properties = ["run", "sample_name", "orientation", "extension"]
            filled_properties = {
                property_: cls._get_property_value_from_filenames(
                    file_name_template, [file_], property_
                )
                for property_ in properties
            }
            return cls(file_, **filled_properties, exists_ok=exists_ok)
        else:
            return cls(file_, exists_ok=exists_ok)

    @property
    def orientation(self):
        return self._orientation

    @orientation.setter
    def orientation(self, val):
        if val is None:
            self._orientation = None
        else:
            if len(val) != 1:
                raise ValueError(
                    "The orientation must be specified by a list containing one unique character."
                )
            self._orientation = tuple(val[0])


class _FastqFileNameTemplate:
    PARSE_RE = re.compile(r"""({{|}}|{\w*(?:(?:\.\w+))*(?::[^}]+)?})""")
    REGEX_SAFETY = re.compile(r"""([?\\\.[\]\()\*+\^$\!\|])""")

    def __init__(self, template: str):
        if not template:
            raise ValueError("Expected a non-zero length file name template.")
        self._groups = []
        self._template = template
        self._regex_expression = self._to_regex(template)

    def _to_regex(self, template):
        expression = []
        for part in self.PARSE_RE.split(template):
            name = None
            if not part:
                continue
            elif part == "{{":
                expression.append(r"\{")
            elif part == "}}":
                expression.append(r"\}")
            elif part.startswith("{") and part.endswith("}"):
                part = part[1:-1]
                width = None
                if ":" in part:
                    name, width = part.split(":")
                    try:
                        width = int(width)
                    except ValueError:
                        raise ValueError(
                            "The width specified in the file name template must be an integer."
                        )
                else:
                    name = part

                if not name:
                    raise ValueError("A field in the template must have a name.")
                if not re.match(r"^\w+$", name):
                    raise ValueError(
                        "A field in the template must contain all alphabatic characters."
                    )
                if name in self._groups:
                    expression.append(r"(?P={})".format(name))
                    pass
                else:
                    to_append = (
                        r"(?P<{}>.*)".format(name)
                        if not width
                        else r"(?P<{}>.{{{}}})".format(name, width)
                    )
                    expression.append(to_append)
                    pass
                self._groups.append(name)
            else:
                # just some text to match
                expression.append(self.REGEX_SAFETY.sub(lambda x: "\\" + x.group(1), part))
                pass
        return "".join(expression)

    def parse(self, to_parse):
        m = re.match(self._regex_expression, to_parse)
        if not m:
            raise ValueError(
                (
                    "Could not parse the file name template "
                    f"'{self._template}' with the given path '{to_parse}'."
                )
            )
        return {group: m[group] for group in self._groups}
