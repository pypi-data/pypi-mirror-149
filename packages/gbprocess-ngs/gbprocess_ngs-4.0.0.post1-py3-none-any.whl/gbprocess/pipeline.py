import datetime
import logging
import multiprocessing
from abc import ABC, abstractmethod
from collections import defaultdict
from csv import DictWriter
from pathlib import Path
from tempfile import TemporaryDirectory
from typing import Dict, Iterable, List, Union

from .data import Fastq, SequencingData
from .operations.operation import Operation

logger = logging.getLogger("Pipeline")


class Pipeline(ABC):
    def __init__(self, temp_dir="/tmp"):
        self._operations: List[Operation] = []
        temp_dir = Path(temp_dir)
        if temp_dir and not temp_dir.is_dir():
            raise ValueError("Temporary directory path is not a directory.")
        else:
            self._temp_dir = temp_dir

    def add_operation(self, operation: Operation) -> None:
        """Schedule an operation in the pipeline.
           Operations will be added at the end of the execution queue.

        :param operation: The operation to be scheduled for execution.
        :type operation: Operation
        """
        if not isinstance(operation, Operation):
            raise ValueError("Can only add operations to the execution queue.")
        self._operations.append(operation)

    @abstractmethod
    def execute(self, seq_data: SequencingData) -> None:
        """Excude the scheduled queue of operations.
           Operations are performed on a FIFO-basis.

        :param seq_data: The data that is used as the input for the first operation.
        :type seq_data: SequencingData
        """

    @staticmethod
    def _compression_worker(fastq: Fastq, compression_suffix: str):
        result = fastq.compress(compression_suffix=compression_suffix)
        fastq.remove()
        return result

    @staticmethod
    def _stats_worker(fastq: Fastq):
        return fastq.number_of_records()

    @staticmethod
    def _get_compressed_runs(seq_data: SequencingData) -> Dict[str, str]:
        return {fastq.run: fastq.compression for fastq in seq_data if fastq.compressed}

    @staticmethod
    def _write_stats(stats: Dict[str, Dict[str, Iterable[int]]], output_dir: Union[str, Path]):
        curr_date_time = datetime.datetime.now().strftime("%Y%m%d%H%M")
        stats_location = Path(output_dir) / f"gbprocess_stats_{curr_date_time}.csv"
        with stats_location.open("w") as csvfile:
            operations = list(stats.keys())
            runs = set(run for stat in stats.values() for run in stat.keys())
            writer = DictWriter(csvfile, fieldnames=["run"] + operations)
            writer.writeheader()
            for run in runs:
                row = {"run": run}
                for operation in operations:
                    try:
                        row[operation] = sum(stats[operation][run])
                    except KeyError:
                        row[operation] = 0
                writer.writerow(row)


class SerialPipeline(Pipeline):
    def __init__(self, temp_dir="/tmp"):
        super().__init__(temp_dir)

    def execute(self, seq_data: SequencingData) -> None:
        """Excude the scheduled queue of operations.
           Operations are performed on a FIFO-basis.

        :param seq_data: The data that is used as the input for the first operation.
        :type seq_data: SequencingData
        """
        if not isinstance(seq_data, SequencingData):
            raise ValueError("Expected sequencingData object.")

        if not self._operations:
            return seq_data

        stats = {}
        stats["original"] = self._stats(seq_data)

        with TemporaryDirectory(dir=str(self._temp_dir)) as temp_dir:
            # Decompress, keep track of what samples were compressed
            compressed_runs = self._get_compressed_runs(seq_data)
            seq_data = self._decompress(seq_data, temp_dir)

            for operation in self._operations:
                previous_seq = seq_data
                logger.info(f"Performing operation {operation}")
                seq_data, _ = seq_data.edit(operation)
                stats[str(operation)] = seq_data.stats()

                if compressed_runs:
                    self._compress(compressed_runs, previous_seq)

            if self._operations:
                last_output_dir = self._operations[-1].output_directory
                self._write_stats(stats, last_output_dir)
                self._compress(compressed_runs, previous_seq)

    @staticmethod
    def _stats(seq_data: SequencingData) -> Dict[str, Dict[str, Iterable[int]]]:
        stats = defaultdict(list)
        for fastq in seq_data:
            stats[fastq.run].append(fastq.number_of_records())
        return stats

    @staticmethod
    def _decompress(seq_data: SequencingData, temp_dir: str) -> SequencingData:
        uncompressed_fastqs = []
        for fastq in seq_data:
            if fastq.compressed:
                uncompressed_fastqs.append(fastq.decompress(temp_dir))
            else:
                uncompressed_fastqs.append(fastq)
        return SequencingData(uncompressed_fastqs)

    def _calculate_stats(self, seq_data: SequencingData) -> Dict[str, Dict[str, Iterable[int]]]:
        stats = defaultdict(list)
        for fastq in seq_data:
            stats[fastq.run].append(fastq.number_of_records())
        return stats

    def _compress(self, compressed_runs: Dict[str, str], seq_data: SequencingData):
        for fastq in seq_data:
            try:
                compression_suffix = compressed_runs[fastq.run]
            except KeyError:
                pass
            else:
                self._compression_worker(fastq, compression_suffix)
                fastq.remove()


