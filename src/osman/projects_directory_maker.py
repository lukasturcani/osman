import os
import pathlib
import subprocess
from dataclasses import dataclass
from typing import Optional

from .installer import Installer
from .present_working_directory import present_working_directory


@dataclass(frozen=True)
class Remote:
    name: str
    account: str


class ProjectsDirectoryMaker(Installer):
    def __init__(self, base: Optional[pathlib.Path] = None) -> None:

        if base is None:
            base = pathlib.Path.home()

        self._projects = base.joinpath("projects")

    def install(self) -> None:
        os.makedirs(
            name=self._projects,
            exist_ok=True,
        )

        self._install_stk()

    def _install_stk(self) -> None:
        stk_master = self._projects.joinpath("stk", "master")
        subprocess.run(
            args=[
                "git",
                "clone",
                "https://lukasturcani@github.com/lukasturcani/stk",
                str(stk_master),
            ],
            check=True,
        )

        remotes = (
            Remote("stk", "supramolecular-toolkit"),
            Remote("lt", "lukasturcani"),
            Remote("jelfs", "JelfsMaterialsGroup"),
        )

        with present_working_directory(stk_master):
            subprocess.run(
                args=[
                    "git",
                    "remote",
                    "add",
                    "all",
                    "https://lukasturcani@github.com/lukasturcani/stk",
                ],
                check=True,
            )

            for remote in remotes:

                url = (
                    "https://lukasturcani@github.com/" f"{remote.account}/stk"
                )

                subprocess.run(
                    args=[
                        "git",
                        "remote",
                        "set-url",
                        "--add",
                        "--push",
                        "all",
                        url,
                    ],
                    check=True,
                )
                subprocess.run(
                    args=[
                        "git",
                        "remote",
                        "add",
                        remote.name,
                        url,
                    ],
                    check=True,
                )

            subprocess.run(["git", "fetch", "origin"], check=True)

            subprocess.run(
                args=[
                    "git",
                    "branch",
                    "master",
                    "-u",
                    "origin/master",
                ],
                check=True,
            )
