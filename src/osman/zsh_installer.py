from typing import Union, Iterable
import pathlib
import subprocess

from .installer import Installer


class ZshInstaller(Installer):
    def __init__(
        self,
        plugins: Union[str, Iterable[str]],
    ) -> None:

        if isinstance(plugins, str):
            plugins = (plugins, )

        self._plugins = tuple(plugins)

        self._plugin_directory = pathlib.Path.home().joinpath(
            '.zsh',
            'plugins',
        )

    def install(self) -> None:
        subprocess.run(
            args=[
                'git',
                'clone',
                'https://github.com/romkatv/powerlevel10k',
                pathlib.Path.home().joinpath('.zsh', 'powerlevel10k'),
            ],
            check=True,
        )
        for plugin in self._plugins:
            *_, name = plugin.split('/')
            destination = str(self._plugin_directory.joinpath(name))
            subprocess.run(
                args=['git', 'clone', plugin, destination],
                check=True,
            )
