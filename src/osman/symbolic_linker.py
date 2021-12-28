from typing import Iterable, Union
import subprocess

from .installer import Installer
from .symbolic_link import SymbolicLink


class SymbolicLinker(Installer):
    def __init__(
        self,
        symbolic_links: Union[SymbolicLink, Iterable[SymbolicLink]],
        root: bool = False,
    ):
        if isinstance(symbolic_links, SymbolicLink):
            symbolic_links = (symbolic_links, )

        self._symbolic_links = tuple(symbolic_links)
        self._root = root

    def install(self) -> None:

        for link in self._symbolic_links:
            link.destination.parent.mkdir(parents=True, exist_ok=True)
            command = ['sudo'] if self._root else []
            command += [
                'ln',
                '-sf',
                str(link.source),
                str(link.destination),
            ]
            subprocess.run(command, check=True)
