from typing import Iterable, Union
import subprocess

from .installer import Installer


class Apt(Installer):
    def __init__(
        self,
        packages: Union[str, Iterable[str]],
    ):
        if isinstance(packages, str):
            packages = (packages, )

        self._packages = tuple(packages)

    def install(self) -> None:
        subprocess.run(
            args=['sudo', 'apt', 'install', *self._packages],
            check=True,
        )
