from __future__ import annotations

import logging
from abc import ABC, abstractmethod
from pathlib import Path
from string import Formatter
from typing import Optional, Tuple, Type, Union

from ..data import Fastq, SequencingData

logger = logging.getLogger("Operation")

NUCLEOTIDE_CODE = set(("A", "C", "G", "T", "N", "R", "Y", "S", "W", "K", "M", "B", "D", "H", "V"))
NUCLEOTIDE_CODE.update(set(nucl.lower() for nucl in NUCLEOTIDE_CODE))
_ALL_OPERATIONS = {}


def register(name):
    def _register(cls):
        _ALL_OPERATIONS[name] = cls
        return cls

    return _register


def get_operation(name):
    try:
        return _ALL_OPERATIONS[name]
    except KeyError:
        raise NotImplementedError(f"Operation {name} not supported.")


class Operation(ABC):
    """Abstract class that defines an operation to be performed on Fastq objects.

    :param output_file_name_template: Template used to create the name of output files.
                                      The output file name template follows the syntax
                                      of format strings as described in
                                      `PEP 3101 <https://www.python.org/dev/peps/pep-3101/>`__.
                                      The template consists of text data that is transferred as-is
                                      to the output file name and replacement fields (indicated by
                                      curly braces) that describe what should be inserted in
                                      place of the field. The field name, the element inside the
                                      curly braces of the replacement field,must refer to a property
                                      attribute of the .fastq file if perform() is called.
    :type output_file_name_template: str
    :param output_directory: Path to an existing directory that will
        hold the output for this operation.
    :type output_directory: Union[Path, str]
    :raises ValueError: The output directory is not an existing directory.
    :raises ValueError: Invalid file name template syntax.
    :raises ValueError: Format specification is currently not supported
        for output file name templates.
    """

    def __init__(self, output_file_name_template: str, output_directory: Union[Path, str]):
        self._cores = 1
        self.output_directory = output_directory
        self.output_file_name_template = output_file_name_template

    @classmethod
    def builder(cls, fastq_type: Type[Fastq]):
        return cls

    def __str__(self):
        return type(self).__name__

    @abstractmethod
    def perform(self, fastq: Fastq) -> Tuple[SequencingData, Optional[SequencingData]]:
        raise NotImplementedError

    @abstractmethod
    def supports_multiprocessing(self):
        raise NotImplementedError

    @property
    def cores(self):
        return self._cores

    @property
    def output_directory(self):
        return self._output_directory

    @output_directory.setter
    def output_directory(self, val):
        output_directory = Path(val)
        if not output_directory.exists():
            output_directory.mkdir()
        if output_directory.exists() and not output_directory.is_dir():
            raise ValueError("The output directory is not an existing directory.")
        self._output_directory = output_directory

    @property
    def output_file_name_template(self):
        return self._output_file_name_template

    @output_file_name_template.setter
    def output_file_name_template(self, val):
        output_file_name_template = str(val)
        self.check_output_file_name_template(output_file_name_template)
        self._output_file_name_template = output_file_name_template

    @cores.setter
    def cores(self, val):
        try:
            val = int(val)
        except ValueError:
            raise ValueError("The number of cores should be an integer with a value above 0.")
        else:
            if not val > 0:
                raise ValueError("The number of cores should be an integer with a value above 0.")
            elif not self.supports_multiprocessing() and not val == 1:
                raise ValueError("This operation does not support multiprocessing.")
            self._cores = val

    @staticmethod
    def check_output_file_name_template(template: str):
        if "{extension}" in template and not template.endswith("{extension}"):
            raise ValueError(
                "As a file ends with the extension, the {extension} field "
                + "can only be defined at the end of the file name template. "
            )
        formatter = Formatter()
        try:
            format_iter = formatter.parse(template)
        except ValueError:
            raise ValueError(f"Invalid file name template: {template}")
        else:
            for _, field_name, format_spec, _ in format_iter:
                if format_spec:
                    raise ValueError(
                        "Format specification is currently not supported for "
                        f"output file name templates, use {{{field_name}}} "
                        f"instead of {{{field_name}:{format_spec}}}."
                    )
