from typing import Union, Iterable
import pathlib

from .installer import Installer


class DirectoryMaker(Installer):
    def __init__(
        self,
        directories: Union[pathlib.Path, Iterable[pathlib.Path]],
    ) -> None:

        if isinstance(directories, pathlib.Path):
            directories = (directories, )

        self._directories = tuple(
            directory.resolve() for directory in directories
        )

    def install(self) -> None:

        for directory in self._directories:
            directory.mkdir(exist_ok=True)
