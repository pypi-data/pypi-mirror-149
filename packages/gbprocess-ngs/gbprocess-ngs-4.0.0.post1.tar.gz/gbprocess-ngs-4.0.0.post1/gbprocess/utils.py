import logging
import os
import shutil
import subprocess
from abc import ABC
from pathlib import Path
from typing import Text, Union

from Bio.Data.IUPACData import ambiguous_dna_letters
from Bio.Seq import Seq
from Bio.SeqIO.FastaIO import FastaTwoLineParser

logger = logging.getLogger("Utils")


class CommandLineWrapper(ABC):
    def __init__(self, executable: Text):
        if not shutil.which(executable):
            raise RuntimeError(
                f"Executable {executable} can not be found "
                + "(please install it or make sure it is added "
                + "to the PATH)."
            )
        self._executable = executable

    def run(self, *args, working_directory=None, **kwargs):
        argument_list = [str(arg) for arg in args]
        for item in kwargs.items():
            argument_list.extend(item)
        logger.debug(f"Running {[self._executable] + argument_list}")
        try:
            output = subprocess.check_output(
                [self._executable] + argument_list,
                cwd=working_directory,
                stderr=subprocess.STDOUT,
            )
            self._write_output_to_file(working_directory, output)
            return output
        except subprocess.CalledProcessError as err:
            logger.error(err.stdout.decode("utf-8"))
            self._write_output_to_file(working_directory, err.stdout)
            raise err

    def _write_output_to_file(self, working_directory: Path, output: bytes):
        with (working_directory / f"{str(self)}_{os.getpid()}.out").open("ba") as output_file:
            output_file.write(output)


def fasta_to_dict(file_path: Union[str, Path]):
    with open(file_path, "rt") as handler:
        try:
            reader = FastaTwoLineParser(handler)
            return dict(reader)
        except ValueError:
            raise ValueError(
                f"Input file {str(file_path)} must be a valid fasta file and "
                "one record must consist of with two lines."
            )


def reverse_complement(dna):
    seq = Seq(dna)
    return str(seq.reverse_complement())


def _is_valid_dna(dna):
    for letter in dna:
        if letter.upper() not in ambiguous_dna_letters:
            return False
    return True
