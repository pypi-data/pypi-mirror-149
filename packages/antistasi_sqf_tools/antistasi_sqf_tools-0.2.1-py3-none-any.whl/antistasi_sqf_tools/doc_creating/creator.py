"""
WiP.

Soon.
"""

# region [Imports]

import os

import shutil

from time import time, sleep

from pathlib import Path

from typing import TYPE_CHECKING, Union, Callable, Iterable, Optional, Mapping, Any, IO, TextIO, BinaryIO, Hashable, Generator, Literal, TypeVar, TypedDict, AnyStr

from tempfile import TemporaryDirectory

from antistasi_sqf_tools.doc_creating.config_handling import find_config_file, DocCreationConfig
from sphinx.cmd.build import main as sphinx_build
# endregion[Imports]

# region [TODO]


# endregion [TODO]

# region [Logging]


# endregion[Logging]

# region [Constants]

THIS_FILE_DIR = Path(__file__).parent.absolute()

# endregion[Constants]python -m fastero


class Creator:

    def __init__(self, config_file: Union[str, os.PathLike], builder_name: str, base_folder: Union[str, os.PathLike] = None) -> None:
        self.builder_name = builder_name
        self.base_folder = Path(config_file).resolve().parent if base_folder is None else Path(base_folder).resolve()
        self.config = DocCreationConfig(config_file)
        self.is_release = False
        if self.builder_name == "release":
            self.is_release = True
            self.builder_name = self.config.get_release_builder_name()

    def build(self):
        if self.is_release is True:
            return self.release()

        output_dir = self.config.get_output_dir(self)
        output_dir.mkdir(parents=True, exist_ok=True)
        with TemporaryDirectory() as temp_dir:
            temp_build_dir = Path(temp_dir).resolve()
            args = ["-M", self.builder_name, str(self.config.get_source_dir(self)), str(temp_build_dir)]
            returned_code = sphinx_build(args)
            if returned_code == 0:
                shutil.rmtree(output_dir)
                shutil.copytree(temp_build_dir / self.builder_name, output_dir, dirs_exist_ok=True)

    def release(self):
        output_dir = self.config.get_release_output_dir()
        output_dir.mkdir(exist_ok=True, parents=True)

        with TemporaryDirectory() as temp_dir:
            temp_build_dir = Path(temp_dir).resolve()
            args = ["-M", self.builder_name, str(self.config.get_release_source_dir()), str(temp_build_dir)]
            returned_code = sphinx_build(args)
            if returned_code == 0:
                shutil.rmtree(output_dir)
                shutil.copytree(temp_build_dir / self.builder_name, output_dir, dirs_exist_ok=True)

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(builder_name={self.builder_name!r}, base_folder={self.base_folder.as_posix()!r}, config={self.config!r})"

# region[Main_Exec]


if __name__ == '__main__':
    pass

# endregion[Main_Exec]