class MultiProcessPipeline(Pipeline):
    """A pipeline schedules operations that are performed on sequencing data for execution.

    `Pipeline` stores the operations to be performed on sequencing data
    and allows for sequential execution of these operations. Output from one operation
    is passed on as input for the next operation.


    :param cpu: Number of cores or threads the operations scheduled in the pipeline
                are allowed to use. The maximum amount of cores
                or threads is limited to the value provided., defaults to 1
    :type cpu: int, optional
    :param temp_dir: Path to a directory where temporary files will be placed., defaults to "/tmp"
    :type temp_dir: str, optional
    :raises ValueError: The amnount of cores/threads defined by the user could
        not be interpreted as an integer.
    :raises ValueError: More maximum cores/threads were requested then available by on the system,
                        being the cpu count reduced by 1 or 1 for single-core systems.
    :raises ValueError: Temporary directory path is not a directory or does not exits.
    """

    def __init__(self, cpu: int = 1, temp_dir="/tmp"):
        try:
            cpu = int(cpu)
        except ValueError:
            raise ValueError("The amnount of cores/threads to use should be an integer.")
        else:
            max_proc = multiprocessing.cpu_count() - 1 or 1
            if cpu > max_proc:
                raise ValueError(
                    "Please leave at least one processing unit available for the system."
                )
            self._cpu = cpu

        super().__init__(temp_dir)
        logger.debug(
            f"Created parallel pipeline with options cpu: {self._cpu}, "
            f"temporary directory: {self._temp_dir}"
        )

    def execute(self, seq_data: SequencingData) -> None:
        """Excude the scheduled queue of operations.
           Operations are performed on a FIFO-basis.

        :param seq_data: The data that is used as the input for the first operation.
        :type seq_data: SequencingData
        """
        if not isinstance(seq_data, SequencingData):
            raise ValueError("Expected sequencingData object.")

        if not self._operations:
            return seq_data

        stats = {}
        with TemporaryDirectory(dir=str(self._temp_dir)) as temp_dir:
            # Decompress, keep track of what samples were compressed
            compressed_runs = self._get_compressed_runs(seq_data)
            decompressed_runs = []
            for fastq in seq_data:
                if fastq.compressed:
                    decompressed_runs.append(fastq.decompress(temp_dir, threads=self._cpu))
                else:
                    decompressed_runs.append(fastq)
            seq_data = SequencingData(decompressed_runs)
            with multiprocessing.Pool(self._cpu) as p:
                stats["original"] = self._stats(p, seq_data)
                # Perform operations
                for operation in self._operations:
                    previous_seq = seq_data
                    if operation.supports_multiprocessing():
                        operation.cores = self._cpu
                        seq_data, _ = seq_data.edit(operation)
                    elif len(seq_data) >= self._cpu:  # No split needed:
                        seq_data, _ = seq_data.edit_parallel(p, operation, self._cpu)
                    else:
                        split_seq_data = seq_data.split(self._cpu, temp_dir)
                        result_split, aux_split = split_seq_data.edit_parallel(
                            p, operation, cpu=self._cpu
                        )
                        seq_data = result_split.join(operation.output_file_name_template)
                        aux_split.join(operation.output_file_name_template)
                        split_seq_data.remove()
                    stats[str(operation)] = self._stats(p, seq_data)
                    if compressed_runs:
                        self._compress(p, compressed_runs, previous_seq)

                if self._operations:
                    last_output_dir = self._operations[-1].output_directory
                    self._write_stats(stats, last_output_dir)
                    self._compress(p, compressed_runs, seq_data, background=False)

    def _stats(
        self, pool: multiprocessing.Pool, seq_data: SequencingData
    ) -> Dict[str, Dict[str, Iterable[int]]]:
        stats = defaultdict(list)
        stats_list = pool.map(self._stats_worker, seq_data)
        for fastq, stat in zip(seq_data, stats_list):
            stats[fastq.run].append(stat)
        return stats

    def _compress(
        self,
        pool: multiprocessing.Pool,
        compressed_runs: Dict[str, str],
        seq_data: SequencingData,
        background=True,
    ):
        need_to_be_compressed = []
        for fastq in seq_data:
            extension = compressed_runs.get(fastq.run)
            if extension:
                need_to_be_compressed.append((fastq, extension))
        if background:
            pool.starmap_async(self._compression_worker, need_to_be_compressed)
        else:
            pool.starmap(self._compression_worker, need_to_be_compressed)
