from typing import Iterable, Union
import subprocess

from .installer import Installer


class Pacman(Installer):
    def __init__(
        self,
        packages: Union[str, Iterable[str]],
    ):
        if isinstance(packages, str):
            packages = (packages, )

        self._packages = tuple(packages)

    def install(self) -> None:
        subprocess.run([
            'sudo', 'pacman', '-S', ' '.join(self._packages)
        ])
