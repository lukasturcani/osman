from typing import Iterable, Union, Optional
import pathlib
import subprocess

from .installer import Installer
from .present_working_directory import present_working_directory


class AurManager(Installer):
    def __init__(
        self,
        packages: Union[str, Iterable[str]],
        build_directory: Optional[pathlib.Path] = None,
    ) -> None:

        if isinstance(packages, str):
            packages = (packages, )

        self._packages = tuple(packages)

        if build_directory is None:
            build_directory = pathlib.Path.home().joinpath('builds')

        self._build_directory = build_directory

    def install(self) -> None:
        self._build_directory.mkdir(exist_ok=True)

        for package in self._packages:
            package_directory = self._build_directory.joinpath(package)
            subprocess.run([
                'git',
                'clone',
                f'https://aur.archlinux.org/{package}',
                str(package_directory),
            ])

            with present_working_directory(package_directory):
                subprocess.run(['makepkg', '-si'])
