from itertools import chain
from typing import List, TextIO, Tuple, Optional, Iterable, Iterator

from wai.common.cli.options import TypedOption, Option
from wai.common.iterate import random

from ...stream import ThenFunction, DoneFunction
from ...stream.util import ProcessState
from ...util import chain_map, recursive_iglob, read_file_list, InstanceState
from .._SourceComponent import SourceComponent
from ._WithRandomness import WithRandomness


class LocalFilenameSource(WithRandomness, SourceComponent[Tuple[str, bool]]):
    """
    Source which yields globbed file-names from disk.
    """
    # The name of the input annotation files to read from
    inputs: List[str] = TypedOption(
        "-i", "--input",
        type=str,
        metavar="FILENAME",
        action="concat"
    )

    # The names of files to load input lists from
    input_files: List[str] = TypedOption(
        "-I", "--inputs-file",
        type=str,
        metavar="FILENAME",
        action="concat"
    )

    # The names of files to include in the conversion without annotations
    negatives: List[str] = TypedOption(
        "-n", "--negative",
        type=str,
        metavar="FILENAME",
        action="concat"
    )

    # The names of files to load negative lists from
    negative_files: List[str] = TypedOption(
        "-N", "--negatives-file",
        type=str,
        metavar="FILENAME",
        action="concat"
    )

    # The filename to write read files to
    output_filename: Optional[str] = TypedOption(
        "-o", "--output-file",
        type=str,
        metavar="FILENAME",
        help="optional file to write read filenames into"
    )

    # The open file handle to write to
    _file_handle: Optional[TextIO] = ProcessState(
        lambda self: open(self.output_filename, "w") if self.output_filename is not None else None
    )

    def produce(
            self,
            then: ThenFunction[Tuple[str, bool]],
            done: DoneFunction
    ):
        # Warn the user if no input files were specified
        if len(self.input_file_names) + len(self.negative_file_names) == 0:
            self.logger.warning("No input files selected to convert")

        inputs = self.input_file_names

        if self.has_random:
            inputs = tuple(random(iter(inputs), self.random))

        for input in inputs:
            then((input, False))
            if self._file_handle is not None:
                self._file_handle.write(f"{input},false\n")

        negatives = self.negative_file_names

        if self.has_random:
            negatives = tuple(random(iter(negatives), self.random))

        for negative in negatives:
            then((negative, True))
            if self._file_handle is not None:
                self._file_handle.write(f"{negative},true\n")

        if self._file_handle is not None:
            self._file_handle.close()

        done()

    @InstanceState
    def input_file_names(self) -> Tuple[str, ...]:
        return tuple(self.load_file_names(self.inputs, self.input_files))

    @InstanceState
    def negative_file_names(self) -> Tuple[str, ...]:
        return tuple(self.load_file_names(self.negatives, self.negative_files))

    @classmethod
    def load_file_names(cls, direct_files: Iterable[str], list_files: Iterable[str]) -> Iterator[str]:
        return chain(
            chain_map(recursive_iglob, direct_files),
            chain_map(read_file_list, chain_map(recursive_iglob, list_files))
        )

    @classmethod
    def get_help_text_for_inputs_option(cls) -> str:
        return "Input files (can use glob syntax)"

    @classmethod
    def get_help_text_for_input_files_option(cls) -> str:
        return "Files containing lists of input files (can use glob syntax)"

    @classmethod
    def get_help_text_for_negatives_option(cls) -> str:
        return "Files that have no annotations (can use glob syntax)"

    @classmethod
    def get_help_text_for_negative_files_option(cls) -> str:
        return "Files containing lists of negative files (can use glob syntax)"

    @classmethod
    def get_help_text_for_option(cls, option: Option) -> Optional[str]:
        if option is cls.inputs:
            return cls.get_help_text_for_inputs_option()
        if option is cls.input_files:
            return cls.get_help_text_for_input_files_option()
        if option is cls.negatives:
            return cls.get_help_text_for_negatives_option()
        if option is cls.negative_files:
            return cls.get_help_text_for_negative_files_option()
        return super().get_help_text_for_option(option)

