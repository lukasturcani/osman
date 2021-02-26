from typing import Iterable, Union
import subprocess

from .installer import Installer


class Pip(Installer):
    def __init__(
        self,
        packages: Union[str, Iterable[str]],
    ):
        if isinstance(packages, str):
            packages = (packages, )

        self._packages = tuple(packages)

    def install(self) -> None:
        for package in self._packages:
            subprocess.run(
                args=['sudo', 'pip', 'install', package],
                check=True,
            )


class Pip3(Installer):
    def __init__(
        self,
        packages: Union[str, Iterable[str]],
    ):
        if isinstance(packages, str):
            packages = (packages, )

        self._packages = tuple(packages)

    def install(self) -> None:
        for package in self._packages:
            subprocess.run(
                args=['sudo', 'pip3', 'install', package],
                check=True,
            )
