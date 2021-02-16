import os
import pathlib
from typing import Optional
import subprocess
from dataclasses import dataclass

from .installer import Installer
from .present_working_directory import present_working_directory


@dataclass(frozen=True)
class Remote:
    name: str
    account: str


class ProjectsDirectoryMaker(Installer):
    def __init__(
        self,
        base: Optional[pathlib.Path] = None
    ) -> None:

        if base is None:
            base = pathlib.Path.home()

        self._projects = base.joinpath('projects')

    def install(self) -> None:
        os.makedirs(
            name=self._projects,
            exist_ok=True,
        )

        self._install_stk()

    def _install_stk(self) -> None:
        stk_master = self._projects.joinpath('stk', 'master')
        subprocess.run([
            'git',
            'clone',
            'https://lukasturcani@github.com/lukasturcani/stk',
            str(stk_master),
        ])

        remotes = (
            Remote('stk', 'supramolecular-toolkit'),
            Remote('lt', 'lukasturcani'),
            Remote('jelfs', 'JelfsMaterialsGroup'),
        )

        with present_working_directory(stk_master):
            for remote in remotes:

                url = (
                    'https://lukasturcani@github.com/'
                    f'{remote.account}/stk'
                )

                subprocess.run([
                    'git',
                    'remote',
                    'set-url',
                    '--add',
                    '--push',
                    'origin',
                    url,
                ])
                subprocess.run([
                    'git',
                    'remote',
                    'add',
                    remote.name,
                    url,
                ])
